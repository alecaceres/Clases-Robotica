# basado en: https://k3no.medium.com/build-a-maze-with-python-920ac2266fe7 
import PySimpleGUI as sg
import numpy as np
import math
import random
import scipy.io as sio # para la lectura del .mat

AppFont = 'Any 16'
sg.theme('DarkGrey5')
_VARS = {'cellCount': 32, 'gridSize': 608, 'canvas': False, 'window': False,
         'playerPos': [1, 1], 'targetA': [10,24], 'targetB': [29,2], 'cellMAP': False,
         'player1Pos': [[4, 27], [5, 27], [4, 28], [5, 28]]}
cellSize = _VARS['gridSize']/_VARS['cellCount']
exitPos = [_VARS['cellCount']-1, _VARS['cellCount']-1]  
possibleMoves = [
    90, # gira al robot 90°
    -90, # gira al robot -90°
    45, # mueve la pata derecha hacia adelante
    135, # mueve la pata izquierda hacia adelante
    -45, # mueve la pata derecha hacia atrás
    -135, # mueve la pata izquierda hacia atrás
    0, # no realiza ningún movimiento
] # estos son los movimientos que le toman a cada robot una iteración en completarlos



def makeMaze():
    mat_contents = sio.loadmat('./src/SwarmRobotics/mat/pista.mat')
    obstaculos = np.zeros((32,32)) # la matriz de obstáculos se extiende a 32x32
    obstaculos[1:31,1:31] = mat_contents['obstaculos']
    paredes = np.ones((32,32))
    paredes[1:31,1:31] = mat_contents['paredes']
    return obstaculos, paredes


_VARS['cellMAP'], _VARS['wallMAP'] = makeMaze() # cellMAP = obstáculos, wallMAP = paredes
for i in range(1,8):
    print(f"Positioning robot {i}...")
    x,y = [random.choice(range(1,31)), random.choice(range(1,31))] # coordenadas de FR
    full = _VARS['cellMAP'].T + _VARS['wallMAP'].T
    robots = [pos for key in _VARS if key.endswith("Pos") for pos in _VARS[key] if isinstance(pos,list)]
    for xpos,ypos in robots: full[xpos,ypos] = 1
    while True:
        print(f"\tTrying with ({x},{y})...")
        is_empty = not (full[x,y])
        print(f"\t\tIs empty? {is_empty}")
        if is_empty:
            direction = []
            for a in [[x-1,y-1], [x,y-1], [x+1,y-1], [x-1,y],[x,y],[x+1,y],[x-1,y+1],[x,y+1],[x+1,y+1]]:
                print("\t\t\t",a, full[a[0], a[1]])

            if not (full[x-1,y] or full[x,y+1] or full[x-1,y+1]): direction.append("UP")
            if not (full[x+1,y] or full[x,y-1] or full[x+1,y-1]): direction.append("DOWN")
            if not (full[x+1,y] or full[x,y+1] or full[x+1,y+1]): direction.append("LEFT")
            if not (full[x-1,y] or full[x,y-1] or full[x-1,y-1]): direction.append("RIGHT")
            print(f"\t\tDirections: {direction}")
            if direction:
                chosenDirection = random.choice(direction)
                print(f"\t\tThe chosen direction is {chosenDirection}")
                if chosenDirection == "UP":
                    _VARS[f'robot{i}Pos'] = [[x-1,y], [x,y], [x-1,y+1], [x,y+1]]
                    break
                if chosenDirection == "DOWN":
                    _VARS[f'robot{i}Pos'] = [[x+1,y], [x,y], [x+1,y-1], [x,y-1]]
                    break
                if chosenDirection == "LEFT":
                    _VARS[f'robot{i}Pos'] = [[x,y+1], [x,y], [x+1,y+1], [x+1,y]]
                    break
                if chosenDirection == "RIGHT":
                    _VARS[f'robot{i}Pos'] = [[x,y-1], [x,y], [x-1,y-1], [x-1,y]]
                    break
        x,y = random.choice(range(1,31)), random.choice(range(1,31))
    


# METHODS:


def drawGrid():
    cells = _VARS['cellCount']
    _VARS['canvas'].TKCanvas.create_rectangle(
        1, 1, _VARS['gridSize'], _VARS['gridSize'], outline='BLACK', width=1)
    for x in range(cells):
        _VARS['canvas'].TKCanvas.create_line(
            ((cellSize * x), 0), ((cellSize * x), _VARS['gridSize']),
            fill='BLACK', width=1)
        _VARS['canvas'].TKCanvas.create_line(
            (0, (cellSize * x)), (_VARS['gridSize'], (cellSize * x)),
            fill='BLACK', width=1)


def drawCell(x, y, color='#b7b7b7', text = "", outline="BLACK"):
    x *= cellSize
    y *= cellSize
    _VARS['canvas'].TKCanvas.create_rectangle(
        x, y, x + cellSize, y + cellSize,
        outline=outline, fill=color, width=1)
    if text: drawTextInCell(x, y, text)


def drawTextInCell(x, y, text, color="BLACK"):
    _VARS['canvas'].TKCanvas.create_text(x+cellSize/2,
                        y+cellSize/2, text=text, fill=color)

def drawRobot(robotNum):
    '''
    Dibuja el robot en el mapa

    robotNum:   1 si se trata del robot principal, 2 si es su compañero

    _VARS[f'player{robotNum}Pos'] debe tener por valor una lista de cuatro
    elementos: posiciones x,y de FL, FR, RL y RR
'''
    FL, FR, RL, RR = _VARS[f'player{robotNum}Pos']
    drawCell(*FL, color="#f6b26b", text = "FL")
    drawCell(*FR, color="#f6b26b", text = "FR")
    drawCell(*RL, color="#b6d7a8", text = "RL")
    drawCell(*RR, color="#b6d7a8", text = "RR")
    
def drawTargets():
    for i, [x,y] in enumerate([_VARS['targetA'], _VARS['targetB']]):
        text = ["A", "B"][i]
        color = ["#ffff00", "#b6d7a8"][i]
        drawCell(x, y, color=color, outline=color) # esq. sup. der.
        drawCell(x-1, y, color=color, outline=color) # esq. sup. izq.
        drawCell(x, y+1, color=color, outline=color) # esq. inf. der.
        drawCell(x-1, y+1, color=color, outline=color) # esq. inf. izq
        _VARS['canvas'].TKCanvas.create_text(x*cellSize,
                        (y+1)*cellSize, text=text, fill="BLACK")

def drawDummyRobots():
    """
    Esta función ubica en el mapa a los robots no controlados del algoritmo.
    """
    for i in range(1,8):
        FL, FR, RL, RR = _VARS[f'robot{i}Pos']
        xcg, ycg = 0, 0
        for x,y in _VARS[f'robot{i}Pos']: xcg+=x/4; ycg+=y/4
        drawCell(*FR, color="#fff2cc", outline="#fff2cc") # esq. sup. der.
        drawCell(*FL, color="#fff2cc", outline="#fff2cc") # esq. sup. izq.
        drawCell(*RR, color="#fff2cc", outline="#fff2cc") # esq. inf. der.
        drawCell(*RL, color="#fff2cc", outline="#fff2cc") # esq. inf. izq
        _VARS['canvas'].TKCanvas.create_text(xcg*cellSize+cellSize/2,
                        ycg*cellSize+cellSize/2, text=f'R{i}', fill="BLACK")

def moveDummyRobots():
    for i in range(1,8):
        move = random.choice(possibleMoves) # si no es posible, espera otro turno
        x,y = _VARS[f'robot{i}Pos']
        drawCell(x, y, color="#fff2cc", outline="#fff2cc") # esq. sup. der.
        drawCell(x-1, y, color="#fff2cc", outline="#fff2cc") # esq. sup. izq.
        drawCell(x, y+1, color="#fff2cc", outline="#fff2cc") # esq. inf. der.
        drawCell(x-1, y+1, color="#fff2cc", outline="#fff2cc") # esq. inf. izq
        _VARS['canvas'].TKCanvas.create_text(x*cellSize,
                        (y+1)*cellSize, text=f'R{i}', fill="BLACK")


def placeCells():
    for row in range(_VARS['cellMAP'].shape[0]):
        for column in range(_VARS['cellMAP'].shape[1]):
            if(_VARS['wallMAP'][column][row] == 1): # 1 si está pintado, 0 si no
                drawCell(row, column, 'BLACK')
            elif(_VARS['cellMAP'][column][row] == 1): # si la pared no está pintada, se verifica el obstáculo
                drawCell(row, column) # se pinta de gris por defecto


def checkEvents(event):
    move = ''
    if len(event) == 1:
        if ord(event) == 63232:  # UP
            move = 'Up'
        elif ord(event) == 63233:  # DOWN
            move = 'Down'
        elif ord(event) == 63234:  # LEFT
            move = 'Left'
        elif ord(event) == 63235:  # RIGHT
            move = 'Right'
    # Filter key press Windows :
    else:
        if event.startswith('Up'):
            move = 'Up'
        elif event.startswith('Down'):
            move = 'Down'
        elif event.startswith('Left'):
            move = 'Left'
        elif event.startswith('Right'):
            move = 'Right'
    return move


# Inicio  :
layout = [[sg.Canvas(size=(_VARS['gridSize'], _VARS['gridSize']),
                     background_color='white',
                     key='canvas')],
          [sg.Exit(font=AppFont),
           sg.Text('', key='-exit-', font=AppFont, size=(5, 1)),
           sg.Button('START', font=AppFont),
           sg.Text('', key='-start-', font=AppFont, size=(5, 1)),
           sg.Button('STOP', font=AppFont)]] # se dibuja el layout de la GUI

_VARS['window'] = sg.Window('Random Puzzle Generator', layout, resizable=True, finalize=True,
                            return_keyboard_events=True)
_VARS['canvas'] = _VARS['window']['canvas']
drawGrid() # se dibuja la malla 32x32
drawRobot(1) # posición inicial del robot A
drawTargets()
drawDummyRobots()
placeCells()


while True:             # Se actúa en un bucle según el evento registrado
    event, values = _VARS['window'].read()
    if event in (None, 'Exit'): # clic en el botón de Exit
        break

    #if event == 'NewMaze': 
    #    _VARS['playerPos'] = [0, 0]
    #    _VARS['cellMAP'] = makeMaze(_VARS['cellCount'], _VARS['cellCount'])
    
    # Filter key press
    xPos = int(math.ceil(_VARS['playerPos'][0]))
    yPos = int(math.ceil(_VARS['playerPos'][1]))    

    if checkEvents(event) == 'Up':
        if int(_VARS['playerPos'][1]) >= 0:
            if _VARS['cellMAP'][yPos-1][xPos] != 1:
                _VARS['playerPos'][1] = _VARS['playerPos'][1]
    elif checkEvents(event) == 'Down':
        if int(_VARS['playerPos'][1]) < _VARS['gridSize']-1:
            if _VARS['cellMAP'][yPos+1][xPos] != 1:
                _VARS['playerPos'][1] = _VARS['playerPos'][1]
    elif checkEvents(event) == 'Left':
        if int(_VARS['playerPos'][0]) >= 0:
            if _VARS['cellMAP'][yPos][xPos-1] != 1:
                _VARS['playerPos'][0] = _VARS['playerPos'][0]
    elif checkEvents(event) == 'Right':
        if int(_VARS['playerPos'][0]) < _VARS['gridSize']-1:
            if _VARS['cellMAP'][yPos][xPos+1] != 1:
                _VARS['playerPos'][0] = _VARS['playerPos'][0]

    # Limpiar canvas, dibujar malla y celdas
    _VARS['canvas'].TKCanvas.delete("all")
    drawGrid()
    drawCell(_VARS['playerPos'][0], _VARS['playerPos'][1], 'TOMATO')
    placeCells()

    # Check for Exit:
    xPos, yPos = _VARS['playerPos']
    if [xPos, yPos] == exitPos:
        _VARS['window']['-exit-'].update('Found the exit !')
    else:
        _VARS['window']['-exit-'].update('')

_VARS['window'].close()