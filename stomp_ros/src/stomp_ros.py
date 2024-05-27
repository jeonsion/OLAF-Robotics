#!/usr/bin/env python3
import argparse
import asyncio
import json
import websockets
import stomper
import rospy
from geometry_msgs.msg import PointStamped

# 매핑 테이블: 문자 -> 좌표 (x, y)
click_point_mapping = {
    "53": (7.581643104553223, 7.222347259521484),
    "54": (5.386044502258301, 8.285445213317871),
    "55": (10.152769088745117, 9.670970916748047)
}

# ROS 노드 초기화
rospy.init_node('STOMP_ROS')
pub = rospy.Publisher('/clicked_point', PointStamped, queue_size=10)

async def connect():
    ws_url = f"ws://{args.host}:{args.port}/ws"
    async with websockets.connect(ws_url) as websocket:
        # Sending a CONNECT frame to establish the STOMP connection
        await websocket.send("CONNECT\naccept-version:1.0,1.1,2.0\n\n\x00\n")

        # Subscribing to the bookinfo channel
        sub_bookinfo = stomper.subscribe("/sub/channel/bookinfo", idx="bookinfo")
        await websocket.send(sub_bookinfo)

        # Infinite loop to keep the connection alive and receive messages
        while True:
            message = await websocket.recv()
            print()
            print("#####################")
            print(f"Received message: {message}")

            # 메시지를 파싱하여 JSON 내용 추출
            parsed_message = stomper.unpack_frame(message)
            body = parsed_message['body']
            try:
                data = json.loads(body)
                location_info = data.get("locationInfo")
                if location_info in click_point_mapping:
                    x, y = click_point_mapping[location_info]
                    publish_click_point(x, y)
                else:
                    print(f"Unknown locationInfo: {location_info}")
            except json.JSONDecodeError as e:
                print(f"Ready to decode JSON")

def publish_click_point(x, y):
    # 현재 시간을 기준으로 PointStamped 메시지 생성
    point_msg = PointStamped()
    point_msg.header.stamp = rospy.Time.now()
    point_msg.header.frame_id = "map"  # 필요한 프레임 아이디로 변경
    point_msg.point.x = x
    point_msg.point.y = y
    point_msg.point.z = 0.0

    print(f"Publishing point: {point_msg}")
    # 토픽 발행
    pub.publish(point_msg)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="STOMP Client")
    parser.add_argument(
        "--host", default="192.168.1.235", help="Host for WebSocket server (default: 192.168.1.235)"
    )
    parser.add_argument(
        "--port", type=int, default=8082, help="Port for WebSocket server (default: 8082)"
    )

    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(connect())
