import pygame, sys, random

pygame.init()
screen = pygame.display.set_mode((288,512)) #draws a canvas of size 288x512
clock = pygame.time.Clock()
flr_move = 0
gravity = 0.25
bird_move = 0
game = False
score = 0
hg_sr = 0
sr_up = True
start = False

#functions
def draw_floor():
    screen.blit(flr,(flr_move,400))
    screen.blit(flr,(flr_move+288,400))

def create_pipe():
    rand_pipe = random.choice(pipe_height)
    up_pipe = pipe.get_rect(midtop=(300,rand_pipe))
    down_pipe = pipe.get_rect(midbottom=(300,rand_pipe - 100))
    return up_pipe, down_pipe

def move_pipes(pipes):
    for p in  pipes:
        p.centerx -=5
    return [p for p in pipes if p.right > -10]

def draw_pipes(pipes):
    for p in pipes:
        if p.bottom >= 400:
            screen.blit(pipe,p)
        else:
            flip = pygame.transform.flip(pipe, False, True)
            screen.blit(flip,p)

def collision(pipes):
    for p in pipes:
        if bird_rect.colliderect(p):
            hit.play()
            return False
    if bird_rect.top <= 0 or bird_rect.bottom >= 400:
        hit.play()
        return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, bird_move*-3, 1)
    return new_bird

def score_display():
    sr_sf = text.render('Score: {}'.format(score),True,(255,255,255)) #Boolean for anti-aliasing
    sr_rt = sr_sf.get_rect(center = (144,30))

    if game:
        screen.blit(sr_sf,sr_rt)

    elif not game and start:
        sr_rt.centery = 180
        hgsr_sf = text.render('High Score: {}'.format(hg_sr),True,(255,255,255)) #Boolean for anti-aliasing
        hgsr_rt = hgsr_sf.get_rect(center = (144,230))
        screen.blit(sr_sf,sr_rt)
        screen.blit(hgsr_sf,hgsr_rt)


def score_check():
    global score, sr_up
    if pipe_list:
        if 45 < pipe_list[0].centerx < 55 and sr_up:
            score+=1
            pt.play()
            sr_up = False
        elif pipe_list[0].centerx < 20:
            sr_up = True

#surfaces
bg = pygame.image.load('assets/background-night.png').convert()
flr = pygame.image.load('assets/base.png').convert()

bird_up = pygame.image.load('assets/redbird-upflap.png').convert_alpha()
bird_mid = pygame.image.load('assets/redbird-midflap.png').convert_alpha()
bird_down = pygame.image.load('assets/redbird-downflap.png').convert_alpha()
bird = [bird_up, bird_mid, bird_down]
bird_index = 0
bird_rect = bird[bird_index].get_rect(center = (50, 256))
FLAP = pygame.USEREVENT
pygame.time.set_timer(FLAP, 50)

pipe = pygame.image.load('assets/pipe-red.png').convert()
pipe_list = []
SPAWNPIPE = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWNPIPE, 1000)
pipe_height = [150, 200, 250, 300, 350]

text = pygame.font.Font("04B_19.TTF",20)

#sounds
flaps = pygame.mixer.Sound("sound/sfx_wing.wav")
hit = pygame.mixer.Sound("sound/sfx_hit.wav")
pt = pygame.mixer.Sound("sound/sfx_point.wav")

while True:  #game loop
    for event in pygame.event.get(): #event loop  #event.get() returns the list of all events
        if event.type == pygame.QUIT:  #when close button is clicked
            pygame.quit()   #closes pygame
            sys.exit()   #closes python

        if event.type == FLAP:
            bird_index = (bird_index + 1) % 3
            bird_rect = bird[bird_index].get_rect(center = (50, bird_rect.centery))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game:
                bird_move = 0
                bird_move -=5
                flaps.play()
            if event.key == pygame.K_RETURN and not game:
                pipe_list.clear()
                bird_rect.center = (50, 256)
                bird_move = -5
                game = True
                start = True
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    screen.blit(bg,(0,0))

    if not start:
        begin = pygame.image.load("assets/message.png").convert_alpha();
        begin_rt = begin.get_rect(center = (144,210))
        screen.blit(begin,begin_rt)

    if game:
        #bird
        bird_move += gravity
        bird_rotate = rotate_bird(bird[bird_index])
        bird_rect.centery += bird_move
        screen.blit(bird_rotate,bird_rect)

        #pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        game=collision(pipe_list)
        score_check()

    elif not game and start:
        if score > hg_sr:
            hg_sr = score
        over = pygame.image.load('assets/gameover.png').convert_alpha()
        over_rt = over.get_rect(center = (144,50))
        screen.blit(over,over_rt)

    #floor
    draw_floor()
    flr_move-=1
    if flr_move < -288:
        flr_move = 0

    score_display()

    pygame.display.update() #updates screen
    clock.tick(60)  #frame rate
