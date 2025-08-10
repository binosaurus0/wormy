# Snake Game - Enhanced version
# A modern 2D Snake game built with pygame

import random
import pygame
import sys
from enum import Enum

# Initialize pygame
pygame.init()

# Game Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 20
FPS = 12

# Calculate grid dimensions
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class GameState(Enum):
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3

class Snake:
    def __init__(self):
        self.reset()
    
    def reset(self):
        # Start with a 3-segment snake in the center
        center_x = GRID_WIDTH // 2
        center_y = GRID_HEIGHT // 2
        
        self.body = [
            (center_x, center_y),
            (center_x - 1, center_y),
            (center_x - 2, center_y)
        ]
        self.direction = Direction.RIGHT
        self.grow_pending = 0
    
    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)
        
        self.body.insert(0, new_head)
        
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()
    
    def change_direction(self, new_direction):
        # Prevent moving directly backward into yourself
        opposite = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        
        if new_direction != opposite[self.direction]:
            self.direction = new_direction
    
    def check_collision(self):
        head_x, head_y = self.body[0]
        
        # Check wall collision
        if (head_x < 0 or head_x >= GRID_WIDTH or 
            head_y < 0 or head_y >= GRID_HEIGHT):
            return True
        
        # Check self collision
        return self.body[0] in self.body[1:]
    
    def eat_food(self):
        self.grow_pending += 1
    
    def draw(self, surface):
        for i, (x, y) in enumerate(self.body):
            pixel_x = x * CELL_SIZE
            pixel_y = y * CELL_SIZE
            
            # Draw head differently from body
            if i == 0:
                pygame.draw.rect(surface, YELLOW, 
                               (pixel_x, pixel_y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(surface, DARK_GREEN, 
                               (pixel_x + 2, pixel_y + 2, CELL_SIZE - 4, CELL_SIZE - 4))
            else:
                pygame.draw.rect(surface, GREEN, 
                               (pixel_x, pixel_y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(surface, DARK_GREEN, 
                               (pixel_x + 2, pixel_y + 2, CELL_SIZE - 4, CELL_SIZE - 4))

class Food:
    def __init__(self):
        self.position = self.generate_position()
    
    def generate_position(self):
        return (random.randint(0, GRID_WIDTH - 1), 
                random.randint(0, GRID_HEIGHT - 1))
    
    def relocate(self, snake_body):
        # Make sure food doesn't spawn on snake
        while True:
            self.position = self.generate_position()
            if self.position not in snake_body:
                break
    
    def draw(self, surface):
        x, y = self.position
        pixel_x = x * CELL_SIZE
        pixel_y = y * CELL_SIZE
        pygame.draw.rect(surface, RED, 
                        (pixel_x, pixel_y, CELL_SIZE, CELL_SIZE))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.state = GameState.MENU
        self.high_score = 0
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if self.state == GameState.MENU:
                    if event.key == pygame.K_SPACE:
                        self.start_new_game()
                    elif event.key == pygame.K_ESCAPE:
                        return False
                
                elif self.state == GameState.PLAYING:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        self.snake.change_direction(Direction.UP)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        self.snake.change_direction(Direction.DOWN)
                    elif event.key in (pygame.K_LEFT, pygame.K_a):
                        self.snake.change_direction(Direction.LEFT)
                    elif event.key in (pygame.K_RIGHT, pygame.K_d):
                        self.snake.change_direction(Direction.RIGHT)
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
                
                elif self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        self.start_new_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU
        
        return True
    
    def start_new_game(self):
        self.snake.reset()
        self.food.relocate(self.snake.body)
        self.score = 0
        self.state = GameState.PLAYING
    
    def update(self):
        if self.state == GameState.PLAYING:
            self.snake.move()
            
            # Check food collision
            if self.snake.body[0] == self.food.position:
                self.snake.eat_food()
                self.score += 10
                self.food.relocate(self.snake.body)
            
            # Check game over conditions
            if self.snake.check_collision():
                self.state = GameState.GAME_OVER
                if self.score > self.high_score:
                    self.high_score = self.score
    
    def draw_grid(self):
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (WINDOW_WIDTH, y))
    
    def draw_menu(self):
        self.screen.fill(BLACK)
        
        title = self.big_font.render('SNAKE GAME', True, GREEN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
        self.screen.blit(title, title_rect)
        
        start_text = self.font.render('Press SPACE to Start', True, WHITE)
        start_rect = start_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(start_text, start_rect)
        
        controls_text = self.font.render('Use ARROW KEYS or WASD to move', True, WHITE)
        controls_rect = controls_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        self.screen.blit(controls_text, controls_rect)
        
        high_score_text = self.font.render(f'High Score: {self.high_score}', True, YELLOW)
        high_score_rect = high_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100))
        self.screen.blit(high_score_text, high_score_rect)
        
        quit_text = self.font.render('Press ESC to Quit', True, WHITE)
        quit_rect = quit_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50))
        self.screen.blit(quit_text, quit_rect)
    
    def draw_game(self):
        self.screen.fill(BLACK)
        self.draw_grid()
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw length
        length_text = self.font.render(f'Length: {len(self.snake.body)}', True, WHITE)
        self.screen.blit(length_text, (10, 50))
    
    def draw_game_over(self):
        self.screen.fill(BLACK)
        
        game_over_text = self.big_font.render('GAME OVER', True, RED)
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
        self.screen.blit(game_over_text, game_over_rect)
        
        final_score_text = self.font.render(f'Final Score: {self.score}', True, WHITE)
        final_score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(final_score_text, final_score_rect)
        
        if self.score == self.high_score and self.score > 0:
            new_record_text = self.font.render('NEW HIGH SCORE!', True, YELLOW)
            new_record_rect = new_record_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))
            self.screen.blit(new_record_text, new_record_rect)
        
        restart_text = self.font.render('Press SPACE to Play Again', True, WHITE)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
        self.screen.blit(restart_text, restart_rect)
        
        menu_text = self.font.render('Press ESC for Menu', True, WHITE)
        menu_rect = menu_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 120))
        self.screen.blit(menu_text, menu_rect)
    
    def run(self):
        running = True
        
        while running:
            running = self.handle_events()
            
            self.update()
            
            # Draw based on current state
            if self.state == GameState.MENU:
                self.draw_menu()
            elif self.state == GameState.PLAYING:
                self.draw_game()
            elif self.state == GameState.GAME_OVER:
                self.draw_game_over()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()