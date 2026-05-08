from ursina import *
import random

app = Ursina()

window.title = "Endless Runner 3D"
window.borderless = False
window.fullscreen = False
window.size = (1000, 700)

Sky(color=color.rgb(100, 150, 210))

scene.fog_color = color.rgb(100, 150, 210)
scene.fog_density = 0.008

score = 0
game_over = False
scroll_speed = 10
obstacle_list = []
lane_positions = [-2.5, 0, 2.5]
current_lane = 1
target_x = 0
spawn_counter = 0

player = Entity(
    model="cube",
    color=color.orange,
    texture="white_cube",
    scale=(0.7, 1, 0.7),
    position=(0, 0.5, 0),
    collider="box",
)
player.y_velocity = 0
player.tilt_target = 0

ground = Entity(
    model="cube",
    color=color.rgb(60, 140, 60),
    scale=(20, 0.2, 200),
    position=(0, -0.1, 0),
    collider="box",
)

road = Entity(
    model="cube",
    color=color.rgb(80, 80, 80),
    texture="white_cube",
    scale=(7, 0.05, 200),
    position=(0, 0.01, 0),
)

for i in range(3):
    Entity(
        model="cube",
        color=color.white,
        scale=(0.1, 0.03, 200),
        position=(-2.5 + i * 2.5, 0.08, 0),
    )

for x in lane_positions:
    for z in range(0, 200, 4):
        Entity(
            model="cube",
            color=color.white,
            scale=(0.05, 0.01, 0.2),
            position=(x, 0.12, z),
        )

DirectionalLight(shadow_map_resolution=Vec2(2048, 2048))


def create_obstacle():
    lane = random.randint(0, 2)
    x = lane_positions[lane]
    height = random.choice([1.0, 1.5, 2.0])
    color_choice = random.choice(
        [color.rgb(200, 50, 50), color.rgb(50, 50, 200), color.rgb(200, 150, 0)]
    )
    obs = Entity(
        model="cube",
        color=color_choice,
        texture="noise",
        scale=(0.7, height, 0.7),
        position=(x, height / 2, 80),
        collider="box",
    )
    obs.hit = False
    obstacle_list.append(obs)


def reset_game():
    global score, game_over, scroll_speed, current_lane, target_x, spawn_counter
    score = 0
    game_over = False
    scroll_speed = 10
    current_lane = 1
    target_x = 0
    spawn_counter = 0
    player.position = (0, 0.5, 0)
    player.y_velocity = 0
    player.color = color.orange
    player.tilt_target = 0
    player.rotation_z = 0
    go_panel.visible = False
    go_text.visible = False
    restart_text.visible = False
    for obs in obstacle_list:
        destroy(obs)
    obstacle_list.clear()


def update():
    global score, game_over, scroll_speed, spawn_counter

    if game_over:
        return

    player.y_velocity -= 25 * time.dt
    player.y += player.y_velocity * time.dt
    if player.y <= 0.5:
        player.y = 0.5
        player.y_velocity = 0

    dx = target_x - player.x
    player.x += dx * 12 * time.dt if abs(dx) > 0.05 else dx

    player.rotation_z = lerp(player.rotation_z, player.tilt_target, 8 * time.dt)

    for obs in obstacle_list[:]:
        obs.z -= scroll_speed * time.dt
        if obs.z < -5:
            obstacle_list.remove(obs)
            destroy(obs)
            if not obs.hit:
                score += 1

    for obs in obstacle_list:
        if player.intersects(obs).hit and not obs.hit:
            obs.hit = True
            game_over = True
            player.color = color.red
            go_panel.visible = True
            go_text.visible = True
            restart_text.visible = True

    spawn_counter += 1
    if spawn_counter > max(15, 40 - score):
        create_obstacle()
        spawn_counter = 0

    scroll_speed = 10 + score * 0.15

    score_text.text = f"Score: {score}"
    if game_over:
        go_text.text = "GAME OVER"
        restart_text.text = "Press SPACE to restart"


def input(key):
    global current_lane, target_x, game_over

    if key == "space":
        if game_over:
            reset_game()
        elif player.y <= 0.51:
            player.y_velocity = 10

    if key == "a" or key == "left arrow":
        current_lane = max(0, current_lane - 1)
        target_x = lane_positions[current_lane]
        player.tilt_target = 8

    if key == "d" or key == "right arrow":
        current_lane = min(2, current_lane + 1)
        target_x = lane_positions[current_lane]
        player.tilt_target = -8

    if (
        key == "a up"
        or key == "left arrow up"
        or key == "d up"
        or key == "right arrow up"
    ):
        player.tilt_target = 0


score_text = Text(
    text="Score: 0",
    position=(-0.85, 0.45),
    scale=2,
    color=color.black,
    font="VeraMono.ttf",
)

go_panel = Entity(
    parent=camera.ui,
    model="quad",
    color=color.rgba(0, 0, 0, 160),
    scale=(0.55, 0.25),
    position=(0, 0.05),
    z=-1,
)
go_panel.visible = False

go_text = Text(
    text="",
    position=(0, 0.12),
    scale=3,
    color=color.red,
    origin=(0, 0),
    font="VeraMono.ttf",
)
go_text.visible = False

restart_text = Text(
    text="",
    position=(0, -0.04),
    scale=1.5,
    color=color.white,
    origin=(0, 0),
    font="VeraMono.ttf",
)
restart_text.visible = False

app.run()
