from pygame import*
from random import randint

init()
mixer.init()
font.init()
WIDTH = 700
HEIGHT = 500
window = display.set_mode((WIDTH,HEIGHT))
display.set_caption("Шутер")

clock = time.Clock()
counter = 30
mixer.music.load("space.ogg")
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
vampirism_text = font1.render("Вампіризм активовано!", True, (255,0,0))
class GameSprite(sprite.Sprite):
    def __init__(self,image_name,x,y,width,height):
        super().__init__()
        self.image = transform.scale(image.load(image_name), (width,height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
    def draw(self):
        window.blit(self.image,self.rect)

class Player(GameSprite):
    def __init__(self):
        super().__init__("rocket.png", 10,400,60,100)
        self.speed = 5
        self.hp = 100
        self.points = 0
        self.bullets = sprite.Group()

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
        if keys[K_SPACE]:
            self.fire()

    def vampirism(self):
        self.hp += 25


class Ufo(GameSprite):
    def __init__(self):
        rand_x = randint(0,WIDTH-75)
        rand_y = randint(-200,-100)
        super().__init__("ufo.png",rand_x,rand_y,75,75)
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
        super().__init__("asteroid.png",rand_x,rand_y,75,75)
        self.sp = randint(3,5)
        self.hp = 100
    def update(self):
        self.rect.y += self.sp
        if self.rect.y > HEIGHT + self.height:
            self.rect.x = randint(0,WIDTH-75)
            self.rect.y = randint(-200,-100)


class Bullet(GameSprite):
    def __init__(self,x,y):
        super().__init__("bullet.png ", x,y,15,20)
        self.speed = 3
    
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0 - self.height:
            self.kill()

   



font1 = font.SysFont("Impact", 50)
bg_image = transform.scale(image.load("galaxy.jpg"), (WIDTH, HEIGHT))

rocket = Player()
ufos = sprite.Group()
asteroids = sprite.Group()

points_text = font2.render("Points:" + str(rocket.points), True, (255,255,255))
hp_text = font2.render("Life:" + str(rocket.hp), True, (255,255,255))
result = font1.render("Ви програли!", True, (255,0,0))
result = font1.render("Ви пeремогли!", True, (255,0,0))
for i in range(0):
    ufo = Ufo()
    ufos.add(ufo)
for a in range(4):
    asteroid = Asteroid()
    asteroids.add(asteroid)


run = True
finish = False
FPS = 60
rand_ufo = 500
while run:
    window.blit(bg_image,(0,0))
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == timer_event:
            counter-=1
            timerk = timer_font.render("Time:" + str(counter), True, (255,255,255))
            if counter == 0:
                finish = True
                result = font1.render("Ви програли!", True, (255,0,0))
           
    if not finish:
        rocket.update()
        rocket.bullets.update()
        ufos.update()
        asteroids.update()
        rocket.bullets.update()
        rocket.draw()
        ufos.draw(window)
        asteroids.draw(window)
        rocket.bullets.draw(window)
        window.blit(points_text,(30,10))
        window.blit(hp_text,(600,10))
        window.blit(timerk,(10,440))
        collides = sprite.groupcollide(ufos,rocket.bullets, True, True)
        collide_list = sprite.spritecollide(rocket, ufos,True)
        collide_list_2 = sprite.spritecollide(rocket, asteroids,True)
        rand_num = randint(0,rand_ufo)
        for i  in collides:
            rocket.points += 1
            points_text = font2.render("Points:" + str(rocket.points), True, (255,255,255))
            if rocket.hp < 100:
                if rocket.points >= 10:
                    rocket.vampirism()
                    window.blit(vampirism_text,(200,200))   
                    hp_text = font2.render("Life:" + str(rocket.hp), True, (255,255,255))
        if rand_num == 5:
            ufo = Ufo()
            ufos.add(ufo)
            if rand_ufo >= 50:
                rand_ufo -=20

        for kick in collide_list:
            rocket.hp -= 25
            hp_text = font2.render("Life:" + str(rocket.hp), True, (255,255,255))
            

            
        for kick in collide_list_2:
            rocket.hp -= 25
            hp_text = font2.render("Life:" + str(rocket.hp), True, (255,255,255))


        if rocket.hp <= 0:
            finish = True
            result = font1.render("Ви програли!", True, (255,0,0))

        if rocket.points == 20:
            finish = True
            result = font1.render("Ви перемогли", True, (255,0,0))
            

    else:
        window.blit(result, (200,200))       
    display.update()
    clock.tick(FPS)



