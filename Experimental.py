import pygame
from pygame.locals import *
from random import randint
from pygame import mixer
pygame.init()
mixer.init()

# Game properties and dimensions
SIZE = 800, 650
width, height = SIZE
pygame.display.set_caption("OOP PROJECT")
screen = pygame.display.set_mode(SIZE)
bg_color = 'black'
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1000)
running = True

# Paddle dimensions
paddle_dimensions = 100, 10
p_height, p_width = paddle_dimensions
paddle_color = "white"


# Background Images
scroll = 850
ground = pygame.image.load("Assets/background/ground.png")
gWidth = ground.get_width()
ground = pygame.transform.scale(ground, (gWidth, 20))

bg_images = []
for i in range(1, 4):
    image = pygame.image.load(f"Assets/background/layers/bg-{i}.png").convert_alpha()
    bg_image = pygame.transform.scale(image, (800, 500))
    bg_images.append(bg_image)
bg_width = bg_images[0].get_width()

# SpriteSheets
ball_sheet = pygame.image.load("Assets/Ball/BallSheet.png").convert_alpha()

# Knight
character_1 = pygame.image.load("Assets/Character/Knight_1/Idle.png").convert_alpha()
character_1_atk = pygame.image.load("Assets/Character/Knight_1/Attack 1.png").convert_alpha()
character_1_d = pygame.image.load("Assets/Character/Knight_1/Dead.png").convert_alpha()
character_1_hrt = pygame.image.load("Assets/Character/Knight_1/Defend.png").convert_alpha()

# Samurai
character_2 = pygame.image.load("Assets/Character/Samurai_Commander/Idle.png").convert_alpha()
character_2_atk = pygame.image.load("Assets/Character/Samurai_Commander/attack_2.png").convert_alpha()
character_2_d = pygame.image.load("Assets/Character/Samurai_Commander/Dead.png").convert_alpha()
character_2_hrt = pygame.image.load("Assets/Character/Samurai_Commander/Protect.png").convert_alpha()

# Vampire

character_3 = pygame.image.load("Assets/Character/Vampire_Girl/Idle.png").convert_alpha()
character_3_atk = pygame.image.load("Assets/Character/Vampire_Girl/attack_4.png").convert_alpha()
character_3_d = pygame.image.load("Assets/Character/Vampire_Girl/Dead.png").convert_alpha()
character_3_hrt = pygame.image.load("Assets/Character/Vampire_Girl/Hurt.png").convert_alpha()

# Wander Magician

character_4 = pygame.image.load("Assets/Character/Wanderer Magican/Idle.png").convert_alpha()
character_4_atk = pygame.image.load("Assets/Character/Wanderer Magican/attack_2.png").convert_alpha()
character_4_d = pygame.image.load("Assets/Character/Wanderer Magican/Dead.png").convert_alpha()
character_4_hrt = pygame.image.load("Assets/Character/Wanderer Magican/Hurt.png").convert_alpha()

# Lightning Mage

character_5 = pygame.image.load("Assets/Character/Lightning Mage/Idle.png").convert_alpha()
character_5_atk = pygame.image.load("Assets/Character/Lightning Mage/attack_1.png").convert_alpha()
character_5_d = pygame.image.load("Assets/Character/Lightning Mage/Dead.png").convert_alpha()
character_5_hrt = pygame.image.load("Assets/Character/Lightning Mage/Hurt.png").convert_alpha()

# Kunoichi

character_6 = pygame.image.load("Assets/Character/Kunoichi/Idle.png").convert_alpha()
character_6_atk = pygame.image.load("Assets/Character/Kunoichi/attack_2.png").convert_alpha()
character_6_d = pygame.image.load("Assets/Character/Kunoichi/Dead.png").convert_alpha()
character_6_hrt = pygame.image.load("Assets/Character/Kunoichi/Hurt.png").convert_alpha()

# HUDscreen.blit(healthBar, (800 - 250, 550))

HUDBar = pygame.image.load("Assets/HUD/HUD_Bar.png").convert_alpha()
healthBar = pygame.image.load("Assets/HUD/health_bar.png").convert_alpha()
healthBar = pygame.transform.scale(healthBar, (250, 50))

# Classes
#Spritesheets kay tig kuha each image sa sprite sheet
class SpriteSheets():
    def __init__(self, image):
        self.image = image

    def getSprite(self, image_width, image_height, frame):
        frame_0 = pygame.Surface((image_width, image_height), pygame.SRCALPHA).convert_alpha()
        frame_0.blit(self.image, (0, 0), ((frame * image_width), 0, image_width, image_height))
        frame_0 = pygame.transform.scale(frame_0, (200, 200))
        return frame_0

    def getBallSprite(self, image_width, image_height, frame):
        frame_0 = pygame.Surface((image_width, image_height), pygame.SRCALPHA).convert_alpha()
        frame_0.blit(self.image, (0, 0), ((frame * image_width), 0, image_width, image_height))
        frame_0 = pygame.transform.scale(frame_0, (64, 64))
        return frame_0

#Player class kay tig store sa mga animation, niya naa siyay iyang healthBar na instance
class Player():
    def __init__(self, character, attack, hurt, death, health_content):
        self.avatar = character
        self.attack = attack
        self.hurt = hurt
        self.death = death
        self.isDead = False
        self.current_state = "idle"
        self.animations = {}
        self.health = HealthBar(*health_content)

    def populateAnimation(self, idle, attack, death, hurt):
        self.animations = {
            "idle": idle,
            "attack": attack,
            "death": death,
            "hurt": hurt
        }

class HealthBar():
    def __init__(self, x, y, w, h, max_HP):
        self.x = x
        self.y = y 
        self.w = w
        self.h = h
        self.hp = max_HP
        self.max_HP = max_HP

    def drawHP(self, surface):
        ratio = self.hp / self.max_HP
        pygame.draw.rect(surface, "Red", (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, "green", (self.x, self.y, ratio * self.w , self.h))

#same sa player class nag contain pd siya sa iyahang animations
class GameBall():
    def __init__(self, x, y, dx, dy, bh, bw, animation):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.bh = bh
        self.bw = bw
        self.og_x = x
        self.og_y = y
        self.frame = 0
        self.reset = False
        self.anim = animation
        self.ball_rect = pygame.Rect(self.x, self.y, self.bh, self.bw)

    def drawBall(self, Ball_animList):
        resizedBall = pygame.transform.scale(Ball_animList[self.frame],(34, 34))
        screen.blit(resizedBall, (self.x, self.y))
        self.x += self.dx
        self.y += self.dy
        animation_cooldown = 70
        current_time = pygame.time.get_ticks()
        if current_time - last_update >= animation_cooldown:
            self.frame = (self.frame + 1) % 6
        self.ball_rect = pygame.Rect(self.x, self.y, self.bh, self.bw)
    
    def resetBall(self):
        self.x = self.og_x
        self.y = self.og_y
        self.dy = 0
        self.dx = 0
        self.reset = True
    
    def launchBall(self):
        self.dx = 7
        self.dy = 7
        self.reset = False

#paddle na class niya gi gamit nato ang inheritance, Makita sa p1 p2 ug ai nga lahi ang ila movement
class Paddle():
    def __init__(self, width, height, x_pos, y_pos):
        self.paddle_width = width
        self.paddle_height = height
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.paddle_rect = pygame.Rect(self.x_pos, self.y_pos, self.paddle_width, self.paddle_height)

    def drawPaddle(self, surface):
        self.paddle_rect = pygame.Rect(self.x_pos, self.y_pos, self.paddle_width, self.paddle_height)
        pygame.draw.rect(surface, (255, 255, 255), self.paddle_rect)

class P1Paddle(Paddle):
    def __init__(self, width, height, x_pos, y_pos):
        super().__init__(width, height, x_pos, y_pos)

    def handleMovement(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            self.y_pos -= 7
        if key[pygame.K_s]:
            self.y_pos += 7

class P2Paddle(Paddle):
    def __init__(self, width, height, x_pos, y_pos):
        super().__init__(width, height, x_pos, y_pos)

    def handleMovement(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            self.y_pos -= 7
        if key[pygame.K_DOWN]:
            self.y_pos += 7

class AiPaddle(Paddle):
    def __init__(self, width, height, x_pos, y_pos):
        super().__init__(width, height, x_pos, y_pos)
        self.duration = 170
        self.move_duration = self.duration + 500
        self.move_cooldown = self.duration
        self.last_move_time = pygame.time.get_ticks()

    def handleMovement(self, Ball):
        offset = 35  
        current_time = pygame.time.get_ticks()
        move_speed = 7  
        if current_time - self.last_move_time >= self.move_duration:
            if current_time - self.last_move_time >= self.move_duration + self.move_cooldown:
                self.last_move_time = current_time
                self.move_duration = self.duration + randint(600, 1000)
                self.move_cooldown = self.duration
            else:
                return
        if self.y_pos > Ball.y - offset:
            self.y_pos -= move_speed
        if self.y_pos < Ball.y - offset:
            self.y_pos += move_speed

# SpriteSheet class instance

# ball
ball_x = 402
ball_y = 250
ball_rad = 10
ball_speed = 7
ball_dx = ball_speed
ball_dy = ball_speed

Ball_animation = SpriteSheets(ball_sheet)
Ball = GameBall(ball_x, ball_y, ball_dx, ball_dy, 30, 30, Ball_animation)

# Player class instance
P1_Health = [50, 560, 200, 25, 100]
P2_Health = [800 - 250, 560, 200, 25, 100]

# Functions

#ang logic sa ge unsa pag kuha ang sliding2 na background, parallax ang tawag sa effect
def drawBg():
    for x in range(12):
        speed = 1
        for i in bg_images:
            screen.blit(i, ((x * bg_width) - scroll * speed, 0))
            speed += 0.2

# tig manage sa physics sa bola, ug tig check if maka score ang player o wala
def handleBallPhysx():
    global ball_x, ball_y, ball_dx, ball_dy, scroll, frame_player_1, frame_player_2
    current_time = pygame.time.get_ticks()
    delay = 5000
    last_update = pygame.time.get_ticks()
    # Scroll logic
    if Ball.dx < 0:
        scroll -= 2
    if Ball.dx > 0:
        scroll += 2

    #--Kani colliderect kay built in function sa pygame na mo check sa collisions
    #--Sa duha ka rectangle, makita ninyo sa GameBall ug Paddle class na naa silay
    #--ilang kaugalingon na rects niya mao na ang ge gamit diri
    if NewAiPaddle.paddle_rect.colliderect(Ball.ball_rect):
        Ball.dx = -Ball.dx

    # Ball boundaries x
    #--sa kani kay if ang x gani sa ball or iya x axis na position kay mas dako pa kaysa width plus 100
    #--Pasabot ana kay nalapas na siya sa right side na border, niya ara makuhaan ang player 2 nga health
    #--niya ari pd nato ge usab ang state sa mga players, since ang sa player Class kay adto mn naka store
    #--ang mga animations nila, if maka score ang player 1 ma set siya to attack niya ang player 2 kay
    #--ma hurt. makita ra sa ubos ge unsa pag ilis sa animation gamit sa player.state
    if Ball.x >= width + 100:
        Ball.resetBall()
        Ball.dx = -Ball.dx
        Player_2.health.hp -= 20
        if Player_1.current_state != "death" and Player_2.current_state != "death":
            # sa kani ge check if wala sa usa kay patay, kay lain pd mag sigeg attack niya patay na ang kuntra
            frame_player_2 = 0
            frame_player_1 = 0
            Player_2.current_state = "hurt"
            Player_1.current_state = "attack"

    #same sa babaw pero sa player 2 na collision
    if newPaddle.paddle_rect.colliderect(Ball.ball_rect):
        Ball.dx = -Ball.dx

    # same pd sa babaw pero para ni sa player 2 if maka score siya
    if Ball.x - ball_rad < - 100:
        Ball.resetBall()
        Ball.dx = -Ball.dx
        Player_1.health.hp -= 20
        if Player_2.current_state != "death" and Player_1.current_state != "death":
            frame_player_2 = 0
            frame_player_1 = 0
            Player_2.current_state = "attack"
            Player_1.current_state = "hurt"

    # Ball boundaries y
    # Bali ang y axis nga border, up and down
    if Ball.y + ball_rad >= height - 180:
        Ball.dy = -Ball.dy
    if Ball.y - ball_rad < 0 - 10:
        Ball.dy = -Ball.dy

#--depende sa dimension sa spritesheet gi kuha nato each frame, since ato mga characters 128 x 128
#--mao ang ato gi kuha niya, ang kanang gamit sa x kay iya position so if 0, naa sa pinaka left
#--atoang makuha sa sheet, niya mo increment by 128 each pa right every increment.
#--Niya ang ilhanan when mo stop kay ge manual nakog ihap ang frames, so mao na ako gi send sa function
#--arun makahibaw siya kanusa kutob ang sheet, Niya kuan pd diay ang each frames makuha kay ma store
#--sa usa ka list or array if sa C
def getAnimations(animation_list, length, player, action):
    for x in range(length):
        animation_list.append(getattr(player, action).getSprite(128, 128, x))

# Same sa sprite pero bola, niya since mas gamay mn ang dimensions sa bola, mao 16x16
def getBallAnimations(animation_list, length, ball):
    for x in range(length):
        animation_list.append(ball.anim.getBallSprite(16, 16, x))

# pag render sa kato sagbot na border
def drawGround():
    x = 0
    gWidth = ground.get_width()
    for x in range(27):
        screen.blit(ground, ((x * gWidth), 490))

#--kani siya kay para rani sa kanang mamatay ang character, gihimo ni nako kay wa ko kahibaw unsaon
#--pag hunong sa death animation, mag sige mn gd balik2, pero ang gamit ani kay once naay mamatay
#--iya ra hutdon ug display ang death animation niya if unsay last frame sa animation kay permanent na
def PlayAnim(count, frame):
    if frame == count-1:
        frame = count
        return 0
    elif frame < count:
        return 1

#--Character select, since wa may switch case ang python ako nalang ge ing ani
#--Ang gamit anang idle, attack ug uban kay mao na ang pila ka frames ang naa sa sheet
#--kato sa ge ingon nako ganiha na need ta makahibaw when ta mo stop ug kuha ug frames
def characterSelect(select, health):
    Player_idle = []
    Player_attack = []
    Player_dead = []
    Player_hurt = []
    if select == 1:
        Player_sheet = SpriteSheets(character_1)
        Player_attack_sheet = SpriteSheets(character_1_atk)
        Player_dead_sheet = SpriteSheets(character_1_d)
        Player_hurt_sheet = SpriteSheets(character_1_hrt)
        Idle = 4
        Attack = 5
        Dead = 6
        Hurt = 5
    elif select == 2:
        Player_sheet = SpriteSheets(character_2)
        Player_attack_sheet = SpriteSheets(character_2_atk)
        Player_dead_sheet = SpriteSheets(character_2_d)
        Player_hurt_sheet = SpriteSheets(character_2_hrt)
        Idle = 5
        Attack = 5
        Dead = 6
        Hurt = 2
    elif select == 3:
        Player_sheet = SpriteSheets(character_3)
        Player_attack_sheet = SpriteSheets(character_3_atk)
        Player_dead_sheet = SpriteSheets(character_3_d)
        Player_hurt_sheet = SpriteSheets(character_3_hrt)
        Idle = 5
        Attack = 5
        Dead = 10
        Hurt = 2
    elif select == 4:
        Player_sheet = SpriteSheets(character_4)
        Player_attack_sheet = SpriteSheets(character_4_atk)
        Player_dead_sheet = SpriteSheets(character_4_d)
        Player_hurt_sheet = SpriteSheets(character_4_hrt)
        Idle = 8
        Attack = 9
        Dead = 4
        Hurt = 4
    elif select == 5:
        Player_sheet = SpriteSheets(character_5)
        Player_attack_sheet = SpriteSheets(character_5_atk)
        Player_dead_sheet = SpriteSheets(character_5_d)
        Player_hurt_sheet = SpriteSheets(character_5_hrt)
        Idle = 7
        Attack = 10
        Dead = 5
        Hurt = 3
    elif select == 6:
        Player_sheet = SpriteSheets(character_6)
        Player_attack_sheet = SpriteSheets(character_6_atk)
        Player_dead_sheet = SpriteSheets(character_6_d)
        Player_hurt_sheet = SpriteSheets(character_6_hrt)
        Idle = 9
        Attack = 8
        Dead = 5
        Hurt = 2
    #--Ari kay naghimo tag player instance, niya ari pd ta nag call sa getAnimations na function
    NewPlayer = Player(Player_sheet, Player_attack_sheet, Player_hurt_sheet, Player_dead_sheet, health)
    getAnimations(Player_idle, Idle, NewPlayer, "avatar")
    getAnimations(Player_attack, Attack, NewPlayer, "attack")
    getAnimations(Player_dead, Dead, NewPlayer, "death")
    getAnimations(Player_hurt, Hurt, NewPlayer, "hurt")
    #--Ang kaning populate kay mao ni ang function para ma store nato sa player class ang mga animations
    #--Bali array na atoang gi send na ga contain each frames
    NewPlayer.populateAnimation(Player_idle, Player_attack, Player_dead, Player_hurt)
    return NewPlayer

#--ang gamit ani niya kay if maka score gani ga while loop ko arun bitaw dili ditso2 ang dagan sa bola,
#--so if maka score unless ma complete ang loop dili ra mag lihok ang bola
def resetBall():
    global reset, current
    if Ball.reset:
        if current >= reset:
            #--if ma complete na gani kay e launch ball na, kuan diay na naa na sa class na function
            #--igo rana niya ilisdan ang speed sa bola
            Ball.launchBall()
            current = 0
        else:
            current += 1

#--Main menu, mao ni ako ipabuhat ninyo, bali himo2 ramog buttons niya inyo lang pachuyan
#--ang sa karun kay black screen rana ug start button hahaha
def mainMenu():
    global Menu, running
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            Menu = False

        # Display the menu
        screen.fill((0, 0, 0))  # Black background
        font = pygame.font.Font(None, 36)
        start_text = font.render("Start", True, (255, 255, 255))
        start_rect = start_text.get_rect(center=(400, 300))
        screen.blit(start_text, start_rect)

        # Check for button click
        mouse_pos = pygame.mouse.get_pos()
        if start_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                Menu = False

        pygame.display.update()

#--mao ni tig handle sa animation, somakita nato currenet time - last_update, if greater than or equal kay
#--iya e increment ang frame_player so mao na ang rason ngano mo lihok ang mga characters
#--sa mainloop adto ninyo makita ge unsa siya pag gamit
def handleAnim():
    global last_update, frame_player_1, frame_player_2
    if Player_1.isDead == False and Player_1.health.hp <= 0:
        Player_1.isDead = True
        frame_player_1 = 0
        Player_1.current_state = "death"
    if Player_2.isDead == False and Player_2.health.hp <= 0:
        Player_2.isDead = True
        frame_player_2 = 0
        Player_2.current_state = "death"

    if current_time - last_update >= animation_cooldown:
        if not Player_1.isDead:
            frame_player_1 += 1
        else:
            frame_player_1 += PlayAnim(len(Player_1.animations[Player_1.current_state]), frame_player_1)
        if not Player_2.isDead:
            frame_player_2 += 1
        else:
            frame_player_2 += PlayAnim(len(Player_2.animations[Player_2.current_state]), frame_player_2)
        last_update = current_time

        if frame_player_1 >= len(Player_1.animations[Player_1.current_state]) and Player_1.current_state != "death":
                Player_1.current_state = "idle"
                frame_player_1 = 0
        if frame_player_2 >= len(Player_2.animations[Player_2.current_state]) and Player_2.current_state != "death":
                Player_2.current_state = "idle"
                frame_player_2 = 0

Menu = True
last_update = pygame.time.get_ticks()
# Ball animation properties

Ball_animList = []
BallLen = 6
getBallAnimations(Ball_animList, BallLen, Ball)

# Character Animation properties
animation_cooldown = 100

# Mainloop

frame_player_1 = 0
frame_player_2 = 0

Player_1 = characterSelect(randint(1, 6), P1_Health)
Player_2 = characterSelect(randint(1, 6), P2_Health)

newPaddle = AiPaddle(20, 100, 20, 250)
NewAiPaddle = AiPaddle(20, 100, 800- 40, 250)

reset = 100
current = 0


# mao ni siya ang mainloop, as long as di ta mupindog sa katong quit sa kanang mruag bar niya, magdagan rani
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    #--ang kaning while (menu), as long as true na iya e render permi ang Menu, niya if mo saka mo balik if mo click tas start,
    #--ang menu kay ma set to false bali mo start na ang duwa
    while (Menu):
         mainMenu()
    current_time = pygame.time.get_ticks()

    #Ari nato gipang call ang mga function

    resetBall()
    # Handle ball physics
    handleBallPhysx()
    # Handle animation
    handleAnim()
    #--Draw
    #--kaning current frame kay ato assignan sa list based sa unsay state sa character
    #--so if ma hurt mn gani, mausab jd ang animation sa player
    #--niya ang rason ari ge assign kay tungod mao ni ako gegamit didto sa ubos
    #--siguro pwede usbon pero unya nalang na hahaha
    P1_currentFrame = Player_1.animations[Player_1.current_state]
    P2_currentFrame = Player_2.animations[Player_2.current_state]
    screen.fill("#6E260E")
    #Background
    drawBg()
    newPaddle.drawPaddle(screen)
    newPaddle.handleMovement(Ball)
    # NewAiPaddle.drawPaddle(screen)
    # NewAiPaddle.handleMovement(Ball)
    NewAiPaddle.drawPaddle(screen)
    NewAiPaddle.handleMovement(Ball)
    #Health bars
    hud = pygame.transform.scale(HUDBar, (800, 150))
    screen.blit(hud, (0, 505))
    Player_1.health.drawHP(screen)
    screen.blit(healthBar, (50, 550)) 
    Player_2.health.drawHP(screen)
    screen.blit(healthBar, (800 - 250, 550))
    #Ball
    Ball.drawBall(Ball_animList)
    #Draw Sprites
    #--mao ni ako pasabot, ang screen,blit na function kay mao diay na ang built int func sa pygame
    #--na mo render sa image sulod sa array, niya if kahinumdom mo ang p1_currentFrame kay mao na ang ge assignan
    #--nato sa list na ga contain ug mga animations depende sa iya current state
    screen.blit(P1_currentFrame[frame_player_1], (280, 300))
    flipped_image = pygame.transform.flip(P2_currentFrame[frame_player_2], True, False)
    screen.blit(flipped_image, (800 - (280 + 164), 300))
    #Ground
    drawGround()
    #Update display
    pygame.display.update()
    clock.tick(80)
pygame.quit()