import pgzrun
import math
import random

WIDTH=1280
HEIGHT=800

button_play = Rect((WIDTH // 2 - 100, HEIGHT // 2 - 100), (200, 50))
button_mute = Rect((WIDTH // 2 - 100, HEIGHT // 2), (200, 50))
button_exit = Rect((WIDTH // 2 - 100, HEIGHT // 2 + 100), (200, 50))

score=0

game_state='menu'
is_muted=False

#--ship component
ship = Actor('ship1')
ship_current_angle=0
ship.angle=180
ship.pos = WIDTH//2 , HEIGHT//1.5
ship_speed=3.5
# ship component-|
# ship animation
SHIP_SPRITE = ['ship1', 'ship2', 'ship3']
ship_frame=0
ship_rate=0.1
ship_current_frame=0

fire_rate=15 
last_fire=fire_rate
BULLET_SPEED=10
bullet=[]

#--enemie component
fly = Actor('fly1')
fly_speed=6
fly_ship=Actor('mother_ship')
fly_ship.pos=(WIDTH//2,HEIGHT//6)
FLY_SPRITE=['fly1', 'fly2']
fly_rate=0.4
fly_frame=0
generate_fly_timer=0.7
fly_generate_pos=0
flies=[]
# enemie component


def generate_fly():
    fly_x = fly_ship.x + random.randint(-50, 50)  # generate from mother_ship
    fly_y = fly_ship.y + random.randint(-50, 50)
    new_fly = Actor('fly1', (fly_x, fly_y))
    new_fly.vx = random.choice([-2, 2])  # x velocity
    new_fly.vy = random.choice([-2, 2])  # y velocity
    flies.append(new_fly)


level=1

def fly_update():

    global fly_frame, generate_fly_timer, level

    # fly animation
    fly_frame += 1 / 60  # 60 FPS
    if fly_frame >= fly_rate:
        fly_frame = 0
        for fly in flies:
            current_sprite = FLY_SPRITE.index(fly.image)
            next_sprite = (current_sprite + 1) % len(FLY_SPRITE)
            fly.image = FLY_SPRITE[next_sprite]

    # move flies
    for fly in flies:
        fly.x += fly.vx
        fly.y += fly.vy

        # remove flies que saem da tela
        if fly.x <= 25 or fly.x >= WIDTH-25:
            fly.vx*=-1
        if fly.y <=25 or fly.y >= HEIGHT-25:
            fly.vy*=-1

    # generate new flies periodically
    generate_fly_timer -= 1 / (60)
    if generate_fly_timer <= 0:
        generate_fly_timer = 0.7  
        level+=0.3
        generate_fly()



def bullet_update():
    #move the bullet from the screen
    for b in bullet[:]:
        b["x"] += b["dx"] * BULLET_SPEED
        b["y"] += b["dy"] * BULLET_SPEED
        if b["x"] < 0 or b["x"] > WIDTH or b["y"] < 0 or b["y"] > HEIGHT:
            bullet.remove(b)


def ship_update():
    global ship_frame, ship_current_frame, last_fire

    #ship animation
    ship_frame += 1 / 60    #60 fps
    if ship_frame >= ship_rate:
        ship_frame = 0
        ship_current_angle = ship.angle
        ship_current_frame = (ship_current_frame + 1) % len(SHIP_SPRITE) 
        ship.image = SHIP_SPRITE[ship_current_frame] 
        ship.angle=ship_current_angle

    #ship moviment
    if keyboard.j:
        ship.angle+=4.5
    if keyboard.l:
        ship.angle-=4.5
    if keyboard.a:
        ship.x -= ship_speed
        if ship.x <= ship.width//2:
            ship.x=ship.width//2
    if keyboard.d:
        ship.x += ship_speed
        if ship.x >= WIDTH - ship.width//2:
            ship.x=WIDTH - ship.width//2
    if keyboard.w:
        ship.y -= ship_speed
        if ship.y <= ship.height//2:
            ship.y=ship.height//2
    if keyboard.s:
        ship.y += ship_speed
        if ship.y >= HEIGHT - ship.height//2:
            ship.y=HEIGHT - ship.height//2

    #ship shoot
    if last_fire < fire_rate:
        last_fire += 1

    if keyboard.k and last_fire>=fire_rate:
        if not is_muted:
            sounds.shoot.play()
        last_fire=0
        rad_angle = math.radians(ship.angle-90) 
        direction_x = math.cos(rad_angle)    
        direction_y = -math.sin(rad_angle)  
        
        direction_x /= math.sqrt(direction_x**2 + direction_y**2)
        direction_y /= math.sqrt(direction_x**2 + direction_y**2) 
    
        bullet.append({
            "x": ship.x,
            "y": ship.y,
            "dx": direction_x,
            "dy": direction_y
        })


def on_mouse_down(pos):
    
    global game_state, is_muted

    if game_state == "menu":
        if button_play.collidepoint(pos):
            game_state = "game" 
        elif button_mute.collidepoint(pos):
            is_muted = not is_muted
            if is_muted:
                music.pause()
            else:
                music.unpause() 
        elif button_exit.collidepoint(pos):
            exit()  



def reset_game():
    global flies, bullet, generate_fly_timer, level, ship, game_state

    game_state='game_over'

    ship.pos = WIDTH // 2, HEIGHT // 1.5
    ship.angle = 180

    flies = []
    bullet = []

    generate_fly_timer = 0.7
    level = 1


def menu():

    #draw initial menu
    screen.clear()
    screen.draw.text("MENU", center=(WIDTH // 2, HEIGHT // 2 - 200), fontsize=60, color="white")

    screen.draw.filled_rect(button_play, "green")
    screen.draw.text("PLAY", center=button_play.center, fontsize=30, color="white")

    screen.draw.filled_rect(button_mute, "blue")
    mute_text = "UNMUTE" if is_muted else "MUTE"
    screen.draw.text(mute_text, center=button_mute.center, fontsize=30, color="white")

    screen.draw.filled_rect(button_exit, "red")
    screen.draw.text("EXIT", center=button_exit.center, fontsize=30, color="white")


music.play('song')


def update():
    global game_state, bullet, score

    if game_state == "game":
        if keyboard.escape:
            game_state = "menu"
            bullet = []
            ship.pos = WIDTH // 2, HEIGHT // 1.5
            ship.angle = 180
        else:
            ship_update()
            bullet_update()
            fly_update()
            
            for f in flies[:]:
                hitbox=Rect(f.x-f.width//4,f.y-f.height//4,f.width//4,f.height//8)
                if ship.colliderect(hitbox):
                    game_state='menu'
                    reset_game()
                    return

            for b in bullet[:]:  
                for e in flies[:]:  
                    if e.collidepoint(b["x"], b["y"]):  
                        bullet.remove(b)  
                        flies.remove(e)
                        score+=1  
                        break
    elif game_state == "game_over":
        if keyboard.escape:
            game_state = "menu"
            score = 0


def draw():

    if game_state == 'menu':
        menu()
    elif game_state == 'game':
        screen.clear()
        ship.draw()
        fly_ship.draw()
        screen.draw.text(f"SCORE: {score}", (WIDTH // 2 - 200, 10), color="white", fontsize=30)
        for b in bullet:
            screen.draw.filled_circle((b["x"], b["y"]), 5, "red")  
        for f in flies:
            f.draw()
    elif game_state == 'game_over':
        screen.clear()
        screen.draw.text("GAME OVER", center=(WIDTH // 2, HEIGHT // 2 - 50), fontsize=60, color="red")
        screen.draw.text(f"FINAL SCORE: {score}", center=(WIDTH // 2, HEIGHT // 2 + 20), fontsize=40, color="white")
        screen.draw.text("PRESS ESC TO RETURN TO MENU", center=(WIDTH // 2, HEIGHT // 2 + 100), fontsize=30, color="yellow")     


pgzrun.go()
