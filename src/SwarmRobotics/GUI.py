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
         'player1Pos': [[4, 27], [5, 27], [4, 28], [5, 28]]} # FL, FR, RL, RR
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

def getOccupiedCells():
    full = _VARS['cellMAP'].T + _VARS['wallMAP'].T
    robots = [pos for key in _VARS if key.endswith("Pos") for pos in _VARS[key] if isinstance(pos,list)]
    for xpos,ypos in robots: full[xpos,ypos] = 1
    return full


_VARS['cellMAP'], _VARS['wallMAP'] = makeMaze() # cellMAP = obstáculos, wallMAP = paredes
for i in range(1,8):
    x,y = [random.choice(range(1,31)), random.choice(range(1,31))] # coordenadas de FR
    full=getOccupiedCells()
    while True:
        is_empty = not (full[x,y])
        if is_empty:
            direction = []
            if not (full[x-1,y] or full[x,y+1] or full[x-1,y+1]): direction.append("UP")
            if not (full[x+1,y] or full[x,y-1] or full[x+1,y-1]): direction.append("DOWN")
            if not (full[x+1,y] or full[x,y+1] or full[x+1,y+1]): direction.append("LEFT")
            if not (full[x-1,y] or full[x,y-1] or full[x-1,y-1]): direction.append("RIGHT")
            if direction:
                chosenDirection = random.choice(direction)
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

def getDirection(FL, FR, RL, RR = None):
    if FL[0]==RL[0] and FR[0]==RR[0] and FL[1]<RL[1]: return "UP"
    if FL[0]==RL[0] and FR[0]==RR[0] and FL[1]>RL[1]: return "DOWN"
    if FL[1]==RL[1] and FR[1]==RR[1] and FL[0]>RL[0]: return "RIGHT"
    if FL[1]==RL[1] and FR[1]==RR[1] and FL[0]<RL[0]: return "LEFT"
    return None

def scan(FL, FR, direction, robotNum=1):
    '''
    Devuelve una lista de distancias conocidas a los siguientes obstáculos,
    proveídas por el sensor ultrasonido
    '''
    full = getOccupiedCells()
    for x,y in _VARS[f'player{robotNum}Pos']: full[x,y]=0
    dist_next_obst = [float("inf")]*4 # 4 valores, de izquierda a derecha del frente del robot (es una distancia)
    [FLx, FLy], [FRx, FRy] = FL, FR
    if direction == "UP":
        for j,x in enumerate([FLx-1, FLx, FRx, FRx+1]):
            for i in range(1,4):
                print(i)
                y = FLy if j<=2 else FRy
                print(f"({x},{y-i}): {full[x,y-i]}")
                if full[x,y-i]: dist_next_obst[j] = i; break
    if direction == "DOWN":
        for j,x in enumerate([FLx+1, FLx, FRx, FRx-1]):
            for i in range(1,4):
                y = FLy if j<=2 else FRy
                if full[x,y+i]: dist_next_obst[j] = i; break
    if direction == "LEFT":
        for j,y in enumerate([FLy+1, FLy, FRy, FRy-1]):
            for i in range(1,4):
                x = FLx if j<=2 else FRx
                if full[x+i,y]: dist_next_obst[j] = i; break
    if direction == "RIGHT":
        for j,y in enumerate([FLy+1, FLy, FRy, FRy-1]):
            for i in range(1,4):
                x = FLx if j<=2 else FRx
                if full[x-i,y]: dist_next_obst[j] = i; break
    return dist_next_obst

def rotateRobot(angle, direction, robotNum = 1):
    FL, FR, RL, RR = _VARS[f'player{robotNum}Pos']
    if angle == 90: FL, FR, RL, RR = RL, FL, RR, FR
    elif angle == -90: FL, FR, RL, RR = FR, RR, FL, RL
    elif angle == 45:
        if direction == "UP": FR, RR = [FR[0],FR[1]-1], [RR[0],RR[1]-1]
        elif direction == "DOWN": FR, RR = [FR[0],FR[1]+1], [RR[0],RR[1]+1]
        elif direction == "LEFT": FR, RR = [FR[0]-1,FR[1]], [RR[0]-1,RR[1]]
        elif direction == "RIGHT": FR, RR = [FR[0]+1,FR[1]], [RR[0]+1,RR[1]]
    elif angle == -45:
        if direction == "DOWN": FR, RR = [FR[0],FR[1]-1], [RR[0],RR[1]-1]
        elif direction == "UP": FR, RR = [FR[0],FR[1]+1], [RR[0],RR[1]+1]
        elif direction == "RIGHT": FR, RR = [FR[0]-1,FR[1]], [RR[0]-1,RR[1]]
        elif direction == "LEFT(": FR, RR = [FR[0]+1,FR[1]], [RR[0]+1,RR[1]]
    _VARS[f'player{robotNum}Pos'] = [FL, FR, RL, RR]
    return

def moveRobot(robotNum = 1):
    '''
    Esta función permite al robot desplazarse a una siguiente posición
    '''
    xdest, ydest = _VARS['targetB']
    FL, FR, RL, RR = _VARS[f'player{robotNum}Pos']
    direction = getDirection(FL, FR, RL, RR)
    dist_next_obst = scan(FL, FR, direction)
    print(dist_next_obst)
    dist_act = abs(xdest-FR[0])+abs(ydest-FR[1]) # aproximación con distancia Manhattan actual
    if dist_next_obst[1] == 1 or dist_next_obst == 1: # si el frente está cubierto
        if FL[0]==FR[0] or FL[1]==FR[1]: # rotar 90°. Si no: retroceder
            if dist_next_obst[0] > dist_next_obst[3]: rotateRobot(90, direction=direction); return
            rotateRobot(-90, direction=direction); return
        if direction == "UP":
            if FL[1]>FR[1]: rotateRobot(-45, direction=direction); return
            rotateRobot(45, direction=direction); return
        if direction == "DOWN":
            if FL[1]>FR[1]: rotateRobot(45, direction=direction); return
            rotateRobot(-45, direction=direction); return
        if direction == "LEFT":
            if FL[0]>FR[0]: rotateRobot(-45, direction=direction); return
            rotateRobot(45, direction=direction); return
        if direction == "RIGHT":
            if FL[0]>FR[0]: rotateRobot(45, direction=direction); return
            rotateRobot(-45, direction=direction); return
    if FL[0]==FR[0] or FL[1]==FR[1]:
        rotateRobot(45, direction=direction); return
    
    rotateRobot(-45, direction=direction)    

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
        moveRobot()

    # Limpiar canvas, dibujar malla y celdas
    _VARS['canvas'].TKCanvas.delete("all")
    drawGrid()
    placeCells()
    drawTargets()
    drawDummyRobots()
    placeCells()
    drawRobot(1)

    # Check for Exit:
    xPos, yPos = _VARS['playerPos']
    if [xPos, yPos] == exitPos:
        _VARS['window']['-exit-'].update('Found the exit !')
    else:
        _VARS['window']['-exit-'].update('')

_VARS['window'].close()