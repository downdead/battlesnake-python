import bottle
import copy
import math
import os

def dist(p, q):
    dx = abs(p['x'] - q['x'])
    dy = abs(p['y'] - q['y'])
    return dx + dy;

def circle(turn, radius):

    dir = turn%(4*(radius))
    if dir < (radius):
        return 'up'
    elif dir < (2*radius):
        return 'left'
    elif dir < (3*radius):
        return 'down'
    elif dir < (4*radius):
        return 'right'

def prime_direction(from_cell, to_cell):
    dx = to_cell['x'] - from_cell['x']
    dy = to_cell['y'] - from_cell['y']

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

    for item in items:
        item_distance = dist(start, item)
        if item_distance < closest_distance:
            closest_item = item
            closest_distance = item_distance

    return closest_item



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
    turn = data['turn']
    size = data['you']['length']
    if data['you']['health'] > 20:
        return {
            'move': circle(turn, int((size/4)+1)),
            'taunt': 'insert mike wazowski quote here'
        }
    else:
        things = data['food']['data']
        my_head = data['you']['body']['data'][0]
        goal = closest(things, my_head)
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
