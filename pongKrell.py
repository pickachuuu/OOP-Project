import pygame
import random
from pygame.locals import *
from random import randint
from pygame import mixer
pygame.init()
mixer.init()

# Game properties

SIZE = 800, 650
width, height = SIZE
pygame.display.set_caption("PONG II")
screen = pygame.display.set_mode(SIZE)
bg_color = 'black'
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1000)
running = True
icon = pygame.image.load("Assets/Random/icon.png")
pygame.display.set_icon(icon)


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



menu_images = []
for i in range(0, 7):
    m_image = pygame.image.load(f"Assets/background/dark/frame_{i}_delay-1s.gif").convert_alpha()
    m_image = pygame.transform.scale(m_image, (800, 650))
    menu_images.append(m_image)
m_width = menu_images[0].get_width()

# Font

Game_font = pygame.font.Font("Assets/fonts/Robus-BWqOd.otf", 156)
Game_font_s = pygame.font.Font("Assets/fonts/Robus-BWqOd.otf", 76)

# SpriteSheets

# Ball

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

class SpriteSheets():
    def __init__(self, image):
        self.image = image

    def getSprite(self, image_width, image_height, frame):
        frame_0 = pygame.Surface((image_width, image_height), pygame.SRCALPHA).convert_alpha()
        frame_0.blit(self.image, (0, 0), ((frame * image_width), 0, image_width, image_height))
        frame_0 = pygame.transform.scale(frame_0, (200, 240))
        return frame_0

    def getBallSprite(self, image_width, image_height, frame):
        frame_0 = pygame.Surface((image_width, image_height), pygame.SRCALPHA).convert_alpha()
        frame_0.blit(self.image, (0, 0), ((frame * image_width), 0, image_width, image_height))
        frame_0 = pygame.transform.scale(frame_0, (64, 64))
        return frame_0
    
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
        self.dx = random.choice((7, -7))
        self.dy = random.choice((7, -7))
        self.reset = False

class Paddle():
    def __init__(self, width, height, x_pos, y_pos, image):
        self.paddle_width = width
        self.paddle_height = height
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.paddle_rect = pygame.Rect(self.x_pos, self.y_pos, self.paddle_width, self.paddle_height)
        self.paddle_img = image

    def drawPaddle(self, surface):
        self.paddle_img = pygame.transform.scale(self.paddle_img, (20, 110))
        self.paddle_rect = pygame.Rect(self.x_pos, self.y_pos, self.paddle_width, self.paddle_height)
        screen.blit(self.paddle_img, self.paddle_rect)

class P1Paddle(Paddle):
    def __init__(self, width, height, x_pos, y_pos, image):
        super().__init__(width, height, x_pos, y_pos, image)

    def handleMovement(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            self.y_pos -= 7
        if key[pygame.K_s]:
            self.y_pos += 7

class P2Paddle(Paddle):
    def __init__(self, width, height, x_pos, y_pos, image):
        super().__init__(width, height, x_pos, y_pos, image)

    def handleMovement(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and self.y_pos > 0:
            self.y_pos -= 7
        if key[pygame.K_DOWN] and self.y_pos < 400:
            self.y_pos += 7

    def drawPaddle(self, surface):
        self.paddle_img = pygame.transform.scale(self.paddle_img, (20, 110))
        self.paddle_rect = pygame.Rect(self.x_pos, self.y_pos, self.paddle_width, self.paddle_height)
        screen.blit(self.paddle_img, self.paddle_rect)
        # pygame.draw.rect(surface, ("Red"), self.paddle_rect)

class AiPaddle(Paddle):
    def __init__(self, width, height, x_pos, y_pos, image):
        super().__init__(width, height, x_pos, y_pos, image)
        self.duration = 1200
        self.move_duration = self.duration
        self.move_cooldown = self.duration
        self.last_move_time = pygame.time.get_ticks()

    def handleMovement(self, Ball):
        offset = 35  
        current_time = pygame.time.get_ticks()
        move_speed = 7  
        if current_time - self.last_move_time >= self.move_duration:
            if current_time - self.last_move_time >= self.move_duration + self.move_cooldown:
                self.last_move_time = current_time
                self.move_duration = self.duration + randint(900, 1100)
                self.move_cooldown = self.duration - randint(0, 500)
            else:
                return
        if self.y_pos > Ball.y - offset and self.y_pos > 0:
            self.y_pos -= move_speed
        if self.y_pos < Ball.y - offset and self.y_pos < 400:
            self.y_pos += move_speed

# SpriteSheet class instance

# ball
ball_x = 402
ball_y = 250
ball_rad = 10
ball_speed = 0
ball_dx = ball_speed
ball_dy = ball_speed

Ball_animation = SpriteSheets(ball_sheet)
Ball = GameBall(ball_x, ball_y, ball_dx, ball_dy, 30, 30, Ball_animation)

# Player class instance
P1_Health = [50, 560, 200, 25, 100]
P2_Health = [800 - 250, 560, 200, 25, 100]

# Functions

def drawBg():
    for x in range(12):
        speed = 1
        for i in bg_images:
            screen.blit(i, ((x * bg_width) - scroll * speed, 0))
            speed += 0.2


def handleBallPhysx():
    global ball_x, ball_y, ball_dx, ball_dy, scroll, frame_player_1, frame_player_2
    current_time = pygame.time.get_ticks()
    delay = 5000
    last_update = pygame.time.get_ticks()

    if NewAiPaddle.paddle_rect.colliderect(Ball.ball_rect):
        Ball.dx += 1
        Ball.dx = -Ball.dx

    # Ball boundaries x
    if Ball.x >= width + 100:
        Ball.resetBall()
        Ball.dx = -Ball.dx
        Player_2.health.hp -= 20
        if Player_1.current_state != "death" and Player_2.current_state != "death":
            frame_player_2 = 0
            frame_player_1 = 0
            Player_2.current_state = "hurt"
            Player_1.current_state = "attack"

    if newPaddle.paddle_rect.colliderect(Ball.ball_rect):
        Ball.dx -= 1
        Ball.dx = -Ball.dx

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
    if Ball.y + ball_rad >= height - 180:
        Ball.dy = -Ball.dy
    if Ball.y - ball_rad < 0 - 10:
        Ball.dy = -Ball.dy

def getAnimations(animation_list, length, player, action):
    for x in range(length):
        animation_list.append(getattr(player, action).getSprite(128, 128, x))

def getBallAnimations(animation_list, length, ball):
    for x in range(length):
        animation_list.append(ball.anim.getBallSprite(16, 16, x))

def drawGround():
    x = 0
    gWidth = ground.get_width()
    for x in range(27):
        screen.blit(ground, ((x * gWidth), 490))
    
def PlayAnim(count, frame):
    global Game_Over
    if frame == count - 1:
        frame = count
        Game_Over = True
        return False
    elif frame < count:
        return True

def PlayBg(background):
    global x_frames_gbg, last_update_bg, running
    if not running:
        return
    animation_delay = 150
    current_time = pygame.time.get_ticks()
    if current_time - last_update_bg >= animation_delay:
        x_frames_gbg = (x_frames_gbg + 1) % len(background)
        last_update_bg = current_time
    screen.blit(background[x_frames_gbg], (0, -100))

def PlayMainBg():
    global x_frames_bg, last_update_bg
    menu_images = []
    animation_delay = 0.3
    current_time = pygame.time.get_ticks()
    for i in range(0, 19):
        m_image = pygame.image.load(f"Assets/background/main/frame_{i}_delay-1s.gif").convert_alpha()
        m_image = pygame.transform.scale(m_image, (900, 800))
        menu_images.append(m_image)
    if current_time - last_update_bg >= animation_delay:
        x_frames_bg = (x_frames_bg + 1) % len(menu_images)
        last_update_bg = current_time
    screen.blit(menu_images[x_frames_bg], (0, -100))

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
    NewPlayer = Player(Player_sheet, Player_attack_sheet, Player_hurt_sheet, Player_dead_sheet, health)
    getAnimations(Player_idle, Idle, NewPlayer, "avatar")
    getAnimations(Player_attack, Attack, NewPlayer, "attack")
    getAnimations(Player_dead, Dead, NewPlayer, "death")
    getAnimations(Player_hurt, Hurt, NewPlayer, "hurt")
    NewPlayer.populateAnimation(Player_idle, Player_attack, Player_dead, Player_hurt)
    return NewPlayer

def mapSelect(map):
    menu_images = []
    max = 0
    if map == 1:
        max = 23
        loc = "dark"
    elif map == 2:
        max = 7
        loc = "lava"
    elif map == 3:
        max = 7
        loc = "temple"
    elif map == 4:
        max = 7
        loc = "falls"
    for i in range(0, max):
        m_image = pygame.image.load(f"Assets/background/{loc}/frame_{i}_delay-1s.gif").convert_alpha()
        m_image = pygame.transform.scale(m_image, (800, 650))
        menu_images.append(m_image)
    
    return menu_images

def resetBall():
    global reset, current
    if Ball.reset:
        if current >= reset:
            Ball.launchBall()
            current = 0
        else:
            current += 1

def mainMenu():
    global Menu, running, x_frames, last_update  # Include last_update in global variables
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            Menu = False
    PlayMainBg()

    single_player = Game_font_s.render("Single Player", True, (255, 255, 255))
    Game_name = Game_font.render("Pong ii", True, (255, 255, 255))
    Game_name_shadow = Game_font.render("Pong ii", True, (0, 0, 0))
    sp_rect = single_player.get_rect(center=(400, 240))
    start_rect_s = Game_name.get_rect(center=(400, 88))
    start_rect = Game_name.get_rect(center=(400, 85))
    screen.blit(Game_name_shadow, start_rect_s)
    screen.blit(Game_name, start_rect)
    screen.blit(single_player, sp_rect)

    # Check for button click
    mouse_pos = pygame.mouse.get_pos()
    if sp_rect.collidepoint(mouse_pos):
        if pygame.mouse.get_pressed()[0]:
            Menu = False
    pygame.display.update()

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

def gameOverScreen():
    global frame_player_1, frame_player_2
    screen.fill("Black")
    font = pygame.font.Font(None, 36)
    Game_Over_text = Game_font.render("Game Over!", True, (255, 255, 255))
    Player_win = Game_font.render(f"Player 1 wins", True, (255, 255, 255))
    Game_Over_rect = Game_Over_text.get_rect(center=(400, 150))
    handleAnim()
    if Player_2.current_state == "death":
        screen.blit(P1_currentFrame[frame_player_1], (300, 220))
    elif Player_1.current_state == "death":
        screen.blit(P2_currentFrame[frame_player_2], (300, 220))
    screen.blit(Game_Over_text, Game_Over_rect)
    screen.blit(Player_win, (20, 500))
    pygame.display.update()
    clock.tick(80)

Menu = True
Game_Over = False
last_update = pygame.time.get_ticks()
# Ball animation properties

Ball_animList = []
BallLen = 6
getBallAnimations(Ball_animList, BallLen, Ball)

# Character Animation properties
animation_cooldown = 100
last_update_bg = pygame.time.get_ticks()
x_frames_gbg = 0
x_frames_bg = 0


# Mainloop

frame_player_1 = 0
frame_player_2 = 0

Player_1 = characterSelect(randint(1, 6), P1_Health)
Player_2 = characterSelect(randint(1, 6), P2_Health)
game_bg = mapSelect(randint(1, 4))
# game_bg = mapSelect(2)

P1PaddleImg = pygame.image.load("Assets/Paddles/paddle_p1.jpg")
P2PaddleImg = pygame.image.load("Assets/Paddles/paddle_p2.jpg")
AiPaddleImg = pygame.image.load("Assets/Paddles/paddle_ai.jpg")

newPaddle = P2Paddle(20, 100, 20, 250, P1PaddleImg)
NewAiPaddle = AiPaddle(20, 100, 800-40, 250, AiPaddleImg)

reset = 100
current = 0
Ball.reset = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    while (Menu):
        mainMenu()

    if Game_Over == True:
        gameOverScreen()
    else:
        resetBall()
        current_time = pygame.time.get_ticks()
        # Handle ball physics
        handleBallPhysx()
        # Handle animation
        handleAnim()
        #--Draw
        P1_currentFrame = Player_1.animations[Player_1.current_state]
        P2_currentFrame = Player_2.animations[Player_2.current_state]
        screen.fill("#6E260E")
        #Background
        # drawBg()
        PlayBg(game_bg)

        newPaddle.drawPaddle(screen)
        newPaddle.handleMovement()
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
        screen.blit(P1_currentFrame[frame_player_1], (280, 260))
        flipped_image = pygame.transform.flip(P2_currentFrame[frame_player_2], True, False)
        screen.blit(flipped_image, (800 - (280 + 164), 260))
        #Ground
        drawGround()
        #Update display
        pygame.display.update()
        clock.tick(80)
pygame.quit()
