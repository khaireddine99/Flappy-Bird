import pygame, sys, random, math
from NN import NeuralNetwrok

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
bg_image = pygame.image.load('assets/images/background.png')

class Bird:
    def __init__(self):
        self.image1 = pygame.image.load('assets/images/downflap.png')
        self.image2 = pygame.image.load('assets/images/midflap.png')
        self.image3 = pygame.image.load('assets/images/upflap.png')
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
        self.image = pygame.image.load('assets/images/base.png')
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
        self.image = pygame.image.load('assets/images/pipe-green.png')
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



def dummy_agent():
    number = random.randint(0, 100) / 100
    return number > 0.95

def distance(point1, point2):
    """
    Calculate Euclidean distance between two points.
    point1, point2: tuples or lists like (x, y)
    """
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def fitness(distance, score):
    return distance + score * 60


def crossover(parent1, parent2):
    '''
    takes two parents and creates a child 
    '''
    child_weights = []

    for w1, w2 in zip(parent1[0], parent2[0]):
        chosen = w1 if random.random() < 0.5 else w2
        child_weights.append(chosen)

    return NeuralNetwrok(child_weights)

def mutate(genome, mutation_rate=0.1, mutation_strength=0.2):
    '''
    muatetes the current genome
    '''
    new_weights = []

    for w in genome.weights:
        if random.random() < mutation_rate:
            w += random.uniform(-mutation_strength, +mutation_strength)
        new_weights.append(w) 
    
   
    genome.weights = new_weights

def parents_search(values):
    highest_value = 0
    second_highest_value = 0
    highest_parent = []
    second_highest_parent = []

    for pair in values:
        if pair[1] > highest_value:
            highest_value = pair[1]
            highest_parent = pair
        elif pair[1] > second_highest_value:
            second_highest_value = pair[1]
            second_highest_parent = pair

    return highest_parent, second_highest_parent


class GameState:
    '''
    class responsible for managing game variables and the state of the game 
    '''
    def __init_(self):
        pass

    def new_game(self):
        pass 

    def game_over(self):
        pass


def main():
    bird = Bird()
    base = Base()
    pipe = Pipes()
    pipe_spawner = 100
    score_board = ScoreBoard()
    game_state = True
    menu_image = pygame.image.load('assets/images/message.png')
    pipes = []
    genome_data = []
    distance_travelled = 0
    genome_id = 0

    generation = 0

    # generate the first population, fitness, etc
    population = []
    for i in range(0, 10):
        new_neuron = NeuralNetwrok()
        population.append(new_neuron)
    
    while True:
        window.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game_state:
                        '''game_state = True
                        bird.move_velocity -= 15
                        nn = NeuralNetwrok()'''
                        genome_id += 1
                        if genome_id > (len(population) - 1):
                            genome_id = len(population) - 1
                        
                        game_state = True

                    else:
                        bird.move_velocity -= 20
                    jump_sound.play()


        if not game_state:
            genome_id += 1
            if genome_id > (len(population) - 1):
                genome_id = 0

                # selection, crossover, mutation
                parent1, parent2 = parents_search(genome_data)
                print(f'generation {generation} highest fitness {parent1[1]}')
                generation += 1
                genome_data = []
                population = []

                print('preparing the next generation')

                for i in range(0,10):
                    new_child = crossover(parent1, parent2)
                    mutate(new_child)
                    population.append(new_child)
 
            game_state = True

        
        window.blit(bg_image, (0, 0))
        window.blit(menu_image, (50,60))

        if game_state:
            distance_travelled += 1
            current_fitness = fitness(distance_travelled, score_board.score)

            if bird.rect.y == 0:
                current_fitness -= 10

            window.blit(bg_image, (0,0))

            # spawn pipes ---------------------------------
            pipe_spawner += 1
            if pipe_spawner >= 100:
                new_pipes = Pipes()
                pipes.append(new_pipes)
                pipe_spawner = 0

            bird.update()


            # calculate the distance between the bird and both pipes ------------------------------------------------------
            if pipes:
                for pipe in pipes:
                    if (pipe.rect.x + pipe.rect.width) > bird.rect.x :
                        # print(f'bird x {bird.rect.x + bird.rect.width}, bird y {bird.rect.y} ')
                        # print(f'first current pipe we are working with {pipe.rect.x + pipe.rect.width}, height {pipe.rect.y + pipe.rect.height}')
                        # print(f'second current pipe we are working with {pipe.rect_second.x + pipe.rect.width}, height {pipe.rect_second.y}')
                        first_distance = distance((bird.rect.x + bird.rect.width, bird.rect.y), (pipe.rect.x + pipe.rect.width, pipe.rect.y + pipe.rect.height))
                        second_distance = distance((bird.rect.x + bird.rect.width, bird.rect.y), (pipe.rect_second.x + pipe.rect_second.width, pipe.rect_second.y))
                        normalised_first_distance = first_distance / 400
                        normalised_second_distance = second_distance / 400
                   
                        if population[genome_id].forward((normalised_first_distance, normalised_second_distance)):
                            bird.move_velocity -= 20
                        
                        break


            # player base collision check -----------------------------------------------------
            if bird.rect.colliderect(base.rect) or bird.rect.colliderect(base.rect_second):

                data = [population[genome_id].weights, current_fitness]
                genome_data.append(data)

                # print(f'current fitness for generation {genome_id} , {fitness(distance_travelled, score_board.score)}')
                hit_sound.play()
                game_state = False
                pipes = []
                score_board.score = 0
                bird = Bird()
                distance_travelled = 0
                pipe_spawner = 100
                
            for pipe in pipes:
                # bird pipe collision check 
                if bird.rect.colliderect(pipe.rect) or bird.rect.colliderect(pipe.rect_second):
                    
                    data = [population[genome_id].weights, current_fitness]
                    genome_data.append(data)
                    
                    hit_sound.play()
                    game_state = False
                    pipes = []
                    score_board.score = 0
                    bird = Bird()
                    distance_travelled = 0
                    pipe_spawner = 100
                    break

                if bird.rect.x > pipe.rect.x and not pipe.passed:
                    pipe.passed = True
                    score_board.update()
                    
                pipe.update()
                pipe.draw()

            # remove pipes that leave the screen to optimize
            for pipe in pipes:
                if pipe.rect.x < - (pipe.rect.width):
                    pipes.remove(pipe)
    
        bird.animate()
        bird.draw()
        
        base.update()
        base.draw()
        score_board.draw()
        screen.blit(pygame.transform.scale(window, (game_width * 1.5, game_height * 1.5)), (0,0))
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
