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
    "53": (7.67016077041626, 6.969274044036865),
    "1": (15.101937294006348, 6.4472761154174805),
    "2": (14.799625396728516, 4.137206077575684)
}

# ROS 노드 초기화
rospy.init_node('STOMP_ROS')
start_pub = rospy.Publisher('/start_point', PointStamped, queue_size=10)
end_pub = rospy.Publisher('/end_point', PointStamped, queue_size=10)

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
                if "startPoint" in data and "endPoint" in data:
                    start_point = str(data["startPoint"])
                    end_point = str(data["endPoint"])
                    print(f"User {start_point}에서 User {end_point}로 전달합니다.")

                    x, y = click_point_mapping[start_point]
                    publish_click_point(x, y, 'start')
                    x, y = click_point_mapping[end_point]
                    publish_click_point(x, y, 'end')
                elif "bookLocation" in data and "userLocation" in data:
                    book_location = str(data["bookLocation"])
                    user_location = str(data["userLocation"])
                    print(f"User {user_location}이 책을 대여했습니다.")
                    x, y = click_point_mapping[book_location]
                    publish_click_point(x, y, 'start')
                    x, y = click_point_mapping[user_location]
                    publish_click_point(x, y, 'end')
                    
                else:
                    print(f"Unknown message format: {data}")
            except json.JSONDecodeError as e:
                print(f"Prepare to Receive Message")

def publish_click_point(x, y, point_type):
    point_msg = PointStamped()
    point_msg.header.stamp = rospy.Time.now()
    point_msg.header.frame_id = "map"
    point_msg.point.x = x
    point_msg.point.y = y
    point_msg.point.z = 0.0

    if point_type == 'start':
        print(f"Publishing start point: {point_msg}")
        start_pub.publish(point_msg)
    elif point_type == 'end':
        print(f"Publishing end point: {point_msg}")
        end_pub.publish(point_msg)
    else:
        proint(f"Unknown point type: {point_type}")


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
