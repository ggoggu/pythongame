from OpenGL.GL import *
from OpenGL.GLU import *
import math

# 각도 두개로 움직이는 Moveboj 클래스의 렌더
def renderobj(obj):
    glPushMatrix()
    glTranslatef(obj.x, obj.y, obj.z)
    glRotatef(obj.angle1,0,1,0)
    glRotatef(obj.angle2,0,0,1)
    obj.render()
    glPopMatrix()

# 벽 렌더
def renderobj2(obj):
    glPushMatrix()
    glTranslatef(obj.x, obj.y, obj.z)
    if(obj.state == 1):
        glRotatef(90,0,0,1)
    elif(obj.state == 2):
        glRotatef(90,1,0,0)
    obj.render()
    glPopMatrix()

# 오일러 회전으로 회전하는 Moveojb2 클래스 렌더
def renderobj3(obj):
    glPushMatrix()
    glTranslatef(obj.x, obj.y, obj.z)
    glRotatef(obj.anglez,0,0,1)
    glRotatef(obj.anglex,1,0,0)
    glRotatef(obj.angley,0,1,0)
    obj.render()
    glPopMatrix()

# aabb 충돌
def aabbcollision1(i,j):
    if(abs(i.x - j.x) <= (i.xlen+j.xlen) and abs(i.y - j.y) <= (i.ylen+j.ylen) and abs(i.z - j.z) <= (i.zlen+j.zlen)):
        return True
    else:
        return False

# 내적    
def dot(vector1,vector2):
    sum = 0.0
    for i in range(len(vector1)):
        sum += vector1[i]*vector2[i]
    return sum

# 외적
def cross(vector1,vector2):
    return [vector1[1]*vector2[2] - vector1[2]*vector2[1],
            vector1[2]*vector2[0] - vector1[0]*vector2[2],
            vector1[0]*vector2[1] - vector1[1]*vector2[0]]

# 두점의 거리
def dist(i,j):
    return math.sqrt(math.pow(i.x - j.x,2) + math.pow(i.y - j.y,2) + math.pow(i.z - j.z,2))

# 두 점의 벡터
def distvector(i,j):
    return [i.x-j.x,i.y-j.y,i.z-j.z]
    
# 구모양 충돌    
def circlecollision(i,j):
    if(dist(i,j) <= (i.xlen+j.xlen)):
        return True
    else:
        return False

#물리식 테스트
def elasticcollision(obj1,obj2):
    velocity = obj1.velocity
    obj1.velocity = -(obj1.velocity*(obj1.mass-obj2.mass) + 2*obj2.mass*obj2.velocity)/(obj1.mass+obj2.mass)
    obj2.velocity = -(obj2.velocity*(obj2.mass-obj1.mass) + 2*obj1.mass*velocity)/(obj1.mass+obj2.mass)


#obb 충돌
def obb(obj1,obj2):
    check1 = True  
    check2 = True

    # 두 obj의 위치 벡터 차이 벡터
    list1 = distvector(obj1,obj2)
    
    # 두 obj의 로컬 x,y,z 축에서의 확인
    dist = abs(dot(list1,obj1.xnorm))
    if((abs(dot(obj1.xnorm,obj2.maxvector[0])*obj2.maxlen) + obj1.xlen) <= dist and
       (abs(dot(obj1.xnorm,obj2.maxvector[1])*obj2.maxlen) + obj1.xlen) <= dist and
       (abs(dot(obj1.xnorm,obj2.maxvector[2])*obj2.maxlen) + obj1.xlen) <= dist and
       (abs(dot(obj1.xnorm,obj2.maxvector[3])*obj2.maxlen) + obj1.xlen) <= dist):
        check1 = False
    dist = abs(dot(list1,obj1.ynorm))
    if((abs(dot(obj1.ynorm,obj2.maxvector[0])*obj2.maxlen) + obj1.ylen) <= dist and
       (abs(dot(obj1.ynorm,obj2.maxvector[1])*obj2.maxlen) + obj1.ylen) <= dist and
       (abs(dot(obj1.ynorm,obj2.maxvector[2])*obj2.maxlen) + obj1.ylen) <= dist and
       (abs(dot(obj1.ynorm,obj2.maxvector[3])*obj2.maxlen) + obj1.ylen) <= dist):
        check1 = False
    dist = abs(dot(list1,obj1.znorm))
    if((abs(dot(obj1.znorm,obj2.maxvector[0])*obj2.maxlen) + obj1.zlen) <= dist and
       (abs(dot(obj1.znorm,obj2.maxvector[1])*obj2.maxlen) + obj1.zlen) <= dist and
       (abs(dot(obj1.znorm,obj2.maxvector[2])*obj2.maxlen) + obj1.zlen) <= dist and
       (abs(dot(obj1.znorm,obj2.maxvector[3])*obj2.maxlen) + obj1.zlen) <= dist):
        check1 = False

    dist = abs(dot(list1,obj2.xnorm))
    if((abs(dot(obj2.xnorm,obj1.maxvector[0])*obj1.maxlen) + obj2.xlen) <= dist and
       (abs(dot(obj2.xnorm,obj1.maxvector[1])*obj1.maxlen) + obj2.xlen) <= dist and
       (abs(dot(obj2.xnorm,obj1.maxvector[2])*obj1.maxlen) + obj2.xlen) <= dist and
       (abs(dot(obj2.xnorm,obj1.maxvector[3])*obj1.maxlen) + obj2.xlen) <= dist ):
        check1 = False
    dist =  abs(dot(list1,obj2.ynorm))
    if((abs(dot(obj2.ynorm,obj1.maxvector[0])*obj1.maxlen)+ obj2.ylen) <= dist and
       (abs(dot(obj2.ynorm,obj1.maxvector[1])*obj1.maxlen)+ obj2.ylen) <= dist and
       (abs(dot(obj2.ynorm,obj1.maxvector[2])*obj1.maxlen)+ obj2.ylen) <= dist and
       (abs(dot(obj2.ynorm,obj1.maxvector[3])*obj1.maxlen)+ obj2.ylen) <= dist ):
        check1 = False
    dist = abs(dot(list1,obj2.znorm))
    if((abs(dot(obj2.znorm,obj1.maxvector[0])*obj1.maxlen) + obj2.zlen) <= dist and
       (abs(dot(obj2.znorm,obj1.maxvector[1])*obj1.maxlen) + obj2.zlen) <= dist and
       (abs(dot(obj2.znorm,obj1.maxvector[2])*obj1.maxlen) + obj2.zlen) <= dist and
       (abs(dot(obj2.znorm,obj1.maxvector[3])*obj1.maxlen) + obj2.zlen) <= dist ):
        check1 = False

    # 두 로컬 축의 외적
    crosslist = [cross(obj1.xnorm,obj2.xnorm),cross(obj1.xnorm,obj2.ynorm),cross(obj1.xnorm,obj2.ynorm),
                 cross(obj1.ynorm,obj2.xnorm),cross(obj1.ynorm,obj2.ynorm),cross(obj1.ynorm,obj2.znorm),
                 cross(obj1.znorm,obj2.xnorm),cross(obj1.znorm,obj2.ynorm),cross(obj1.znorm,obj2.znorm)]
    
    # 외적한 축에서의 확인
    for vector in crosslist:
        dist = abs(dot(list1,vector))
        for norm1 in obj1.maxvector:
            for norm2 in obj2.maxvector:
                if(abs(dot(vector,norm1)*obj1.maxlen) + abs(dot(vector,norm2)*obj2.maxlen) <= dist):
                    check2 = False

        if(abs(dot(obj1.xnorm,vector)*obj1.xlen) + abs(dot(obj2.xnorm,vector)*obj2.xlen) <= dist):
            check2 = False
        if(abs(dot(obj1.xnorm,vector)*obj1.xlen) + abs(dot(obj2.ynorm,vector)*obj2.ylen) <= dist):
            check2 = False
        if(abs(dot(obj1.xnorm,vector)*obj1.xlen) + abs(dot(obj2.znorm,vector)*obj2.zlen) <= dist):
            check2 = False

        if(abs(dot(obj1.ynorm,vector)*obj1.ylen) + abs(dot(obj2.xnorm,vector)*obj2.xlen) <= dist):
            check2 = False
        if(abs(dot(obj1.ynorm,vector)*obj1.ylen) + abs(dot(obj2.ynorm,vector)*obj2.ylen) <= dist):
            check2 = False
        if(abs(dot(obj1.ynorm,vector)*obj1.ylen) + abs(dot(obj2.znorm,vector)*obj2.zlen) <= dist):
            check2 = False

        if(abs(dot(obj1.znorm,vector)*obj1.zlen) + abs(dot(obj2.xnorm,vector)*obj2.xlen) <= dist):
            check2 = False
        if(abs(dot(obj1.znorm,vector)*obj1.zlen) + abs(dot(obj2.ynorm,vector)*obj2.ylen) <= dist):
            check2 = False
        if(abs(dot(obj1.znorm,vector)*obj1.zlen) + abs(dot(obj2.znorm,vector)*obj2.zlen) <= dist):
            check2 = False

    # 두 물체의 로컬 축에서 확인 되거나 외적한 축에서 확인 되면 충돌 판정
    if(check1 == True or check2 == True):
        return True
    else:
        return False

# 충돌 적용            
def boxtobox(list1, list2):
    for i in list1:
        for j in list2:
            if(obb(i,j)):
                    i.velocity = 0; j.velocity = 0
                
def circletocircle(list1, list2):
    for i in list1:
        for j in list2:
            if(circlecollision(i,j)):
                i.velocity = 0
                j.velocity = 0

def circletowall(list, walllist):
    for i in list:
        for wall in walllist:
            if(wall.state == 0):
                if(abs(i.y - wall.y) <= i.xlen and abs(i.z - wall.z)<= wall.height and abs(i.x - wall.x) <= wall.width):
                    i.velocity = -i.velocity
                    i.a = -i.a
                    i.angle1 = i.angle1-180
                    i.changenorm()
            elif(wall.state == 1):
                if(abs(i.x - wall.x) <= i.xlen and abs(i.y - wall.y)<= wall.height and abs(i.z - wall.z) <= wall.width):
                    i.angle2 = 180-i.angle2
                    i.changenorm()
            elif(wall.state == 2):
                if(abs(i.z - wall.z) <= i.xlen and abs(i.y - wall.y)<= wall.height and abs(i.z - wall.z) <= wall.width):
                    i.angle2 = 180 - i.angle2
                    i.changenorm()
                    
#####################################################################################################

# 움직임과 렌더 적용
def listmove1(objlist,df):
    for i in objlist:
         i.move(df)

def listrender1(objlist):
    for i in objlist:
        renderobj(i)

def listrender2(objlist):
    for i in objlist:
        renderobj2(i)

def listrender3(objlist):
    for i in objlist:
        renderobj3(i)

#################################################################################################


# 배고픔이 -10으로 되면 사라짐
def listhungry(objlist,pos):
    for i in objlist:
        if(i.hungry <= -10):
            objlist.remove(i)
        i.checkhungry(pos)
