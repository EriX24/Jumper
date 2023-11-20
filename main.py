import pygame
from sys import exit
from random import randint, choice


# Highest score: 59 (on 2 players uneven)
# Highest score: 45 (on 1 player normal)
# Highest score: 40 (on 2 players normal)
# Highest score: ??? (on 1 player uneven)

class Player(pygame.sprite.Sprite):
    def __init__(self, player_num):
        super().__init__()
        player_walk1 = pygame.image.load("graphics/Player/player_walk_1.png")
        player_walk2 = pygame.image.load("graphics/Player/player_walk_2.png")
        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load("graphics/Player/jump.png")

        self.player_num = player_num
        self.image = self.player_walk[0]
        if player_num == 1:
            self.rect = self.image.get_rect(midbottom=(100, 300))
        else:
            self.rect = self.image.get_rect(midbottom=(200, 300))
        self.gravity = 0
        # self.player_surf = player_walk[0]
        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")
        self.jump_sound.set_volume(0.4)

    def player_input(self):
        input_keys = pygame.key.get_pressed()
        if self.player_num == 2:
            if input_keys[pygame.K_SPACE] and self.rect.bottom >= 300:
                self.gravity = -20
                self.jump_sound.play()
        else:
            if input_keys[pygame.K_w] and self.rect.bottom >= 300:
                self.gravity = -20
                self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animate(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animate()


class Obstacle(pygame.sprite.Sprite):
    global enemy_rect_list

    def __init__(self, enemy_type):
        super().__init__()

        if enemy_type == "fly":
            fly_1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
            fly_2 = pygame.image.load("graphics/Fly/Fly2.png")
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            snail_2 = pygame.image.load("graphics/snail/snail2.png")
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))
        self.enemy_type = enemy_type
        # rect = self.image.get_rect()
        # enemy_rect_list.append(rect)

    def animate(self):
        if self.enemy_type == "fly":
            self.animation_index += 0.1
        self.animation_index += 0.1
        if self.animation_index > len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.destroy()
        self.animate()
        self.rect.x -= 6


pygame.init()
pygame.display.set_caption("Runner")
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()

# Sound
bg_music = pygame.mixer.Sound("audio/music.wav")
bg_music.play(-1)

# Groups
player1 = pygame.sprite.GroupSingle()
player1.add(Player(1))
player2 = pygame.sprite.GroupSingle()
player2.add(Player(2))

obstacle_group = pygame.sprite.Group()

# Assets
sky = pygame.image.load("graphics/Sky.png").convert()
ground = pygame.image.load("graphics/ground.png").convert()
# Font
score_font = pygame.font.Font("font/Pixeltype.ttf", 50)

# Enemies
# List
enemy_rect_list = []

# Snail
snail_frame_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_frame_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]
# snail_rect = snail_surface.get_rect(midbottom=(700, 300))

# Fly
fly_frame_1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
fly_frame_2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

# Intro screen
# Player
player_walk1 = pygame.image.load("graphics/Player/player_walk_1.png")
player_walk2 = pygame.image.load("graphics/Player/player_walk_2.png")
player_walk = [player_walk1, player_walk2]
player_index = 0
player_jump = pygame.image.load("graphics/Player/jump.png")
player_surf = player_walk[0]

player_rect = player_surf.get_rect(midbottom=(80, 300))
player_stand = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
player_stand = pygame.transform.scale(player_stand, (170, 210))
player_stand_rect = player_stand.get_rect(center=(400, 200))
# Name setup
game_name = score_font.render("Pixel Runner", False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))
# Score setup
score_surface = score_font.render(f"Press R to run", False, (111, 196, 169))
score_rect = score_surface.get_rect(center=(400, 320))
# snail_x_pos = 700

# Gravity
gravity = 0

# Start time
start_time = 0

# Score
score = 0

# Timers
# Timer for spawning obstacles
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1000)

# Timer for snail animation
snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)


# fly_animation_timer = pygame.USEREVENT + 3
# pygame.time.set_timer(fly_animation_timer, 200)


# Moving the enemies
# def obstacle_move(enemy_list):
#     if enemy_list:
#         for enemy_rect in enemy_list:
#             enemy_rect.x -= 6
#             if enemy_rect.bottom == 300:
#                 screen.blit(snail_surface, enemy_rect)
#             else:
#                 screen.blit(fly_surface, enemy_rect)
#         enemy_list = [enemy for enemy in enemy_list if enemy.x > -100]
#         # print(enemy_list)
#         return enemy_list
#     else:
#         return []


def collisions(player, enemies):
    if enemies:
        for enemy_rect in enemies:
            if player.colliderect(enemy_rect):
                return False
    return True


# Display the score
def display_score():
    global score_surface, score_rect, start_time
    current_time = pygame.time.get_ticks() - start_time
    score_surface = score_font.render(f"Score: {int(current_time / 1000)}", False, (64, 64, 64))
    score_rect = score_surface.get_rect(center=(400, 50))
    return current_time


def collision_sprite(self):
    if pygame.sprite.spritecollide(player1.sprite, obstacle_group, False) or pygame.sprite.spritecollide(
            player2.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


# Game over
def game_over():
    global enemy_rect_list
    # for i in enemy_rect_list:
    #     i.y += 1
    enemy_rect_list = []
    return enemy_rect_list


# Player animation
def player_animation():
    global player_surf, player_index
    if player_rect.bottom < 300:
        # Jump animate
        player_surf = player_jump
    else:
        # Walk animate
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]


# on = False
active = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
        #         on = False
        #         print("Jump!!!")
        #         gravity = -20

        # if event.type == pygame.MOUSEMOTION:
        #     if player_rect.collidepoint(pygame.mouse.get_pos()):
        #         print("Contact")
        #         gravity = -20

        if event.type == pygame.MOUSEBUTTONDOWN:
            # pygame.draw.line(screen, "Yellow", (400, 200), pygame.mouse.get_pos())
            # print("test")
            if player_rect.collidepoint(pygame.mouse.get_pos()):
                gravity = -20

        if active:
            fly_frame_1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
            fly_frame_2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
            fly_frames = [fly_frame_1, fly_frame_2]
            if event.type == fly_animation_timer:
                # print(fly_animation_timer)
                if fly_frame_index == 0:
                    fly_frame_index = 1
                    fly_surface = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
                else:
                    fly_frame_index = 0
                    fly_surface = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
                # fly_surface = fly_frames[fly_frame_index]
                # print("Hello, Test")
            # Obstacle timer
            if event.type == obstacle_timer:
                # Even spawning
                # obstacle_group.add(Obstacle(choice(["fly", "snail"])))
                # Uneven spawning
                obstacle_group.add(Obstacle(choice(["fly", "snail", "snail", "snail"])))

                # if randint(0, 2):
                #     # enemy_rect_list.append(snail_surface.get_rect(bottomright=(randint(900, 1100), 300)))
                #     obstacle_group.add(Obstacle("fly"))
                # else:
                #     # enemy_rect_list.append(fly_surface.get_rect(bottomright=(randint(900, 1100), 210)))
                #     obstacle_group.add(Obstacle("snail"))
            # Snail animation
            if event.type == snail_animation_timer:
                # print(event.type)
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surface = snail_frames[snail_frame_index]
            # Fly animation

            # fly_surface = fly_frames[fly_frame_index]
            # obstacle_move(enemy_rect_list)
            # if event.type == fly_animation_timer:
            #     if fly_frame_index == 0:
            #         fly_frame_index = 1
            #     else:
            #         fly_frame_index = 0
            #     fly_surface = fly_frames[fly_frame_index]

    if active:
        score = display_score()
        # Screen
        screen.blit(sky, (0, 0))
        screen.blit(ground, (0, 300))
        # Show items
        pygame.draw.rect(screen, "#c0e8ec", score_rect, border_radius=10)
        # pygame.draw.ellipse(screen, "Blue", pygame.Rect(50, 200, 100, 100))
        screen.blit(score_surface, score_rect)
        # screen.blit(snail_surface, snail_rect)

        # Snail
        # snail_rect.x -= 6
        # if snail_rect.right <= 0:
        #     snail_rect.left = 800

        # Player
        gravity += 1
        player_rect.y += gravity
        player_animation()
        # screen.blit(player_surf, player_rect)
        player1.draw(screen)
        player2.draw(screen)
        player1.update()
        player2.update()
        if player_rect.y > 400:
            player_rect.y = 200
            gravity = 0
            # if player_rect.colliderect(snail_rect):
            #     print("Ah! D:")
            active = False
        if player_rect.bottom >= 300:
            gravity = 0
            player_rect.bottom = 300
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player_rect.bottom >= 300:
            # on = False
            print("Jump!!!")
            gravity = -20
        # if player_rect.bottom == 300:
        #     on = True
        score = int((pygame.time.get_ticks() - start_time) / 1000)
        # print(f"Score: {score}")

        # Enemy movement
        # enemy_rect_list = obstacle_move(enemy_rect_list)
        obstacle_group.update()

        # Enemy
        obstacle_group.draw(screen)

        # Collisions
        # active = collisions(player_rect, enemy_rect_list)
        active = collision_sprite(screen)

    else:
        game_over()
        # player_rect.midbottom = (800, 300)
        gravity = 0
        screen.fill((94, 129, 162))
        # screen.blit(score_surface, score_rect)
        screen.blit(player_stand, player_stand_rect)
        score_message = score_font.render(f"Score: {score}", False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))
        screen.blit(game_name, game_name_rect)
        if score == 0:
            screen.blit(score_surface, score_rect)
        else:
            screen.blit(score_message, score_message_rect)
        keys_pressed = pygame.key.get_pressed()
        # score = int((pygame.time.get_ticks() - start_time) / 2000)
        # print(f"Score: {score}")
        if keys_pressed[pygame.K_r]:
            # snail_rect.left = 800
            if score != 0:
                print(f"Score: {score}")
            start_time = pygame.time.get_ticks()
            print("Respawned!!!")
            active = True

    pygame.display.update()
    clock.tick(60)
