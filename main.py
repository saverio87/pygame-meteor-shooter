import pygame, sys, random



class Spaceship(pygame.sprite.Sprite):

    def __init__(self,path,xpos,ypos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = (xpos,ypos))
        self.shield_surface = pygame.image.load('assets/shield.png')
        self.health = 5

    def constrain_screen(self):
        if self.rect.right >= 1280:
            self.rect.right = 1280

        if self.rect.left <= 0:
            self.rect.left = 0

    def display_health(self):
        for index, shield in enumerate(range(self.health)):
            screen.blit(self.shield_surface,(1200 - (index * 40),40))

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.constrain_screen()
        self.display_health()

    def collision_damage(self, damage_amount):
        self.health -= damage_amount
    
        

class Meteor(pygame.sprite.Sprite):

    def __init__(self,path,xpos,ypos,xspeed,yspeed):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = (xpos,ypos))

        self.xspeed = xspeed
        self.yspeed = yspeed

    def update(self):
        self.rect.center = (self.rect.centerx+self.xspeed, self.rect.centery + self.yspeed)

        if self.rect.centery > 780:
            self.kill()


class Laser(pygame.sprite.Sprite):
    
    def __init__(self,path,pos,speed):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = pos)

        self.speed = speed
        self.pos = pos
        
    def update(self):

        self.rect.centery -= self.speed

        if self.rect.centery < 0:
            self.kill()

    def dissolve(self):
        self.kill()

        

pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
game_font = pygame.font.Font('assets/LazenbyCompSmooth.ttf',100)
game_font2 = pygame.font.Font('assets/LazenbyCompSmooth.ttf',20)
score = 0


pygame.mouse.set_visible(False)

# Create Spaceship instance and its group

spaceship = Spaceship('assets/spaceship.png',640, 500)
spaceship_group = pygame.sprite.GroupSingle()
spaceship_group.add(spaceship)

# Create Meteor group

meteor_group = pygame.sprite.Group()

# Create Laser group

laser_group =pygame.sprite.Group()

# Set timer and user event

METEOR_EVENT = pygame.USEREVENT
pygame.time.set_timer(METEOR_EVENT,100)



def init_spaceship():
    
    global screen, spaceship_group
    
    spaceship_group.draw(screen)
    spaceship_group.update()

def check_spaceship_collision():
    
    global spaceship_group, meteor_group
    
    if pygame.sprite.spritecollide(spaceship_group.sprite, meteor_group, True):
        spaceship_group.sprite.collision_damage(1)

def spawn_meteor():
    
    global meteor_group

    path = random.choice(('assets/Meteor1.png','assets/Meteor2.png','assets/Meteor3.png'))
    xpos = random.randrange(0,1280)
    ypos = random.randrange(-500,-50)
    xspeed = random.randrange(-1,1)
    yspeed = random.randrange(3,8)
    meteor = Meteor(path, xpos, ypos, xspeed, yspeed)
    meteor_group.add(meteor)

def fire_meteor():

    global screen, meteor_group
    meteor_group.draw(screen)
    meteor_group.update()

def spawn_laser(position):

    global laser_group

    path = 'assets/laser.png'
    speed = 10
    laser = Laser(path, position, speed)
    laser_group.add(laser)

def fire_laser():
    
    global laser_group
    
    laser_group.draw(screen)
    laser_group.update()

def check_laser_collision():

    global laser_group

    for laser in laser_group:
        # dokill is set to True, meaning the meteor instance gets automatically destroyed
        if pygame.sprite.spritecollide(laser, meteor_group, True):
            laser.dissolve()
            # Because otherwise it would keep going and destroy other meteors



def  main_game():

    score_surface = game_font2.render('Score:',True, (255,255,255))
    score_rect = score_surface.get_rect(topleft = (20,20))
    score_surface2 = game_font2.render(f'{score}',True, (255,255,255))
    score_rect2 = score_surface2.get_rect(topleft = (20,50))
    screen.blit(score_surface, score_rect)
    screen.blit(score_surface2, score_rect2)

    
     # We want the laser to be render first (its origin position is the mouse click pos, that is the center of the spaceship)
    fire_laser()
    init_spaceship()
    fire_meteor()

    # Check for collision

    check_spaceship_collision()
    check_laser_collision()

    return 1
    # Every frame one point is accrued, which gets then added to the score

def end_game():

    text_surface = game_font.render(f"Game over",True, (255,255,255))
    text_rect = text_surface.get_rect(center = (640,340))
    screen.blit(text_surface, text_rect)

    endgame_score = game_font2.render(f"Score: {score}",True, (255,255,255))
    endgame_score_rect = endgame_score.get_rect(center = (640,420))
    screen.blit(endgame_score, endgame_score_rect)
    


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Every time the user event METEOR_EVENT is triggered (which is every 1/10 of a second), spawn a meteor
        if event.type == METEOR_EVENT:
            spawn_meteor()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # We pass in the event position, which is the position where the mouse click gets triggered
            spawn_laser(event.pos)

        if event.type == pygame.MOUSEBUTTONDOWN and spaceship_group.sprite.health < 0:

            meteor_group.empty()
            spaceship_group.sprite.health = 5
            score = 0
            

    screen.fill((42,45,51))

    if spaceship_group.sprite.health >= 0:
        score = score + main_game()
    else:
        end_game()
        
    
    pygame.display.update()
    clock.tick(120)


