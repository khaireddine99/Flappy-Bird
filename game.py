import pygame, sys, random

pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()
game_width = 288
game_height = 512
screen = pygame.display.set_mode((game_width * 1.5, game_height * 1.5))
window = pygame.Surface((game_width, game_height))
pygame.display.set_caption('Flappy Bird')

jump_sound = pygame.mixer.Sound('assets/sound/wing.wav')
point_sound = pygame.mixer.Sound('assets/sound/point.wav')
hit_sound = pygame.mixer.Sound('assets/sound/hit.wav')
bg_image = pygame.image.load('background.png')

class Bird:
    def __init__(self):
        self.image1 = pygame.image.load('downflap.png')
        self.image2 = pygame.image.load('midflap.png')
        self.image3 = pygame.image.load('upflap.png')
        self.sprites = [self.image1, self.image2, self.image3]
        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.rect.x = 20
        self.rect.y = 230
        self.move_velocity = 0
        self.animation_counter = 0
        self.rotation_angle = 0

    
    def update(self):
        # bird movement
        self.move_velocity += 1
        if self.move_velocity > 7:
            self.move_velocity = 7
        if self.move_velocity < -24:
            self.move_velocity = -24
             
        self.rect.y += self.move_velocity
        
        if self.rect.y < 0:
            self.rect.y = 0

    
                
    def animate(self):
        # bird animation 
        self.animation_counter += 1
        if self.animation_counter >= 30:
            self.animation_counter = 0
        self.image = self.sprites[int(self.animation_counter/10)]

        if self.move_velocity < 0:
            self.rotation_angle += 15
            if self.rotation_angle > 45:
                self.rotation_angle = 45

        if self.move_velocity > 0:
            self.rotation_angle -= 5
            if self.rotation_angle < -90:
                self.rotation_angle = -90

    def draw(self):
        window.blit(pygame.transform.rotate(self.image, self.rotation_angle), (self.rect.x, self.rect.y))
        

class Base:
    def __init__(self):
        self.image = pygame.image.load('base.png')
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = game_height - self.rect.height + 25
        self.rect_second = self.image.get_rect()
        self.rect_second.x = self.rect.width
        self.rect_second.y = self.rect.y
        self.base_move_speed = 2

    def update(self):
        self.rect.x -= self.base_move_speed
        if self.rect.x < - self.rect.width:
            self.rect.x = self.rect_second.x + self.rect.width - self.base_move_speed
        self.rect_second.x -= self.base_move_speed
        if self.rect_second.x < - self.rect.width:
            self.rect_second.x = self.rect.x + self.rect.width - self.base_move_speed 

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        window.blit(self.image, (self.rect_second.x, self.rect_second.y))


class Pipes:
    def __init__(self):
        self.image = pygame.image.load('pipe-green.png')
        self.rect = self.image.get_rect()
        self.rect.x = game_width
        self.indent = random.randint(-300,-50)
        self.rect.y = self.indent
        self.passed = False

        # second pipe rect
        self.rect_second = self.image.get_rect()
        self.rect_second.x = self.rect.x
        self.rect_second.y = self.rect.y + self.rect.height + 150
    
    def update(self):
        self.rect.x -= 2
        self.rect_second.x = self.rect.x

    def draw(self):
        window.blit(pygame.transform.flip(self.image, False, True), (self.rect.x, self.rect.y))
        window.blit(self.image, (self.rect_second.x, self.rect_second.y))


class ScoreBoard:
    def __init__(self):
        self.digits = {
            '0': pygame.image.load('assets/numbers/0.png'),
            '1': pygame.image.load('assets/numbers/1.png'),
            '2': pygame.image.load('assets/numbers/2.png'),
            '3': pygame.image.load('assets/numbers/3.png'),
            '4': pygame.image.load('assets/numbers/4.png'),
            '5': pygame.image.load('assets/numbers/5.png'),
            '6': pygame.image.load('assets/numbers/6.png'),
            '7': pygame.image.load('assets/numbers/7.png'),
            '8': pygame.image.load('assets/numbers/8.png'),
            '9': pygame.image.load('assets/numbers/9.png'),
        }
        self.score = 0
        

    def update(self):
        self.score += 1
        point_sound.play()

    def draw(self):
        self.score_str = str(self.score)
        x = 120
        y = 10
        
        for digit in self.score_str:
            img = self.digits[digit]
            window.blit(img, (x, y))
            x += img.get_width() + 2 

def death_animation():
    '''will add death animation here'''
    pass

def main():
    bird = Bird()
    base = Base()
    pipe = Pipes()
    pipe_spawner = 0
    score_board = ScoreBoard()
    game_state = False
    menu_image = pygame.image.load('assets/images/message.png')
    pipes = []
    

    while True:
        window.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game_state:
                        game_state = True
                        bird.move_velocity -= 15
                    else:
                        bird.move_velocity -= 20
                    jump_sound.play()
        

        window.blit(bg_image, (0, 0))
        window.blit(menu_image, (50,60))

        if game_state:
            window.blit(bg_image, (0,0))
            pipe_spawner += 1
            if pipe_spawner == 100:
                new_pipes = Pipes()
                pipes.append(new_pipes)
                pipe_spawner = 0

            bird.update()

            for pipe in pipes:
                # bird pipe collision check 
                if bird.rect.colliderect(pipe.rect) or bird.rect.colliderect(pipe.rect_second):
                    hit_sound.play()
                    game_state = False
                    pipes = []
                    score_board.score = 0
                    bird = Bird()
                    break
                if bird.rect.x > pipe.rect.x and not pipe.passed:
                    pipe.passed = True
                    score_board.update()
                    
                pipe.update()
                pipe.draw()
            
            
            

        bird.animate()
        bird.draw()
        

        base.update()
        base.draw()
        score_board.draw()
        screen.blit(pygame.transform.scale(window, (game_width * 1.5, game_height * 1.5)), (0,0))
        pygame.display.update()
        clock.tick(60)

main()
    


