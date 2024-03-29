# 마이오 밴드를 이용한 미니게임
### 진행 기간 : 2022년 6월 24일 ~ 12월 24일
### 참여 인원
|인원|역할|
|---|---|
|김도훈|Raspberry Pi 세팅, Python 프로그램, Arduino 펌웨어|
|장상균|Myo Armband 및 Bluetooth 모듈 세팅, 하드웨어 제작, Arduino 펌웨어|

## 사용 기술
+ <img src="https://img.shields.io/badge/Arduino-00979D?style=flat-square&logo=Arduino&logoColor=white"/> - Interface with Myo Armband, Raspberry Pi
+ <img src ="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=Python&logoColor=white"/> - Raspberry Pi Programming Language
+ <img src="https://img.shields.io/badge/Raspberry Pi-A22846?style=flat-square&logo=Raspberry Pi&logoColor=white"/> - LCD Panel(Interface with Arduino, person)
+ <img src="https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=GitHub&logoColor=white"/> - Configuration Management

## 프로젝트 설명
+ Myo Armband를 활용한 미니 게임 프로그램
+ 마이오 암밴드에 달린 근전도 센서가 근육의 움직임을 감지해 근육 동작에 맞는 이벤트 수행
+ Bluetooth 모듈로 마이오 암밴드와 아두이노가 서로 통신
+ 아두이노는 라즈베리 파이와 USB-to-TTL 케이블을 통해 서로 UART 통신
+ 라즈베리 파이에 연결된 LCD 터치 패널은 화면 및 제어 기능 제공
+ 스크린 터치와 Myo Armband의 동작을 통해 게임 플레이
+ 게임의 경우 파이썬의 pygame 라이브러리를 활용해 구현

---
## 핵심 기능 설명

### 0. Index
+ <img src ="https://github.com/Mellowball/Games-using-Myo_Armband/blob/main/img_Readme/0-index.png"/>

### 1. 전체 구조
+ <img src ="https://github.com/Mellowball/Games-using-Myo_Armband/blob/main/img_Readme/1-1.png"/>

### 2. 구조도 설명
+ <img src ="https://github.com/Mellowball/Games-using-Myo_Armband/blob/main/img_Readme/2-1.png"/>

+ <img src ="https://github.com/Mellowball/Games-using-Myo_Armband/blob/main/img_Readme/2-2.png"/>

+ <img src ="https://github.com/Mellowball/Games-using-Myo_Armband/blob/main/img_Readme/2-3.png"/>

### 3. 하드웨어 설명
+ <img src ="https://github.com/Mellowball/Games-using-Myo_Armband/blob/main/img_Readme/3-1.png"/>

+ <img src ="https://github.com/Mellowball/Games-using-Myo_Armband/blob/main/img_Readme/3-2.png"/>

+ <img src ="https://github.com/Mellowball/Games-using-Myo_Armband/blob/main/img_Readme/3-3.png"/>

+ <img src ="https://github.com/Mellowball/Games-using-Myo_Armband/blob/main/img_Readme/3-4.png"/>

+ <img src ="https://github.com/Mellowball/Games-using-Myo_Armband/blob/main/img_Readme/3-5.png"/>

### 4. 데이터 처리 과정
+ <img src ="https://github.com/Mellowball/Games-using-Myo_Armband/blob/main/img_Readme/4-1.png"/>

+ <img src ="https://github.com/Mellowball/Games-using-Myo_Armband/blob/main/img_Readme/4-2.png"/>

+ <img src ="https://github.com/Mellowball/Games-using-Myo_Armband/blob/main/img_Readme/4-3.png"/>

+ <img src ="https://github.com/Mellowball/Games-using-Myo_Armband/blob/main/img_Readme/4-4.png"/>

### 5. 게임 프로그램
+ <img src ="https://github.com/Mellowball/Games-using-Myo_Armband/blob/main/img_Readme/5-1.png"/>

+ <img src ="https://github.com/Mellowball/Games-using-Myo_Armband/blob/main/img_Readme/5-2.png"/>

+ <img src ="https://github.com/Mellowball/Games-using-Myo_Armband/blob/main/img_Readme/5-3.png"/>

### 6. 실제 동작 영상
<img src ="https://github.com/Mellowball/Games-using-Myo_Armband/blob/main/img_Readme/bluetooth_connect.gif"/>
<img src ="https://github.com/Mellowball/Games-using-Myo_Armband/blob/main/img_Readme/rsp_game.gif"/>
<img src ="https://github.com/Mellowball/Games-using-Myo_Armband/blob/main/img_Readme/dino_game.gif"/>

  
