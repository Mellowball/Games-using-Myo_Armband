import pygame
import random

##함수
def eventProcess():
    global isActive, choiceUser, choiceCom, result
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isActive = False
                # pygame.quit()
            if result == -1:
                if event.key == pygame.K_LEFT:  # 가위
                    choiceUser = 0
                if event.key == pygame.K_DOWN:  # 바위
                    choiceUser = 1
                if event.key == pygame.K_RIGHT:  # 보
                    choiceUser = 2
                if choiceUser != -1:
                    resultProcess()
            else:
                if event.key == pygame.K_SPACE:  # 재시작
                    result, choiceUser, choiceCom = -1, -1, -1

def resultProcess():
    global result, win, lose, draw, choiceCom, choiceUser
    choiceCom = random.randint(0, 2)
    if choiceCom == choiceUser:
        result = 0
        draw += 1
    elif (choiceUser == 0 and choiceCom == 2)\
            or (choiceUser == 1 and choiceCom == 0)\
            or (choiceUser == 2 and choiceCom == 1):
        result = 1
        win += 1
    else:
        result = 2
        lose += 1

def setText():
    global result, win, lose, draw
    mFont = pygame.font.SysFont("굴림", 20)
    mtext = mFont.render(f'win {win}, lose {lose}, draw {draw}', True, 'green')
    SCREEN.blit(mtext, (10, 10, 0, 0))

    mFont = pygame.font.SysFont("arial", 15)
    mtext = mFont.render(
        f'(scissors : ←) (rock :  ↓) (paper : →) (continue : space)', True, 'white')
    SCREEN.blit(mtext, (CENTER_WIDTH-40, 10, 0, 0))

    mFont = pygame.font.SysFont("arial", 60)
    mtext = mFont.render(f'VS', True, 'yellow')
    SCREEN.blit(mtext, (CENTER_WIDTH-35, CENTER_HEIGHT-40, 0, 0))

    mFont = pygame.font.SysFont("arial", 40)
    mtext = mFont.render(f'Computer             User', True, 'white')
    SCREEN.blit(mtext, (CENTER_WIDTH-200, CENTER_HEIGHT-100, 0, 0))

    if result != -1:
        mFont = pygame.font.SysFont("arial", 60)
        resultText = ['Draw!!', 'Win!!', 'Lose']
        mtext = mFont.render(resultText[result], True, 'red')
        SCREEN.blit(mtext, (CENTER_WIDTH-80, CENTER_HEIGHT+100, 0, 0))

def getIndex():
    global updateTime, updateIndex
    if result == -1:
        updateTime += 1
        if updateTime > 10:
            updateTime = 0
            updateIndex = (updateIndex+1) % len(player)
        return updateIndex, updateIndex
    else:
        return choiceCom, choiceUser

def updatePlayer():
    idex1, idex2 = getIndex()

    recPlayer[idex1].centerx = CENTER_WIDTH-100
    recPlayer[idex1].centery = CENTER_HEIGHT
    SCREEN.blit(player[idex1], recPlayer[idex1])

    recPlayer[idex2].centerx = CENTER_WIDTH+100
    recPlayer[idex2].centery = CENTER_HEIGHT
    SCREEN.blit(player[idex2], recPlayer[idex2])

##변수 선언 및 초기화
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
CENTER_WIDTH = SCREEN_WIDTH/2
CENTER_HEIGHT = SCREEN_HEIGHT/2
isActive = True
updateTime = 0
updateIndex = 0
choiceUser, choiceCom = -1, -1
result = -1
win, lose, draw = 0, 0, 0
clock = pygame.time.Clock()

##pygmae init
pygame.init()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CodingNow!!")

##이미지 가져오기
pIamges = ['scissors.png', 'rock.png', 'paper.png']
player = [pygame.image.load(pIamges[i]) for i in range(len(pIamges))]
player = [pygame.transform.scale(player[i], (100, 100)) for i in range(len(player))]
recPlayer = [player[i].get_rect() for i in range(len(player))]

##효과음
pygame.mixer.init()
pygame.mixer.music.load('Cat Shat in the Box - josh pan.mp3')
pygame.mixer.music.play(-1)

##Loop
while(isActive):
    SCREEN.fill((0, 0, 0))
    eventProcess()
    updatePlayer()
    setText()
    pygame.display.flip()
    clock.tick(100)