import sys, pygame
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *

from objloader import *
from func1 import *
from moveobj import *

pygame.init()
viewport = (800,600)
hx = viewport[0]/2
hy = viewport[1]/2
srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)

mob1 = Monster()
moblist = [mob1]

model1 = Moveobj("3dmodel/box.obj",5,7,-6,-0.7,0,20,30)
model2 = Moveobj("3dmodel/box.obj",10,0,-2,1.0,0,180,20)

model1_1 = Moveobj("3dmodel/box.obj",15,0,-5,0.1,0,-20,0)
model2_1 = Moveobj("3dmodel/box.obj",20,0,0,0.1,0,90,0)

omodel1 = Moveobj2(z = -5,y=0 ,x=35,anglez = 30, anglex =20,angley = 30,velocity=0.1)
omodel2 = Moveobj2(z = -5,y=0 ,x=40,anglez = 20, anglex = 10,angley= 20,velocity=-0.1)

olist1 = [omodel1]
olist2 = [omodel2]

wall1 = Wall(x=-15,y=-5)
wall2 = Wall(x=-25,y=5,state=1)
wall3 = Wall(x=-5,y=5,state=1)
wall4 = Wall(x=-15,y=15)
wall5 = Wall(x=-15,y=5,z=-10,state=2)
wall6 = Wall(x=-15,y=5,z= 10,state=2)

circle1 = Moveobj("3dmodel/circle.obj",x=20,y=0,z=-5,velocity=0.1,xlen=1,angle1=0)
circle2 = Moveobj("3dmodel/circle.obj",x=30,y=0,z=-5,velocity=-0.1,xlen=1,angle1=0)
circle3 = Moveobj("3dmodel/circle.obj",x=0,y=20,z=-5,velocity=0.0,xlen=1,angle1=0)

bcircle = Moveobj("3dmodel/circle.obj",x=-10,y=10,z=-5,velocity=1,xlen=1,angle1=30,angle2=30)
gcircle = Moveobj("3dmodel/circle.obj",x=-13,y=10,z=-5,velocity=1,xlen=1,angle1=90,angle2=30)

circlelist1 = []
circlelist2 = []
circlelist1.append(circle1)
circlelist1.append(circle3)
circlelist2.append(circle2)

bcirclelist = []
bcirclelist.append(bcircle)
bcirclelist.append(gcircle)


modellist1 = []
modellist2 = []
modellist1.append(model1)
modellist2.append(model2)
modellist1.append(model1_1)
modellist2.append(model2_1)

walllist = []
walllist.append(wall2)
walllist.append(wall1)
walllist.append(wall3)
walllist.append(wall4)
walllist.append(wall5)
walllist.append(wall6)

# 빛
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 0.2))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.4, 0.4, 0.4, 0.6))
glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0,1.0,1.0,1.0))
glEnable(GL_LIGHT0)

glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_DEPTH_TEST)  

clock = pygame.time.Clock()

glMatrixMode(GL_PROJECTION)

width, height = viewport
gluPerspective(90.0, width/float(height), 1, 100.0)

glMatrixMode(GL_MODELVIEW)
glEnable(GL_DEPTH_TEST)

rx, ry = (0,0)
pos = [0,0,5]
rotate = False
lightpos = [0,0,-50]
angle = 0

time = 0
tick = 0

while 1:
    df = clock.tick(60)

    tick += 1
    if(tick == 60):
        time += 1
        mob1.hungry -= 1
        print(mob1.hungry)
        tick = 0

    for e in pygame.event.get():
        if e.type == QUIT:
            sys.exit()

        elif e.type == KEYDOWN:
            if(e.key == K_ESCAPE):
                sys.exit()

        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1: rotate = True
        elif e.type == MOUSEBUTTONUP:
            if e.button == 1: rotate = False
        elif e.type == MOUSEMOTION:
            i, j = e.rel
            if rotate:
                rx += i
                ry += j


    event = pygame.key.get_pressed()

    #로컬 x축 z축 구하기
    movex = [math.cos(math.radians(rx)),0,-math.sin(math.radians(rx))]
    movez = [math.sin(math.radians(rx)),0,math.cos(math.radians(rx))]

    # wasd 로 앞 뒤 양옆으로, rf로 위아래로 이동
    if(event[K_d]):
        for i in range(3):
            pos[i] -= movex[i]*0.2
                  
    if(event[K_a]):
        for i in range(3):
            pos[i] += movex[i]*0.2
    
    if(event[K_w]):
        for i in range(3):
            pos[i] -= movez[i]*0.2
    
    if(event[K_s]):
        for i in range(3):
            pos[i] += movez[i]*0.2

    if(event[K_r]):
        pos[1] -= 0.2

    if(event[K_f]):
        pos[1] += 0.2


    # 회전 후 이동
    glLoadIdentity()
    glRotate(ry, 1, 0, 0)
    glRotate(rx, 0, 1, 0)
    glTranslate(pos[0], pos[1], -pos[2])
    
    

    angle += 0.02
    if(angle >= 360):
        angle -= 360
    lightpos[0] = -200*math.cos(math.radians(angle))
    lightpos[1] = 200*math.sin(math.radians(angle))

    glLightfv(GL_LIGHT0, GL_POSITION,  (lightpos[0], lightpos[1], lightpos[2], 0.0))
    
    listhungry(moblist,pos)

    listmove1(modellist1,df), listmove1(modellist2,df)
    listmove1(circlelist1,df); listmove1(circlelist2,df); listmove1(bcirclelist,df); listmove1(olist1,df); listmove1(olist2,df)
    circlelist1[1].gravity(df),  listmove1(moblist,df)

    boxtobox(modellist1, modellist2)
    boxtobox(olist1,olist2)
    circletocircle(circlelist1, circlelist2)
    circletowall(bcirclelist,walllist)
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    
    listrender1(modellist1);listrender1(modellist2); listrender1(circlelist1);listrender1(circlelist2); listrender1(bcirclelist)
    listrender2(walllist); listrender3(olist1); listrender3(olist2); listrender3(moblist)

    pygame.display.flip()