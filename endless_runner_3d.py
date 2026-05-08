from ursina import *
import random

app = Ursina()

window.title = "Endless Runner 3D"
window.borderless = False
window.fullscreen = False
window.size = (1000, 700)

score = 0
game_over = False
scroll_speed = 8
obstacle_list = []
lane_positions = [-3, 0, 3]
current_lane = 1
target_x = 0

player = Entity(
    model="cube",
    color=color.black,
    scale=(0.8, 1.2, 0.8),
    position=(0, 1, 0),
    collider="box",
)
player.y_velocity = 0

camera.position = (0, 6, -12)
camera.rotation_x = 20

ground = Entity(
    model="cube",
    color=color.rgb(60, 40, 20),
    scale=(30, 0.5, 100),
    position=(0, -0.25, 50),
    texture="white_cube",
    collider="box",
)

road = Entity(
    model="cube",
    color=color.rgb(80, 80, 80),
    scale=(10, 0.1, 100),
    position=(0, 0.05, 50),
)

for i in range(2):
    Entity(
        model="cube",
        color=color.rgb(200, 200, 200),
        scale=(0.15, 0.05, 50),
        position=(-5 + i * 10, 0.1, 50),
    )


def create_obstacle():
    lane = random.randint(0, 2)
    x = lane_positions[lane]
    height = random.choice([1.0, 1.5, 2.0])
    obs = Entity(
        model="cube",
        color=color.rgb(34, 139, 34),
        scale=(0.8, height, 0.8),
        position=(x, height / 2, 60),
        collider="box",
    )
    obs.hit = False
    obstacle_list.append(obs)


def reset_game():
    global score, game_over, scroll_speed, current_lane, target_x
    score = 0
    game_over = False
    scroll_speed = 8
    current_lane = 1
    target_x = 0
    player.position = (0, 1, 0)
    player.y_velocity = 0
    player.color = color.black
    for obs in obstacle_list:
        destroy(obs)
    obstacle_list.clear()


def update():
    global score, game_over, scroll_speed

    if game_over:
        return

    player.y_velocity -= 20 * time.dt
    player.y += player.y_velocity * time.dt
    if player.y <= 1:
        player.y = 1
        player.y_velocity = 0

    dx = target_x - player.x
    player.x += dx * 10 * time.dt if abs(dx) > 0.05 else dx

    for obs in obstacle_list[:]:
        obs.z -= scroll_speed * time.dt
        if obs.z < -10:
            obstacle_list.remove(obs)
            destroy(obs)
            if not obs.hit:
                score += 1

    for obs in obstacle_list:
        if player.intersects(obs).hit and not obs.hit:
            obs.hit = True
            game_over = True
            player.color = color.red

    if random.random() < 0.02:
        create_obstacle()

    scroll_speed = 8 + score * 0.1

    score_text.text = f"Score: {score}"
    if game_over:
        go_text.text = "GAME OVER"
        restart_text.text = "Press SPACE to restart"


def input(key):
    global current_lane, target_x, game_over

    if key == "space":
        if game_over:
            reset_game()
        elif player.y <= 1.01:
            player.y_velocity = 8

    if key == "a" or key == "left arrow":
        current_lane = max(0, current_lane - 1)
        target_x = lane_positions[current_lane]

    if key == "d" or key == "right arrow":
        current_lane = min(2, current_lane + 1)
        target_x = lane_positions[current_lane]


score_text = Text(text="Score: 0", position=(-0.85, 0.45), scale=2, color=color.black)
go_text = Text(text="", position=(0, 0.1), scale=3, color=color.red, origin=(0, 0))
restart_text = Text(
    text="", position=(0, -0.1), scale=1.5, color=color.black, origin=(0, 0)
)

app.run()
