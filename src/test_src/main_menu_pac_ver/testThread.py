
import threading
import serial

line = ''
port = '/dev/ttyUSB1'
baud = 9600
ser = serial.Serial(port, baud, timeout=0)
receivenumber = 0

##함수
def readthread(ser):
    global line, receivenumber
    for c in ser.read():
        # line 변수에 차곡차곡 추가하여 넣는다.
        line += (chr(c))
        if line.startswith('[') and line.endswith(']'):  # 라인의 끝을 만나면..
            # 데이터 처리 함수로 호출
            print('receive data=' + line)
            receivenumber = int(line[1:2])
            line = ''
            
def doThread():
    # 시리얼 읽을 쓰레드 생성
    thread = threading.Thread(target=readthread, args=(ser,))
    thread.start()
    thread.join()

def do0():
    receivenumber = 0
    # print('receivenum0 =', receivenumber)

while(1):
    doThread()
    do0()