import pygame, sys, random

# ? creates function
def draw_floor():
    screen.blit(floor, (floor_x_pos, 650))
    screen.blit(floor, (floor_x_pos + 432, 650))
def create_pipe(): 
    random_pipe_pos = random.choice(pipe_height)
    bot_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos - 650))
    return bot_pipe, top_pipe
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600: 
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        return False
    return True        
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement * 3, 1)
    return new_bird
def birdanimation(): 
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect
def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render('Score: ' + str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (216, 100))
        screen.blit(score_surface, score_rect)
    
    if game_state == 'game over':
        score_surface = game_font.render('Score: ' + str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center = (216, 100))
        screen.blit(score_surface, score_rect)
        
        high_score_surface = game_font.render('High Score: ' + str(int(high_score)), True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center = (216, 630))
        screen.blit(high_score_surface, high_score_rect)
        
def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

# ? creates variable
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
screen = pygame.display.set_mode((432, 768))
clock = pygame.time.Clock()
gravity = 0.25
bird_movement = 0
game_active = False
score = 0
high_score = 0
game_font = pygame.font.Font('04B_19.TTF', 40)

# ? insert background
bg = pygame.image.load('assests/background-night.png').convert()
bg = pygame.transform.scale2x(bg)

# ? insert floor 
floor = pygame.image.load('assests/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

# ? create bird
bird_down = pygame.transform.scale2x(pygame.image.load('assests/yellowbird-downflap.png')).convert_alpha()
bird_mid = pygame.transform.scale2x(pygame.image.load('assests/yellowbird-midflap.png')).convert_alpha()
bird_up = pygame.transform.scale2x(pygame.image.load('assests/yellowbird-upflap.png')).convert_alpha()
bird_list = [bird_down, bird_mid, bird_up]
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center = (100, 384))

# ? create pipe
pipe_surface = pygame.image.load('assests/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
pipe_height = [200, 300, 400]

# ? create timer for pipe
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)

# ? create timer for bird
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap,200)
# ? insert over end background
game_over_surface = pygame.transform.scale2x(pygame.image.load('assests/message.png')).convert_alpha()
game_over_rest = game_over_surface.get_rect(center = (216, 384))
# ? insert sound effects
flap_sound = pygame.mixer.Sound('sound/sfx_swooshing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_down = 100

# TODO: main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement = -10
                flap_sound.play()
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 384)
                bird_movement = 0
                score = 0
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else: 
                bird_index = 0
            bird, bird_rect = birdanimation()
    # TODO: background and end background
    screen.blit(bg, (0, 0))
    if (game_active == False) :
        screen.blit(game_over_surface, game_over_rest)
        
    if game_active: 
        # TODO: bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)
        # TODO: pipe
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.05
        score_display('main game')
        score_sound_down -= 0.5  
        if score_sound_down <= 0:
            score_sound.play()
            score_sound_down = 100
    else: 
        screen.blit(game_over_surface, game_over_rest)
        high_score = update_score(score, high_score)
        score_display('game over')
    # TODO : floor
    draw_floor()
    floor_x_pos -= 1
    # ? reset floor position to the right side of the screen when it reaches the left side
    if floor_x_pos <= -432:
        floor_x_pos = 0  
    
    pygame.display.update()
    clock.tick(120)