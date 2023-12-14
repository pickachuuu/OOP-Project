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
pygame.display.set_caption("PongBat")
screen = pygame.display.set_mode(SIZE)
bg_color = 'black'
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1000)
running = True
icon = pygame.image.load("Assets/Random/icon.png")
pygame.display.set_icon(icon)


# Music properties

pygame.mixer.music.load("Assets/Sounds/bgm.mp3")
crash_sound = mixer.Sound("Assets/Sounds/hit.wav")
pygame.mixer.music.set_volume(0.5)
mixer.music.play(-1)
crash_sound.set_volume(0.5)

# Button properties

music_on = pygame.image.load("Assets/buttons/m_on.png")
music_off = pygame.image.load("Assets/buttons/m_off.png")
music_on = pygame.transform.scale(music_on, (64,64))
music_off = pygame.transform.scale(music_off, (64,64))

sfx_on = pygame.image.load("Assets/buttons/on.png")
sfx_off = pygame.image.load("Assets/buttons/off.png")
sfx_on = pygame.transform.scale(sfx_on, (64,64))
sfx_off = pygame.transform.scale(sfx_off, (64,64))

sfx_rect = sfx_on.get_rect(center=(355, 50))
msc_rect = music_on.get_rect(center=(435, 50))

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

Game_font = pygame.font.Font("Assets/fonts/mkmyth.ttf", 86)
Game_font_m = pygame.font.Font("Assets/fonts/mkmyth.ttf", 50)
Game_font_s = pygame.font.Font("Assets/fonts/mkmyth.ttf", 45)


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
        self.duration = 1000
        self.move_duration = self.duration + randint(200, 1000)
        self.move_cooldown = self.duration
        self.last_move_time = pygame.time.get_ticks()

    def drawPaddle(self, surface):
        self.paddle_img = pygame.transform.scale(self.paddle_img, (20, 110))
        self.paddle_rect = pygame.Rect(self.x_pos, self.y_pos, self.paddle_width, self.paddle_height)
        screen.blit(self.paddle_img, self.paddle_rect)

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

class P1Paddle(Paddle):
    def __init__(self, width, height, x_pos, y_pos, image):
        super().__init__(width, height, x_pos, y_pos, image)

    def handleMovement(self, Ball):
        key = pygame.key.get_pressed()
        if key[pygame.K_w] and self.y_pos > 0:
            self.y_pos -= 7
        if key[pygame.K_s] and self.y_pos < 400:
            self.y_pos += 7

class P2Paddle(Paddle):
    def __init__(self, width, height, x_pos, y_pos, image):
        super().__init__(width, height, x_pos, y_pos, image)

    def handleMovement(self, Ball):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and self.y_pos > 0:
            self.y_pos -= 7
        if key[pygame.K_DOWN] and self.y_pos < 400:
            self.y_pos += 7


# class AiPaddle(Paddle):
#     def __init__(self, width, height, x_pos, y_pos, image): 
#         super().__init__(width, height, x_pos, y_pos, image)
#         self.duration = 1000
#         self.move_duration = self.duration + randint(200, 1000)
#         self.move_cooldown = self.duration
#         self.last_move_time = pygame.time.get_ticks()

#     # def handleMovement(self, Ball):
#     #     offset = 35  
#     #     current_time = pygame.time.get_ticks()
#     #     move_speed = 7  
#     #     if current_time - self.last_move_time >= self.move_duration:
#     #         if current_time - self.last_move_time >= self.move_duration + self.move_cooldown:
#     #             self.last_move_time = current_time
#     #             self.move_duration = self.duration + randint(900, 1100)
#     #             self.move_cooldown = self.duration - randint(0, 500)
#     #         else:
#     #             return
#     #     if self.y_pos > Ball.y - offset and self.y_pos > 0:
#     #         self.y_pos -= move_speed
#     #     if self.y_pos < Ball.y - offset and self.y_pos < 400:
#     #         self.y_pos += move_speed

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

    if newPaddle2.paddle_rect.colliderect(Ball.ball_rect) and not Ball.collision_occurred:
        CollideSound()
        Ball.collision_occurred = True
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
        Ball.collision_occurred = False  # Reset the collision flag

    if newPaddle1.paddle_rect.colliderect(Ball.ball_rect) and not Ball.collision_occurred:
        CollideSound()
        Ball.collision_occurred = True
        Ball.dx -= 1
        Ball.dx = -Ball.dx

    if Ball.x - ball_rad < -100:
        Ball.resetBall()
        Ball.dx = -Ball.dx
        Player_1.health.hp -= 20
        if Player_2.current_state != "death" and Player_1.current_state != "death":
            frame_player_2 = 0
            frame_player_1 = 0
            Player_2.current_state = "attack"
            Player_1.current_state = "hurt"
        Ball.collision_occurred = False  # Reset the collision flag

    # Ball boundaries y
    if Ball.y + ball_rad >= height - 180 or Ball.y - ball_rad < 0 - 10:
        Ball.dy = -Ball.dy

    if not (newPaddle2.paddle_rect.colliderect(Ball.ball_rect) or newPaddle1.paddle_rect.colliderect(Ball.ball_rect)):
        Ball.collision_occurred = False  # Reset the collision flag


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
    multi_player = Game_font_s.render("Multi Player", True, (255, 255, 255))

    Game_name = Game_font.render("PongBat", True, (210, 43, 43))
    Game_name_shadow = Game_font.render("PongBat", True, (145, 56, 49))

    sp_rect = single_player.get_rect(center=(400, 240))
    mp_rect = multi_player.get_rect(center=(400, 340))
    start_rect = Game_name.get_rect(center=(400, 85))
    start_rect_s = Game_name.get_rect(center=(400, 87))

    mouse_pos = pygame.mouse.get_pos()
    if sp_rect.collidepoint(mouse_pos):
        single_player = Game_font_m.render("Single Player", True, (210, 255, 255))
        if pygame.mouse.get_pressed()[0]:
            Menu = False
            return 1
    elif mp_rect.collidepoint(mouse_pos):
        multi_player = Game_font_m.render("Multi Player", True, (210, 255, 255))
        if pygame.mouse.get_pressed()[0]:
            Menu = False
            return 2
        
    screen.blit(Game_name_shadow, start_rect_s)
    screen.blit(Game_name, start_rect)
    screen.blit(single_player, sp_rect)
    screen.blit(multi_player, mp_rect)
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
        game_over_text = Game_font.render("Game Over", True, (255, 255, 255))
        play_again = Game_font_s.render("Play again", True, (255, 255, 255))
        back_menu = Game_font_s.render("Menu", True, (255, 255, 255))
        play_rect = play_again.get_rect(topleft=(100, 300))
        menu_rect = back_menu.get_rect(topleft=(100, 350))

        mouse_pos = pygame.mouse.get_pos()

        # Play Again Button Logic
        if play_rect.collidepoint(mouse_pos):
            play_again, action, button_id = Game_font_m.render("Play again", True, (210, 255, 255)), restartGame, 1
            handleButtonAction(play_rect, action, button_id)

        # Return to Menu Button Logic
        if menu_rect.collidepoint(mouse_pos):
            back_menu, action, button_id = Game_font_m.render("Menu", True, (210, 255, 255)), backToMenu, 2
            handleButtonAction(menu_rect, action, button_id)

        # Display winner sprite
        if Player_1.isDead:
            screen.blit(P2_currentFrame[frame_player_2], (300, 200))
        else:
            screen.blit(P1_currentFrame[frame_player_1], (300, 200))

        screen.blit(game_over_text, (200, 150))
        screen.blit(play_again, play_rect)
        screen.blit(back_menu, menu_rect)
        pygame.display.update()
        clock.tick(80)

def handleButtonAction(rect, action, button_id):
    global last_click_state
    mouse_pos = pygame.mouse.get_pos()

    if rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] and not last_click_state:
        last_click_state = True
        if button_id == 1:
            action()
        elif button_id == 2:
            action()
    elif not pygame.mouse.get_pressed()[0]:
        last_click_state = False


def CollideSound():
    crash_sound.play()

def handleButtons():
    global button, image, image_sfx, last_click_state
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if msc_rect.collidepoint(mouse_pos) and click[0] and not last_click_state:
        last_click_state = True
        if button:
            button = False
            image = music_off
            pygame.mixer.music.set_volume(0.0)
        else:
            button = True
            image = music_on
            pygame.mixer.music.set_volume(0.5)
    elif not click[0]:
        last_click_state = False
    
    if sfx_rect.collidepoint(mouse_pos) and click[0] and not last_click_state:
        last_click_state = True
        if button:
            button = False
            image_sfx = sfx_off
            crash_sound.set_volume(0.0)
        else:
            button = True
            image_sfx = sfx_on
            crash_sound.set_volume(0.5)
    elif not click[0]:
        last_click_state = False

    screen.blit(image, msc_rect)
    screen.blit(image_sfx, sfx_rect)

def backToMenu():
    global Game_Over, Menu, Player_1, Player_2, game_bg, newPaddle1, newPaddle2, Ball
    Game_Over = False
    Menu = True

    Player_1.health.hp = 100
    Player_2.health.hp = 100

    Player_1.current_state = "idle"
    Player_2.current_state = "idle"

    Player_1.isDead = False
    Player_2.isDead = False

    Player_1.animations = {}
    Player_2.animations = {}

    Player_1 = characterSelect(randint(1, 6), P1_Health)
    Player_2 = characterSelect(randint(1, 6), P2_Health)

    newPaddle1 = P1Paddle(20, 100, 20, 250, P1PaddleImg)
    newPaddle2 = Paddle(20, 100, 800-40, 250, AiPaddleImg)

    Ball.resetBall()

def restartGame():
    global Game_Over
    Game_Over = False
    Player_1.health.hp = 100
    Player_2.health.hp = 100
    Player_1.isDead = False
    Player_2.isDead = False
    Player_1.current_state = "idle"
    Player_2.current_state = "idle"
    newPaddle1.x_pos = 20
    newPaddle1.y_pos = 250
    newPaddle2.x_pos = 800 - 40
    newPaddle2.y_pos = 250
    Ball.resetBall()
    global frame_player_1, frame_player_2
    frame_player_1 = 0
    frame_player_2 = 0

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

# buttons

button = True
image = music_on
image_sfx = sfx_on

# Mainloop

frame_player_1 = 0
frame_player_2 = 0

Player_1 = characterSelect(randint(1, 6), P1_Health)
Player_2 = characterSelect(randint(1, 6), P2_Health)
game_bg = mapSelect(randint(1, 4))

P1PaddleImg = pygame.image.load("Assets/Paddles/paddle_p1.jpg")
P2PaddleImg = pygame.image.load("Assets/Paddles/paddle_p2.jpg")
AiPaddleImg = pygame.image.load("Assets/Paddles/paddle_ai.jpg")

reset = 100
current = 0
Ball.reset = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    while (Menu):
        mode = mainMenu()
        if mode == 1:
            newPaddle1 = P1Paddle(20, 100, 20, 250, P1PaddleImg)
            newPaddle2 = Paddle(20, 100, 800-40, 250, AiPaddleImg)
        elif mode == 2:
            newPaddle1 = P1Paddle(20, 100, 20, 250, P1PaddleImg)
            newPaddle2 = P2Paddle(20, 100, 800-40, 250, P2PaddleImg)

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
        handleButtons()
        newPaddle1.drawPaddle(screen)
        newPaddle1.handleMovement(Ball)
        newPaddle2.drawPaddle(screen)
        newPaddle2.handleMovement(Ball)

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
