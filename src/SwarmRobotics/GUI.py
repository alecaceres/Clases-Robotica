# basado en: https://k3no.medium.com/build-a-maze-with-python-920ac2266fe7 
import PySimpleGUI as sg
import numpy as np
import math
import random
import scipy.io as sio # para la lectura del .mat

AppFont = 'Any 16'
sg.theme('DarkGrey5')
_VARS = {'cellCount': 32, 'gridSize': 608, 'canvas': False, 'window': False,
         'playerPos': [1, 1], 'targetA': [23,9], 'targetB': [28,1], 'cellMAP': False}
cellSize = _VARS['gridSize']/_VARS['cellCount']
exitPos = [_VARS['cellCount']-1, _VARS['cellCount']-1]  



def makeMaze():
    mat_contents = sio.loadmat('./src/SwarmRobotics/mat/pista.mat')
    obstaculos = np.zeros((32,32)) # la matriz de obstáculos se extiende a 32x32
    obstaculos[1:31,1:31] = mat_contents['obstaculos'] # datos de entrada
    paredes = np.ones((32,32))
    paredes[1:31,1:31] = mat_contents['paredes']
    return obstaculos, paredes


_VARS['cellMAP'], _VARS['wallMAP'] = makeMaze() # cellMAP = obstáculos, wallMAP = paredes


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


def drawCell(x, y, color='GREY', text = ""):
    x *= cellSize
    y *= cellSize
    _VARS['canvas'].TKCanvas.create_rectangle(
        x, y, x + cellSize, y + cellSize,
        outline='BLACK', fill=color, width=1)
    if text: drawTextInCell(x, y, text)


def drawTextInCell(x, y, text, color="BLACK"):
    _VARS['canvas'].TKCanvas.create_text(x+cellSize/2,
                        y+cellSize/2, text=text, fill=color)

def drawRobot(x, y, direction):
    '''
    Dibuja el robot en el mapa

    x,y:        posición del vértice superior derecho del robot
    direction:  uno de los siguientes: UP, DOWN, LEFT, RIGHT
'''
    # Por defecto, se considera direction = UP
    FL = [x-1,y] # front left
    FR = [x, y] # front right
    RL = [x-1, y+1] # rear left
    RR = [x, y+1] # rear right
    if direction == "DOWN": # rotación de 180° con respecto a la orientación hacia arriba
        FL, FR, RL, RR = RR, RL, FR, FL
    elif direction == "LEFT": # rotación de -90° con respecto a la orientación hacia arriba
        FL, FR, RL, RR = FR, RR, FL, RL
    elif direction == "RIGHT": # rotación de 90° con respecto a la orientación hacia arriba
        FL, FR, RL, RR = RL, FL, RR, FR
    drawCell(*FL, color="#f6b26b", text = "FL")
    drawCell(*FR, color="#f6b26b", text = "FR")
    drawCell(*RL, color="#b6d7a8", text = "RL")
    drawCell(*RR, color="#b6d7a8", text = "RR")
    



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
           sg.Text('', key='-exit-', font=AppFont, size=(15, 1)),
           sg.Button('NewMaze', font=AppFont)]] # se dibuja el layout de la GUI

_VARS['window'] = sg.Window('Random Puzzle Generator', layout, resizable=True, finalize=True,
                            return_keyboard_events=True)
_VARS['canvas'] = _VARS['window']['canvas']
drawGrid() # se dibuja la malla 32x32
drawCell(_VARS['playerPos'][0], _VARS['playerPos'][1], 'TOMATO') # posición inicial del robot A
# drawCell(exitPos[0], exitPos[1], 'Black') # no hay celda de salida
drawRobot(4, 26, "UP")
drawCell(10, 18, '#290907')
placeCells()


while True:             # Event Loop
    event, values = _VARS['window'].read()
    if event in (None, 'Exit'):
        break

    #if event == 'NewMaze': 
    #    _VARS['playerPos'] = [0, 0]
    #    _VARS['cellMAP'] = makeMaze(_VARS['cellCount'], _VARS['cellCount'])
    
    # Filter key press
    xPos = int(math.ceil(_VARS['playerPos'][0]/cellSize))
    yPos = int(math.ceil(_VARS['playerPos'][1]/cellSize))    

    if checkEvents(event) == 'Up':
        if int(_VARS['playerPos'][1] - cellSize) >= 0:
            if _VARS['cellMAP'][yPos-1][xPos] != 1:
                _VARS['playerPos'][1] = _VARS['playerPos'][1] - cellSize
    elif checkEvents(event) == 'Down':
        if int(_VARS['playerPos'][1] + cellSize) < _VARS['gridSize']-1:
            if _VARS['cellMAP'][yPos+1][xPos] != 1:
                _VARS['playerPos'][1] = _VARS['playerPos'][1] + cellSize
    elif checkEvents(event) == 'Left':
        if int(_VARS['playerPos'][0] - cellSize) >= 0:
            if _VARS['cellMAP'][yPos][xPos-1] != 1:
                _VARS['playerPos'][0] = _VARS['playerPos'][0] - cellSize
    elif checkEvents(event) == 'Right':
        if int(_VARS['playerPos'][0] + cellSize) < _VARS['gridSize']-1:
            if _VARS['cellMAP'][yPos][xPos+1] != 1:
                _VARS['playerPos'][0] = _VARS['playerPos'][0] + cellSize

    # Clear canvas, draw grid and cells
    _VARS['canvas'].TKCanvas.delete("all")
    drawGrid()
    drawCell(exitPos[0], exitPos[1], 'Black')
    drawCell(_VARS['playerPos'][0], _VARS['playerPos'][1], 'TOMATO')
    placeCells()

    # Check for Exit:
    xPos = int(math.ceil(_VARS['playerPos'][0]/cellSize))
    yPos = int(math.ceil(_VARS['playerPos'][1]/cellSize))
    if [xPos, yPos] == exitPos:
        _VARS['window']['-exit-'].update('Found the exit !')
    else:
        _VARS['window']['-exit-'].update('')

_VARS['window'].close()