import pgzrun
import random

WIDTH=800
HEIGHT=600

GRAVITY=10
Y_VELOCITY=0

PLAYER_IMAGES={
    'eyes':['facial_part_eye_open',
            'facial_part_eye_closed_down'],
}

player=Actor('red_body_circle',(WIDTH//2,HEIGHT//2))
eye=Actor(PLAYER_IMAGES['eyes'][0],(player.x,player.y))
is_jump=False

idle_t=0
blink_t=0
last_position=player.pos

chunks = []
current_chunk_index = 0

def create_chunk():
    #create random chunk's
    floor = []
    x_position = 0
    while x_position < WIDTH:
        width = random.randint(85, 130)
        height = random.randint(HEIGHT - 130, HEIGHT - 85)
        floor.append(Actor('tile', (x_position + width // 2, height)))
        x_position += width + random.randint(85, 130)
    return floor

def load_chunk(index):
    #carrega todos os chunks anteriormente salvos
    global chunks
    while len(chunks) <= index:
        chunks.append(create_chunk())
    return chunks[index]

def create_floor():
    global floor
    for i in range(1,WIDTH,200):
        height=random.randint(200,500)
        width=random.randint(100,500)
        floor.append(Actor('tile',(width,height)))

floor=[
    Actor('main_floor',(WIDTH//2,HEIGHT-50))    
]

def blink():
    current_state = PLAYER_IMAGES['eyes'].index(eye.image)
    next_state = (current_state + 1) % len(PLAYER_IMAGES['eyes'])
    eye.image = PLAYER_IMAGES['eyes'][next_state]


def update():
    global blink_t, last_position, idle_t

    blink_t+=1
    if blink_t > 30:  
        blink()
        blink_t = 0

    if keyboard.a:
        player.x -= 5
        if player.x <= player.width//2:
            player.x=player.width//2

    if keyboard.d:
        player.x+=5
        if player.x>=WIDTH-player.width//2:
            player.x=WIDTH-player.width//2

    if keyboard.w:
        player.y-=5
        if player.y<=player.height//2:
            player.y=player.height//2
        
    if keyboard.s:
        player.y+=5
        if player.y>=HEIGHT-player.height//2:
            player.y=HEIGHT-player.height//2


    if keyboard.s and keyboard.space:
        player.image='red_body_circle'
    elif keyboard.space:
        player.image='red_body_circle_big'

    eye.pos=player.pos
    last_position=player.pos
    

def draw():
    screen.fill((130,179,216))
    for f in floor:
        f.draw()
    player.draw()
    eye.draw()

create_floor()

pgzrun.go()
