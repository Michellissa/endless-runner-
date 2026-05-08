import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 400, 600
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = -8.5
PIPE_WIDTH = 60
PIPE_GAP = 180
PIPE_SPEED = 4

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 36)
big_font = pygame.font.SysFont("Arial", 48)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
YELLOW = (255, 230, 50)
SKY_BLUE = (135, 206, 235)
GROUND_COLOR = (220, 180, 80)


class Bird:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.radius = 15
        self.vel_y = 0
        self.rotation = 0

    def jump(self):
        self.vel_y = JUMP_STRENGTH

    def update(self):
        self.vel_y += GRAVITY
        self.y += self.vel_y
        self.rotation = max(-30, self.vel_y * -3)

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (self.x, int(self.y)), self.radius)
        pygame.draw.circle(screen, BLACK, (self.x, int(self.y)), self.radius, 2)
        eye_x = self.x + 6
        eye_y = self.y - 4
        pygame.draw.circle(screen, BLACK, (int(eye_x), int(eye_y)), 3)
        pygame.draw.circle(screen, WHITE, (int(eye_x + 2), int(eye_y - 1)), 1)
        beak = [
            (self.x + 14, self.y),
            (self.x + 22, self.y - 3),
            (self.x + 22, self.y + 3),
        ]
        pygame.draw.polygon(screen, (255, 150, 0), beak)

    def rect(self):
        return pygame.Rect(
            self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2
        )


class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap_y = random.randint(120, HEIGHT - 200)
        self.top_height = self.gap_y - PIPE_GAP // 2
        self.bottom_y = self.gap_y + PIPE_GAP // 2
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED

    def draw(self):
        top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.top_height)
        bottom_rect = pygame.Rect(
            self.x, self.bottom_y, PIPE_WIDTH, HEIGHT - self.bottom_y
        )
        pygame.draw.rect(screen, GREEN, top_rect)
        pygame.draw.rect(screen, GREEN, bottom_rect)
        pygame.draw.rect(screen, (0, 120, 0), top_rect, 3)
        pygame.draw.rect(screen, (0, 120, 0), bottom_rect, 3)
        cap_top = pygame.Rect(self.x - 5, self.top_height - 20, PIPE_WIDTH + 10, 20)
        cap_bottom = pygame.Rect(self.x - 5, self.bottom_y, PIPE_WIDTH + 10, 20)
        pygame.draw.rect(screen, (0, 150, 0), cap_top)
        pygame.draw.rect(screen, (0, 150, 0), cap_bottom)

    def rects(self):
        top = pygame.Rect(self.x, 0, PIPE_WIDTH, self.top_height)
        bottom = pygame.Rect(self.x, self.bottom_y, PIPE_WIDTH, HEIGHT - self.bottom_y)
        return top, bottom

    def off_screen(self):
        return self.x + PIPE_WIDTH < 0


def reset_game():
    return Bird(), [], 0, 0, False


def draw_background():
    screen.fill(SKY_BLUE)
    ground_rect = pygame.Rect(0, HEIGHT - 60, WIDTH, 60)
    pygame.draw.rect(screen, GROUND_COLOR, ground_rect)
    pygame.draw.line(screen, (180, 140, 40), (0, HEIGHT - 60), (WIDTH, HEIGHT - 60), 3)
    for i in range(0, WIDTH, 30):
        x = (i - (pygame.time.get_ticks() // 3 % 30)) % WIDTH
        pygame.draw.line(screen, (180, 140, 40), (x, HEIGHT - 60), (x, HEIGHT - 40), 2)


def main():
    bird, pipes, score, spawn_timer, game_over = reset_game()
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_over:
                        bird, pipes, score, spawn_timer, game_over = reset_game()
                    else:
                        bird.jump()
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    sys.exit()

        draw_background()

        if not game_over:
            bird.update()
            spawn_timer += 1
            if spawn_timer > random.randint(80, 120):
                pipes.append(Pipe(WIDTH + 20))
                spawn_timer = 0

            for pipe in pipes[:]:
                pipe.update()
                if pipe.off_screen():
                    pipes.remove(pipe)
                elif not pipe.passed and pipe.x + PIPE_WIDTH < bird.x:
                    pipe.passed = True
                    score += 1

            for pipe in pipes:
                top, bottom = pipe.rects()
                if bird.rect().colliderect(top) or bird.rect().colliderect(bottom):
                    game_over = True

            if bird.y - bird.radius > HEIGHT - 60 or bird.y + bird.radius < 0:
                game_over = True

        for pipe in pipes:
            pipe.draw()
        bird.draw()

        score_text = font.render(str(score), True, BLACK)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 30))

        if game_over:
            go_text = big_font.render("GAME OVER", True, BLACK)
            restart_text = font.render("Press SPACE to restart", True, BLACK)
            bg = pygame.Rect(WIDTH // 2 - 140, HEIGHT // 2 - 50, 280, 100)
            pygame.draw.rect(screen, (255, 255, 255, 200), bg)
            pygame.draw.rect(screen, BLACK, bg, 2)
            screen.blit(
                go_text, (WIDTH // 2 - go_text.get_width() // 2, HEIGHT // 2 - 40)
            )
            screen.blit(
                restart_text,
                (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 15),
            )

        pygame.display.flip()


if __name__ == "__main__":
    main()
