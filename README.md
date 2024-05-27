# Olaf(ongoing)
LINC 3.0 시제작품 공모전

---

### Installation
```
sudo apt-get install ros-noetic-serial
```

### Build LiDAR SDK[]
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
