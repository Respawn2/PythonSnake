import pygame
import random
from typing import Tuple

# Константы
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
BOARD_BACKGROUND_COLOR = (0, 0, 0)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class GameObject:
    # Базовый класс для игровых объектов

    def __init__(self, position: Tuple[int, int], body_color: Tuple[int, int, int]):
        self.position = position
        self.body_color = body_color

    def draw(self, surface: pygame.Surface):
        pass


class Apple(GameObject):
    # Класс яблоко

    def __init__(self):
        super().__init__((0, 0), (255, 0, 0))  # Красный цвет
        self.randomize_position()

    def randomize_position(self):
        self.position = (
            random.randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
            random.randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE,
        )

    def draw(self, surface: pygame.Surface):
        # Отрисовывает яблоко на игровом поле
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, r)


class Snake(GameObject):
    # Класс, представляющий змейки

    def __init__(self):
        # Инициализация змейки
        super().__init__(((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)), (0, 255, 0))  # Зеленый цвет
        self.length = 1
        self.positions = [self.position]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    def update_direction(self):
        # Обновление направления движения змейки
        if self.next_direction and self.next_direction != tuple(map(lambda x, y: -x, self.direction, self.next_direction)):
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        # Перемещение змейки на одну клетку
        cur = self.get_head_position()
        x, y = self.direction
        new = (
            ((cur[0] + (x * GRID_SIZE)) % SCREEN_WIDTH),
            ((cur[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT),
        )
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.last = self.positions[-1]  # Сохранение последнего сегмента
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def draw(self, surface: pygame.Surface):
        # Отрисовка змейки на игровом поле
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, r)
            pygame.draw.rect(surface, (255, 255, 255), r, 1)
        if self.last:  # Стирание последнего сегмента
            r = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, r)

    def get_head_position(self) -> Tuple[int, int]:
        # Возврат позиции головы змейки
        return self.positions[0]

    def reset(self):
        # Сбрасывает змейку в начальное состояние
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])


def handle_keys(snake: Snake):
    # Обрабатывает нажатия клавиш
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = RIGHT


def main():
    # Основной Игрового цикла
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    surface.fill(BOARD_BACKGROUND_COLOR)
    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        surface.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(surface)
        apple.draw(surface)
        screen.blit(surface, (0, 0))
        pygame.display.update()
        clock.tick(10)


if __name__ == "__main__":
    main()