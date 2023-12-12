from objloader import *
import math

class Moveobj(OBJ):
    def __init__(self,filename,x=0,y=0,z=0,velocity = 0,a = 0,angle1 = 0,angle2 = 0,mass = 1,xlen = 1,ylen = 1,zlen = 1):
        super().__init__(filename,False)
        self.x = x
        self.y = y
        self.z = z

        self.velocity = velocity
        self.angle1 = angle1
        self.angle2 = angle2

        # 로컬 값 구하기
        self.xnorm = [math.cos(math.radians(angle1))*math.cos(math.radians(angle2)),math.sin(math.radians(angle2)),-math.sin(math.radians(angle1))*math.cos(math.radians(angle2))]
        self.znorm = [-self.xnorm[2]/math.sqrt(self.xnorm[2]*self.xnorm[2] + self.xnorm[0]*self.xnorm[0]),0,self.xnorm[0]/math.sqrt(self.xnorm[2]*self.xnorm[2] + self.xnorm[0]*self.xnorm[0])]
        self.ynorm = [-self.xnorm[1]*self.znorm[2],self.znorm[2]*self.xnorm[0] - self.xnorm[2]*self.znorm[0],
                      self.znorm[0]*self.xnorm[1]]

        self.normlist = [self.xnorm,self.ynorm,self.znorm]

        # 로컬 x 축을 따라 이동
        self.vx = velocity*self.xnorm[0]
        self.vz = velocity*self.xnorm[2]
        self.vy = velocity*self.ynorm[1]

        self.g = 0.0

#        self.colrotation = [0,0,0]; self.rcheck = False

        self.a = a

        # 충돌 박스의 범위
        self.xlen = xlen
        self.ylen = ylen
        self.zlen = zlen

        self.maxlen = math.sqrt(xlen*xlen + ylen*ylen + zlen*zlen)

        # 충돌 박스의 대각선 벡터 4개
        self.maxvector = [[(self.xnorm[0]+self.ynorm[0]+self.znorm[0])/math.sqrt(3), (self.xnorm[1]+self.ynorm[1]+self.znorm[1])/math.sqrt(3), (self.xnorm[2]+self.ynorm[2]+self.znorm[2])/math.sqrt(3)],
                          [(self.xnorm[0]-self.ynorm[0]-self.znorm[0])/math.sqrt(3), (self.xnorm[1]-self.ynorm[1]-self.znorm[1])/math.sqrt(3), (self.xnorm[2]-self.ynorm[2]-self.znorm[2])/math.sqrt(3)],
                          [(self.xnorm[0]+self.ynorm[0]-self.znorm[0])/math.sqrt(3), (self.xnorm[1]+self.ynorm[1]-self.znorm[1])/math.sqrt(3), (self.xnorm[2]+self.ynorm[2]-self.znorm[2])/math.sqrt(3)],
                          [(self.xnorm[0]-self.ynorm[0]+self.znorm[0])/math.sqrt(3), (self.xnorm[1]-self.ynorm[1]+self.znorm[1])/math.sqrt(3), (self.xnorm[2]-self.ynorm[2]+self.znorm[2])/math.sqrt(3)]]

#        self.boxvertex1 = []; self.boxvertex2 = []        

        self.mass = mass
        

    # 속도와 가속도에 따라 이동
    def move(self,df):
        self.velocity += self.a*df

        self.vx = self.velocity*self.xnorm[0]
        self.vz = self.velocity*self.xnorm[2] 
        self.vy = self.velocity*self.xnorm[1]
        
        self.x += self.vx*df*0.01
        self.y += self.vy*df*0.01 - self.g
        self.z += self.vz*df*0.01

        if(abs(self.x) > 50 or abs(self.y) > 50 or abs(self.z) >50):
            self.velocity = 0; self.a = 0


    # 중력
    def gravity(self,df):
        self.g += 0.0001*df

    # 각도에 맞춰 로컬 벡터들 변환
    def changenorm(self):
        self.xnorm = [math.cos(math.radians(self.angle1))*math.cos(math.radians(self.angle2)),math.sin(math.radians(self.angle2)),-math.sin(math.radians(self.angle1))*math.cos(math.radians(self.angle2))]
        self.znorm = [-self.xnorm[2]/math.sqrt(self.xnorm[2]*self.xnorm[2] + self.xnorm[0]*self.xnorm[0]),0,self.xnorm[0]/math.sqrt(self.xnorm[2]*self.xnorm[2] + self.xnorm[0]*self.xnorm[0])]
        self.ynorm = [-self.xnorm[1]*self.znorm[2],self.znorm[2]*self.xnorm[0] - self.xnorm[2]*self.znorm[0],
                      self.znorm[0]*self.xnorm[1]]
        
        self.normlist = [self.xnorm,self.ynorm,self.znorm]

        self.maxvector = [[(self.xnorm[0]+self.ynorm[0]+self.znorm[0])/math.sqrt(3), (self.xnorm[1]+self.ynorm[1]+self.znorm[1])/math.sqrt(3), (self.xnorm[2]+self.ynorm[2]+self.znorm[2])/math.sqrt(3)],
                          [(self.xnorm[0]-self.ynorm[0]-self.znorm[0])/math.sqrt(3), (self.xnorm[1]-self.ynorm[1]-self.znorm[1])/math.sqrt(3), (self.xnorm[2]-self.ynorm[2]-self.znorm[2])/math.sqrt(3)],
                          [(self.xnorm[0]+self.ynorm[0]-self.znorm[0])/math.sqrt(3), (self.xnorm[1]+self.ynorm[1]-self.znorm[1])/math.sqrt(3), (self.xnorm[2]+self.ynorm[2]-self.znorm[2])/math.sqrt(3)],
                          [(self.xnorm[0]-self.ynorm[0]+self.znorm[0])/math.sqrt(3), (self.xnorm[1]-self.ynorm[1]+self.znorm[1])/math.sqrt(3), (self.xnorm[2]-self.ynorm[2]+self.znorm[2])/math.sqrt(3)]]
        
    # 힘에 따라 가속도 주기
    def makeforce(self,force):
        self.a = force*self.mass*0.01

# 벽
class Wall(OBJ):
    def __init__(self,filename="3dmodel/wall.obj",x=0,y=0,z=0,state = 0,width = 10, height = 10):
        super().__init__(filename,False)
        self.x = x
        self.y = y
        self.z = z

        #벽의 종류
        self.state = state

        if(state == 0):
            self.norm = [0,1,0]
        elif(state == 1):
            self.norm = [1,0,0]
        elif(state == 2):
            self.norm = [0,0,1]
        
        self.width = width
        self.height = height


# 오일러 회전을 이용한 것
class Moveobj2(OBJ):
    def __init__(self,filename="3dmodel/box.obj",x=0,y=0,z=0,velocity=0,w=0,a=0,wa=0,anglex=0,angley=0,anglez=0,mass=0,f=0,vector = [1,0,0], xlen = 1, ylen= 1, zlen=1):
        super().__init__(filename,False)
        self.x = x; self.y = y; self.z = z
        self.velocity = velocity; self.w = w; self.a = a; self.wa = wa
        self.anglex = anglex; self.angley = angley; self.anglez = anglez
        self.mass = mass; self.f = f; self.vector = vector
        self.xlen = xlen; self.ylen = ylen; self.zlen = zlen

        self.vx = 0; self.vy = 0; self.vz = 0
        
        self.xnorm = [1,0,0]
        self.ynorm = []
        self.znorm = []

        self.maxlen = math.sqrt(xlen*xlen + ylen*ylen + zlen*zlen)

        # 로컬 벡터 구하기
        self.makexnorm()
        
        # 대각선 벡터 구하기
        self.maxvector = [[(self.xnorm[0]+self.ynorm[0]+self.znorm[0])/math.sqrt(3), (self.xnorm[1]+self.ynorm[1]+self.znorm[1])/math.sqrt(3), (self.xnorm[2]+self.ynorm[2]+self.znorm[2])/math.sqrt(3)],
                          [(self.xnorm[0]-self.ynorm[0]-self.znorm[0])/math.sqrt(3), (self.xnorm[1]-self.ynorm[1]-self.znorm[1])/math.sqrt(3), (self.xnorm[2]-self.ynorm[2]-self.znorm[2])/math.sqrt(3)],
                          [(self.xnorm[0]+self.ynorm[0]-self.znorm[0])/math.sqrt(3), (self.xnorm[1]+self.ynorm[1]-self.znorm[1])/math.sqrt(3), (self.xnorm[2]+self.ynorm[2]-self.znorm[2])/math.sqrt(3)],
                          [(self.xnorm[0]-self.ynorm[0]+self.znorm[0])/math.sqrt(3), (self.xnorm[1]-self.ynorm[1]+self.znorm[1])/math.sqrt(3), (self.xnorm[2]-self.ynorm[2]+self.znorm[2])/math.sqrt(3)]]

        self.g = 0

    # 오일러 회전에 따른 로컬 벡터 구하기
    def makexnorm(self):
        ttomatrix = [[math.cos(math.radians(self.anglez))*math.cos(math.radians(self.angley)),
                     math.sin(math.radians(self.anglex))*math.sin(math.radians(self.angley))*math.cos(math.radians(self.anglez)) - math.sin(math.radians(self.anglez))*math.cos(math.radians(self.anglex)),
                     math.sin(math.radians(self.anglex))*math.sin(math.radians(self.anglez)) + math.cos(math.radians(self.anglex))*math.cos(math.radians(self.anglez))*math.sin(math.radians(self.angley))],

                     [math.sin(math.radians(self.anglez))*math.cos(math.radians(self.angley)),
                      math.cos(math.radians(self.anglex))*math.cos(math.radians(self.anglez)) + math.sin(math.radians(self.anglex))*math.sin(math.radians(self.angley))*math.sin(math.radians(self.anglez)),
                      math.cos(math.radians(self.anglex))*math.sin(math.radians(self.angley))*math.sin(math.radians(self.anglez))-math.sin(math.radians(self.anglex))*math.cos(math.radians(self.anglez))],

                      [-math.sin(math.radians(self.angley)),
                       math.sin(math.radians(self.anglex))*math.cos(math.radians(self.angley)),
                      math.cos(math.radians(self.anglex))*math.cos(math.radians(self.angley))]]
        
        self.xnorm = [self.xnorm[0]*ttomatrix[0][0] + self.xnorm[1]*ttomatrix[0][1] +self.xnorm[2]*ttomatrix[0][2],
                      (self.xnorm[0]*ttomatrix[1][0] + self.xnorm[1]*ttomatrix[1][1] +self.xnorm[2]*ttomatrix[1][2]),
                      (self.xnorm[0]*ttomatrix[2][0] + self.xnorm[1]*ttomatrix[2][1] +self.xnorm[2]*ttomatrix[2][2])]
        
        self.znorm = [-self.xnorm[2]/math.sqrt(self.xnorm[2]*self.xnorm[2] + self.xnorm[0]*self.xnorm[0]),0,self.xnorm[0]/math.sqrt(self.xnorm[2]*self.xnorm[2] + self.xnorm[0]*self.xnorm[0])]

        self.ynorm = [-self.xnorm[1]*self.znorm[2],self.znorm[2]*self.xnorm[0] - self.xnorm[2]*self.znorm[0],
                      self.znorm[0]*self.xnorm[1]]
        
        self.maxvector = [[(self.xnorm[0]+self.ynorm[0]+self.znorm[0])/math.sqrt(3), (self.xnorm[1]+self.ynorm[1]+self.znorm[1])/math.sqrt(3), (self.xnorm[2]+self.ynorm[2]+self.znorm[2])/math.sqrt(3)],
                          [(self.xnorm[0]-self.ynorm[0]-self.znorm[0])/math.sqrt(3), (self.xnorm[1]-self.ynorm[1]-self.znorm[1])/math.sqrt(3), (self.xnorm[2]-self.ynorm[2]-self.znorm[2])/math.sqrt(3)],
                          [(self.xnorm[0]+self.ynorm[0]-self.znorm[0])/math.sqrt(3), (self.xnorm[1]+self.ynorm[1]-self.znorm[1])/math.sqrt(3), (self.xnorm[2]+self.ynorm[2]-self.znorm[2])/math.sqrt(3)],
                          [(self.xnorm[0]-self.ynorm[0]+self.znorm[0])/math.sqrt(3), (self.xnorm[1]-self.ynorm[1]+self.znorm[1])/math.sqrt(3), (self.xnorm[2]-self.ynorm[2]+self.znorm[2])/math.sqrt(3)]]

        

    # 이동
    def move(self,df):
        self.velocity += self.a*df

        self.vx = self.velocity*self.vector[0]
        self.vz = self.velocity*self.vector[2] 
        self.vy = self.velocity*self.vector[1]
        
        self.x += self.vx*df*0.01
        self.y += self.vy*df*0.01 - self.g
        self.z += self.vz*df*0.01


    def gravity(self,df):
        self.g += 0.0001*df

# 간단한 인공지능을 가진 물체
class Monster(Moveobj2):
    def __init__(self,filename = "3dmodel/Ball.obj",life = 10, hungry = 10):
        super().__init__(filename=filename)
        self.hungry = hungry
        self.life = life
    

    # 일정 범위에 들어오거나 배고파 지면 playerpos로 이동
    def checkhungry(self,playerpos):
        dfx = self.x + playerpos[0]; dfy = self.y + playerpos[1]; dfz = self.z - playerpos[2]
        len = math.sqrt(dfx*dfx + dfy*dfy + dfz*dfz)
        if(len == 0):
            len = 1
        if(self.hungry <= 0):
            self.velocity = 0.5
            self.vector = [-dfx/len, -dfy/len,-dfz/len]
            if(len <= 1):
                self.hungry = 10
        elif(len <= 20):
            self.velocity = 0.5
            self.vector = [-dfx/len, -dfy/len, -dfz/len]
            if(len <= 1):
                self.hungry = 10
        else:
            self.velocity = 0
            

    