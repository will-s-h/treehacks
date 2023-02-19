import pygame
from sys import exit
import levels
import textbox
from random import randint, choice
import PIL
from PIL import Image

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1,player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300: 
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def custom_func(self, obstacles):
        info = []
        jump = False
        for obstacle in obstacles:
            info.append((obstacle.rect.x, obstacle.rect.y, obstacle.type))

        try:
            jump = self.custom(self.rect.x, self.rect.y, info)
        except:
            pass
        
        if jump and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
    
    def set_custom(self, string):
        # string should contain 'def jump'
        try:
            exec(string)
            self.custom = locals()["jump"]
        except:
            # self.custom remains unchanged
            pass
    
    def update(self, obstacles, string=None):
        if string is not None:
            self.set_custom(string)
        self.custom_func(obstacles)
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
	def __init__(self,type):
		super().__init__()
		
		if type == 'fly':
			fly_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
			fly_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
			self.frames = [fly_1,fly_2]
			y_pos = 210

		elif type == 'dragon':
			dragon_1 = pygame.image.load('graphics/dragon/birdsprite.png').convert_alpha()
			dragon_2 = pygame.image.load('graphics/dragon/birdsprite.png').convert_alpha()
			self.frames = [dragon_1, dragon_2]
			y_pos = 200
		
		elif type == 'lion':
			lion_1 = pygame.image.load('graphics/lion/lion1.png').convert_alpha()
			lion_2 = pygame.image.load('graphics/lion/lion2.png').convert_alpha()
			self.frames = [lion_1, lion_2]
			y_pos = 320

		else:
			snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
			snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
			self.frames = [snail_1,snail_2]
			y_pos = 300
		
		self.type = type
		self.animation_index = 0
		self.image = self.frames[self.animation_index]
		self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

	def animation_state(self):
		self.animation_index += 0.1
		if self.type == 'lion':
			if self.rect.x <= 250 and self.rect.x >= 180:
				self.image = self.frames[1]
				self.rect.y = 200
			#if self.rect.x < 180 and self.rect.x >= 175:
			#	self.image = self.frames[0]
			#	self.rect.y = 320
		elif self.animation_index >= len(self.frames):
			self.animation_index = 0
			self.image = self.frames[int(self.animation_index)]

	def update(self):
		if self.type == 'dragon':
			self.rect.x -= 20
		self.animation_state()
		self.rect.x -= 6
		self.destroy()

	def destroy(self):
		if self.rect.x <= -100: 
			self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}',False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else: return True

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('./font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
text_counter = 0
bg_music = pygame.mixer.Sound('./audio/music.wav')
bg_music.play(loops = -1)

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('./graphics/Sky.png').convert()
ground_surface = pygame.image.load('./graphics/ground.png').convert()

# Snail 
snail_frame_1 = pygame.image.load('./graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('./graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

# Fly
fly_frame1 = pygame.image.load('./graphics/fly/fly1.png').convert_alpha()
fly_frame2 = pygame.image.load('./graphics/fly/fly2.png').convert_alpha()
fly_frames = [fly_frame1, fly_frame2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

player_walk_1 = pygame.image.load('./graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('./graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1,player_walk_2]
player_index = 0
player_jump = pygame.image.load('./graphics/player/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80,300))
player_gravity = 0

# Intro screen
player_stand = pygame.image.load('./graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Pixel Runner',False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render('PLAY',False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,370))

# Timer 
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

# custom code
pygame.key.set_repeat(500, 25)
code = textbox.TextInputBox(x=10, y=10, font_family="monospace", font_size=20, max_width=780, max_height=380)
level = 0

while True:
    events = pygame.event.get()

    # allows typing in text box
    if not game_active and level != 0: 
        code.update(events)
    
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        # player jump / player force quit
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300: 
                    player_gravity = -20
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
            
            # force quit to next level                            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_active = False
                for obstacle in obstacle_group: obstacle.kill()
                if level < len(levels.texts) - 1 and score >= levels.reqs[level]: level += 1
            
        else:
            # click play button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] in range(game_message_rect.centerx - game_message_rect.width // 2, game_message_rect.centerx + game_message_rect.width // 2) and \
                   event.pos[1] in range(game_message_rect.centery - game_message_rect.height // 2, game_message_rect.centery + game_message_rect.height // 2):
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 1000)
                    text_counter = 0
                    player.update(obstacle_group, string=code.get_text())
                    code.clear_text()

        # add obstacles
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))


    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        score = display_score()
        
        player.draw(screen)
        player.update(obstacle_group)

        obstacle_group.draw(screen)
        obstacle_group.update()

        # collision detection
        game_active = collision_sprite()
        if not game_active: # if killed, move to next level
            for obstacle in obstacle_group: obstacle.kill()
            if level < len(levels.texts) - 1 and score >= levels.reqs[level]: level += 1
            
		# escape text
        if score >= levels.reqs[level]:
            escape_message = test_font.render("Level Complete: Press Escape to Continue",False,(111,196,169))
            escape_message_rect = escape_message.get_rect(center = (400,250))
            screen.blit(escape_message, escape_message_rect)
        
    else:
        screen.fill((94,129,162))
        if level == 0:
            screen.blit(player_stand, player_stand_rect)

            score_message = test_font.render(f'Your score: {score}',False,(111,196,169))
            score_message_rect = score_message.get_rect(center = (400,330))
            screen.blit(game_name,game_name_rect)
            screen.blit(game_message,game_message_rect)
        else:
            if len(levels.texts[level]) > text_counter: 
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_c, unicode=levels.texts[level][text_counter]))
                text_counter += 1

            # display code
            code.render(screen)
            
            # new location for play button for level >= 0
            game_message = test_font.render('PLAY',False,(111,196,169))
            game_message_rect = game_message.get_rect(center = (750,370))
            screen.blit(game_message, game_message_rect)

        player_rect.midbottom = (80,300)
        player_gravity = 0

    pygame.display.update()
    clock.tick(60)