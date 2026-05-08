import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 800, 400
FPS = 60
GRAVITY = 0.6
JUMP_STRENGTH = -12
GROUND_Y = HEIGHT - 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Endless Runner")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 32)
big_font = pygame.font.SysFont("Arial", 48)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GROUND_COLOR = (80, 60, 40)
SKY_COLOR = (135, 206, 235)
OBSTACLE_COLOR = (34, 139, 34)


class Player:
    def __init__(self):
        self.x = 100
        self.y = GROUND_Y
        self.width = 30
        self.height = 40
        self.vel_y = 0
        self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False

    def update(self):
        self.vel_y += GRAVITY
        self.y += self.vel_y
        if self.y >= GROUND_Y:
            self.y = GROUND_Y
            self.vel_y = 0
            self.on_ground = True

    def draw(self):
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height))
        eye_x = self.x + self.width - 10
        eye_y = self.y + 8
        pygame.draw.circle(screen, WHITE, (eye_x, eye_y), 4)
        pygame.draw.circle(screen, BLACK, (eye_x, eye_y), 2)

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class Obstacle:
    def __init__(self):
        self.width = random.choice([20, 25, 30])
        self.height = random.choice([35, 45, 50])
        self.x = WIDTH
        self.y = GROUND_Y + 10 - self.height
        self.speed = 6
        self.passed = False

    def update(self):
        self.x -= self.speed

    def draw(self):
        pygame.draw.rect(
            screen, OBSTACLE_COLOR, (self.x, self.y, self.width, self.height)
        )
        pygame.draw.rect(
            screen, (0, 80, 0), (self.x - 2, self.y + self.height, self.width + 4, 6)
        )

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def off_screen(self):
        return self.x + self.width < 0


class Cloud:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(30, 150)
        self.width = random.randint(50, 100)
        self.height = 30
        self.speed = 1

    def update(self):
        self.x -= self.speed
        if self.x + self.width < 0:
            self.x = WIDTH
            self.y = random.randint(30, 150)
            self.width = random.randint(50, 100)

    def draw(self):
        pygame.draw.ellipse(screen, WHITE, (self.x, self.y, self.width, self.height))


def reset_game():
    player = Player()
    obstacles = []
    clouds = [Cloud() for _ in range(4)]
    score = 0
    spawn_timer = 0
    game_over = False
    return player, obstacles, clouds, score, spawn_timer, game_over


def main():
    player, obstacles, clouds, score, spawn_timer, game_over = reset_game()
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
                        player, obstacles, clouds, score, spawn_timer, game_over = (
                            reset_game()
                        )
                    else:
                        player.jump()
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.quit()
                    sys.exit()

        if not game_over:
            player.update()

            for cloud in clouds:
                cloud.update()

            spawn_timer += 1
            if spawn_timer > random.randint(60, 120):
                obstacles.append(Obstacle())
                spawn_timer = 0

            for obs in obstacles[:]:
                obs.update()
                if obs.off_screen():
                    obstacles.remove(obs)
                elif not obs.passed and obs.x + obs.width < player.x:
                    obs.passed = True
                    score += 1

            for obs in obstacles:
                if player.rect().colliderect(obs.rect()):
                    game_over = True

            speed_bonus = score // 5
            for obs in obstacles:
                obs.speed = 6 + speed_bonus

        screen.fill(SKY_COLOR)

        pygame.draw.rect(
            screen, GROUND_COLOR, (0, GROUND_Y + 10, WIDTH, HEIGHT - GROUND_Y)
        )
        pygame.draw.line(screen, BLACK, (0, GROUND_Y + 10), (WIDTH, GROUND_Y + 10), 3)

        for i in range(0, WIDTH, 50):
            x = (i - (pygame.time.get_ticks() // 5 % 50)) % (WIDTH + 50)
            pygame.draw.ellipse(screen, (100, 80, 50), (x, GROUND_Y + 25, 30, 8))

        for cloud in clouds:
            cloud.draw()

        for obs in obstacles:
            obs.draw()

        player.draw()

        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        if game_over:
            go_text = big_font.render("GAME OVER", True, BLACK)
            restart_text = font.render("Press SPACE to restart", True, BLACK)
            screen.blit(
                go_text, (WIDTH // 2 - go_text.get_width() // 2, HEIGHT // 2 - 40)
            )
            screen.blit(
                restart_text,
                (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20),
            )

        pygame.display.flip()


if __name__ == "__main__":
    main()
