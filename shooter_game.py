from pygame import*
from random import randint

init()
mixer.init()
font.init()
WIDTH = 700
HEIGHT = 500
window = display.set_mode((WIDTH,HEIGHT))
display.set_caption("Shooter")
clock = time.Clock()
counter = 0
RED = (255,0,0)

mixer.music.load("through space.ogg")
mixer.music.set_volume(0.5)
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg") 

timer_event = USEREVENT+1
time = time.set_timer(timer_event, 1000)

font1 = font.SysFont("Impact", 50)
font2 = font.SysFont("Impact",30)
timer_font = font.SysFont("Impact",40)
timerk = timer_font.render("Time:" + str(counter), True, (255,255,255))
result = font1.render("Ви програли!", True, (255,0,0))
result = font1.render("Ви пeремогли!", True, (255,0,0))
font3 = font.SysFont("Impact",25)
vampirism_text = font3.render("Вампіризм активовано", True, (255,255,255))
shield_text = font3.render("Щит активовано", True, (255,255,255))

player_img = image.load("rocket.png")
ufo_img = image.load("ufo_2.png")
bullet_img = image.load("bullet.png")
shield_img = image.load("shield.png")
laser_img = image.load("laser.png")
asteroid_img = image.load("asteroid.png")

class GameSprite(sprite.Sprite):
    def __init__(self,img,x,y,width,height):
        super().__init__()
        self.image = transform.scale(img, (width,height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
    def draw(self):
        window.blit(self.image,self.rect)

class Player(GameSprite):
    def __init__(self):
        super().__init__(player_img, 10,400,60,100)
        self.speed = 5
        self.hp = 100
        self.points = 0
        self.bullets = sprite.Group()
        self.v = False
        self.shield_is = False
        

    def fire(self):
        new_bullet = Bullet(self.rect.centerx,self.rect.y)
        self.bullets.add(new_bullet)
        fire_sound.play()

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x>0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x<WIDTH - self.width:
            self.rect.x += self.speed
        
    


class Ufo(GameSprite):
    def __init__(self):
        rand_x = randint(0,WIDTH-75)
        rand_y = randint(-200,-100)
        super().__init__(ufo_img,rand_x,rand_y,75,75)
        self.sp = randint(3,5)
        self.hp = 100
    def update(self):
        self.rect.y += self.sp
        if self.rect.y > HEIGHT + self.height:
            self.rect.x = randint(0,WIDTH-75)
            self.rect.y = randint(-200,-100)
            
class Asteroid(GameSprite):
    def __init__(self):
        rand_x = randint(0,WIDTH-75)
        rand_y = randint(-200,-100)
        super().__init__(asteroid_img,rand_x,rand_y,75,75)
        self.sp = randint(3,5)
        self.hp = 100
    def update(self):
        self.rect.y += self.sp
        if self.rect.y > HEIGHT + self.height:
            self.rect.x = randint(0,WIDTH-75)
            self.rect.y = randint(-200,-100)


class Bullet(GameSprite):

    def __init__(self,x,y):
        super().__init__(bullet_img, x,y,15,20)
        self.speed = 7
    
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0 - self.height:
            self.kill()


class Shield(GameSprite):

    def __init__(self):
        rand_x = randint(0,WIDTH-75)
        rand_y = randint(-200,-100)
        super().__init__(shield_img,rand_x,rand_y,75,75)
        self.sp = randint(3,5)

    def update(self):
        self.rect.y += self.sp
        if self.rect.y > HEIGHT + self.height:
            self.kill()

class Vampirism(GameSprite):

    def __init__(self):
        rand_x = randint(0,WIDTH-75)
        rand_y = randint(-200,-100)
        super().__init__(laser_img,rand_x,rand_y,75,75)
        self.sp = randint(3,5)

    def update(self):
        self.rect.y += self.sp
        if self.rect.y > HEIGHT + self.height:
            self.kill()


    



font1 = font.SysFont("Impact", 50)

bg_image = transform.scale(image.load("space_2.png"), (WIDTH, HEIGHT))

restart = GameSprite("restart.png", 250,250,180,100)

bg_y1 = 0 
bg_y2 = -HEIGHT
rocket = Player()

ufos = sprite.Group()
asteroids = sprite.Group()
shields = sprite.Group()
vampirism_bullets = sprite.Group()

points_text = font2.render("Points:" + str(rocket.points), True, (255,255,255))
hp_text = font2.render("Life:" + str(rocket.hp), True, (255,255,255))
result = font1.render("Ви програли!", True, (255,0,0))
result = font1.render("Ви пeремогли!", True, (255,0,0))

for a in range(4):
    asteroid = Asteroid()
    asteroids.add(asteroid)


run = True
finish = False
FPS = 60
rand_ufo = 500
while run:
    window.blit(bg_image,(0,bg_y1))
    window.blit(bg_image,(0,bg_y2))

    bg_y1 += 1
    bg_y2 += 1

    if bg_y1 >= HEIGHT:
        bg_y1 = -HEIGHT

    if bg_y2 >= HEIGHT:
        bg_y2 = -HEIGHT

    for e in event.get():
        if e.type == QUIT:
            run = False

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()

        if e.type == timer_event:
            counter+=1
            timerk = timer_font.render("Time:" + str(counter), True, (255,255,255))
            if counter == 60:
                finish = True
                result = font1.render("Ви програли!", True, (255,0,0))
            if counter == 1:   
                for i in range(5):
                    ufo = Ufo()
                    ufos.add(ufo)
            if counter == 6:
                for i in range(5):
                    ufo = Ufo()
                    ufos.add(ufo)
            if counter == 14:
                for i in range(10):
                    ufo = Ufo()
                    ufos.add(ufo)
            if counter == 20:
                for i in range(15):
                    ufo = Ufo()
                    ufos.add(ufo)
        

    if not finish:
        rocket.update()
        rocket.bullets.update()
        ufos.update()
        asteroids.update()
        shields.update()
        vampirism_bullets.update()
        rand_num1 = randint(0,500)
        rand_num2 = randint(0,500)
        if rand_num1 == 25:
            shields.add(Shield())
        if rand_num2 == 25:
            vampirism_bullets.add(Vampirism())
        shields.draw(window)
        vampirism_bullets.draw(window)
        rocket.draw()
        ufos.draw(window)
        asteroids.draw(window)
        rocket.bullets.draw(window)
        window.blit(points_text,(30,10))
        window.blit(hp_text,(600,10))
        window.blit(timerk,(10,440))

        if rocket.v == True:
            window.blit(vampirism_text,(430,40))
        if rocket.shield_is == True:
            window.blit(shield_text,(500,60))

        collides = sprite.groupcollide(ufos,rocket.bullets,True,True)
        collide_list = sprite.spritecollide(rocket, ufos,False)
        collide_list_2 = sprite.spritecollide(rocket, asteroids,False)
        collide_list_3 = sprite.spritecollide(rocket, shields,True)
        collidelist_4 = sprite.spritecollide(rocket, vampirism_bullets,True)



        for i  in collides:
            rocket.points += 1
            points_text = font2.render("Points:" + str(rocket.points), True, (255,255,255))
            if rocket.v == True:
                rocket.hp += 25
                hp_text = font2.render("Life:" + str(rocket.hp), True, (255,255,255))
                vampirism_text = font3.render("Вампіризм активовано", True, (255,255,255))
                if rocket.hp <= 100:
                    rocket.v = False
                    hp_text = font2.render("Life:" + str(rocket.hp), True, (255,255,255))

                

        

        for kick in collide_list:
            if not rocket.shield_is and not rocket.v:
                rocket.hp -= 25
                hp_text = font2.render("Life:" + str(rocket.hp), True, (255,255,255))
                kick.rect.x = randint(0,WIDTH-75)
                kick.rect.y = randint(-200,-100)
            else:
                rocket.shield_is = False
                rocket.v = False

        
        for kick in collide_list_2:
            if not rocket.shield_is and not rocket.v:
                rocket.hp -= 25
                hp_text = font2.render("Life:" + str(rocket.hp), True, (255,255,255))
                kick.rect.x = randint(0,WIDTH-75)
                kick.rect.y = randint(-200,-100)
            else:
                rocket.shield_is = False
                rocket.v = False   


        for kick in collide_list_3:
            rocket.shield_is = True

        

        for kick in collidelist_4:
            rocket.v = True
            hp_text = font2.render("Life:" + str(rocket.hp), True, (255,255,255))
            


        if rocket.hp <= 0:
            finish = True
            result = font1.render("Ви програли!", True, (255,0,0))
            restart.draw()

        if rocket.points == 30:
            finish = True
            result = font1.render("Ви перемогли", True, (255,0,0))
            restart.draw()
            

    else:
        window.blit(result, (200,200))       
    display.update()
    clock.tick(FPS)



