"""Virtual Cube - control a 3x3 Rubik's cube with your hand.
Keyboard fallback: U R F D L B (hold SHIFT for prime), S scramble, SPACE solve, C reset.
Mouse: drag to rotate view."""
from ursina import *
from cube_state import Cube, FACES, random_scramble, dot
from hand_control import HandControl

USE_HAND = True          # set False to play with keyboard/mouse only
HAND_ROT_SPEED = 300     # flip sign if cube rotates the wrong way
TURN_TIME = 0.3

app = Ursina(title='Virtual Cube', borderless=False)
window.color = color.rgb(25, 25, 35)
camera.position = (0, 0, -16)

COL = {'U': color.white, 'R': color.red, 'F': color.green,
       'D': color.yellow, 'L': color.orange, 'B': color.blue}
def U(v): return Vec3(v[0], v[1], -v[2])   # logical (right-handed) -> ursina

cube = Cube()
root = Entity()
cores = []
for x in (-1, 0, 1):
    for y in (-1, 0, 1):
        for z in (-1, 0, 1):
            e = Entity(parent=root, model='cube', color=color.black, scale=0.97, position=U((x, y, z)))
            e.home, e.logical = e.position, (x, y, z)
            cores.append(e)
ents = [Entity(parent=root, model='cube') for _ in cube.stickers]

def sync():
    for e, s in zip(ents, cube.stickers):
        n = s[1]
        e.rotation = (0, 0, 0)
        e.scale = tuple(0.04 if n[i] else 0.84 for i in range(3))
        e.position = U(s[0]) + U(n) * 0.49
        e.color = COL[s[2]]
sync()

queue, busy = [], False
status = Text('', position=(-0.85, 0.47), scale=1.2)
Text('Hand: GRAB=rotate | POINT+swipe=turn layer | FIST(hold)=solve\n'
     'Keys: U R F D L B (+SHIFT) | S scramble | SPACE solve | C reset',
     position=(-0.85, -0.44), scale=0.9)

def run_move(m):
    global busy
    busy = True
    axis = FACES[m[0]]
    ai = [i for i in range(3) if axis[i]][0]
    turns = 2 if '2' in m else 1
    cw = -1 if "'" in m else 1
    ang = 90 * turns * cw * sum(axis) * (-1 if ai == 2 else 1)   # ursina is left-handed
    pivot = Entity(parent=root)
    moving = [e for e, s in zip(ents, cube.stickers) if dot(s[0], axis) == 1]
    moving += [c for c in cores if dot(c.logical, axis) == 1]
    for e in moving:
        e.world_parent = pivot
    pivot.animate('rotation_' + 'xyz'[ai], ang, duration=TURN_TIME * turns, curve=curve.in_out_quad)

    def finish():
        global busy
        for e in moving:
            e.world_parent = root
        pivot.disable(); destroy(pivot)
        for c in cores:
            c.position, c.rotation = c.home, (0, 0, 0)
        cube.move(m)
        sync()
        busy = False
    invoke(finish, delay=TURN_TIME * turns + 0.03)

def solve():
    if busy or queue:
        return
    if cube.is_solved():
        status.text = 'Already solved'; return
    sol = cube.solve()
    status.text = 'Solution: ' + ' '.join(sol)
    queue.extend(sol)

def scramble():
    if not busy and not queue:
        s = random_scramble(18)
        status.text = 'Scramble: ' + ' '.join(s)
        queue.extend(s)

hand = HandControl() if USE_HAND else None
SWIPE_MOVES = {'right': "U", 'left': "U'", 'up': "R", 'down': "R'"}

def update():
    if hand:
        h = hand.poll()
        root.rotation_y -= h['dx'] * HAND_ROT_SPEED
        root.rotation_x += h['dy'] * HAND_ROT_SPEED
        if h['swipe'] and not queue:
            queue.append(SWIPE_MOVES[h['swipe']])
        if h['solve']:
            solve()
    if held_keys['left mouse button']:
        root.rotation_y -= mouse.velocity[0] * 200
        root.rotation_x += mouse.velocity[1] * 200
    if queue and not busy:
        run_move(queue.pop(0))

def input(key):
    if key in ('u', 'r', 'f', 'd', 'l', 'b') and not busy:
        queue.append(key.upper() + ("'" if held_keys['shift'] else ''))
    elif key == 's': scramble()
    elif key == 'space': solve()
    elif key == 'c' and not busy:
        queue.clear(); cube.reset(); sync(); status.text = 'Reset'

app.run()
if hand: hand.release()
