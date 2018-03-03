import bottle
import copy
import math
import os

SNAKE = 1
FOOD = 3

def dist(p, q):
    dx = abs(p[0] - q[0])
    dy = abs(p[1] - q[1])
    return dx + dy;

def prime_direction(from_cell, to_cell):
    dx = to_cell[0] - from_cell[0]
    dy = to_cell[1] - from_cell[1]

    if abs(dx) > abs(dy):
        if dx < 0:
            return 'left'
        else:
            return 'right'

    else:
        if dy < 0:
            return 'down'
        else:
            return 'up'

def closest(items, start):
    closest_item = None
    closest_distance = 10000

    # TODO: use builtin min for speed up
    for item in items:
        item_distance = distance(start, item)
        if item_distance < closest_distance:
            closest_item = item
            closest_distance = item_distance

    return closest_item

def init(data):
    grid = [[0 for col in xrange(data['height'])] for row in xrange(data['width'])]
    for snek in data['snakes']:
        for coord in snek['coords']:
            grid[coord[0]][coord[1]] = SNAKE
    mysnake = data['you']


    for f in data['food']:
        grid[f[0]][f[1]] = FOOD

    return mysnake, grid

@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.get('/')
def index():
    head_url = '%s://%s/static/Traitor.gif' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    return {
        'color': '#00ff00',
        'head': head_url
    }


@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data.get('game_id')
    board_width = data.get('width')
    board_height = data.get('height')

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )


    return {
        'color': '#00FF00',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url
    }


@bottle.post('/move')
def move():
    data = bottle.request.json
    snek, grid = init(data)
    things = data['food']
    my_coords = snek['coords']
    my_head = snek['coords'][0]
    goal = closest(food, my_head)
    return {
        'move': prime_direction(my_head, goal),
        'taunt': 'insert mike wazowski quote here'
    }


@bottle.post('/end')
def end():
    data = bottle.request.json

    # TODO: Do things with data

    return {
        'taunt': 'battlesnake-python!'
    }


application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
