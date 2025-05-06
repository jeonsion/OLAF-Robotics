# Olaf(ongoing)
Autonomous Driving Robot
---

### Installation
```
sudo apt-get install ros-noetic-serial
```

### Build LiDAR SDK
```
git clone https://github.com/YDLIDAR/YDLidar-SDK.git
cd YDLidar-SDK/build
cmake ..
make
sudo make install
```

### Permission Setting
```
cd /dev
sudo chmod 777 *
```
