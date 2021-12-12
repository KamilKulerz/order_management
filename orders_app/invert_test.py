
my_node = {
    'value': 1,
    'left': {
        'value': 2,
        'left': {
            'value': 244,
            'left': {
                'value': 3,
                'left': {'value': 27},
                'right': {'value': 26}
            },
            'right': {
                'value': 4,
                'left': {'value': 25},
                'right': {'value': 24}
            }
        },
        'right': {
            'value': 233,
            'left': {
                'value': 5,
                'left': {'value': 23},
                'right': {'value': 22}
            },
            'right': {
                'value': 6,
                'left': {'value': 21},
                'right': {'value': 20}
            }
        }
    },
    'right': {
        'value': 7,
        'left': {
            'value': 211,
            'left': {
                'value': 8,
                'left': {'value': 19},
                'right': {'value': 18}
            },
            'right': {
                'value': 9,
                'left': {'value': 17},
                'right': {'value': 16}
            }
        },
        'right': {
            'value': 299,
            'left': {
                'value': 10,
                'left': {'value': 15},
                'right': {'value': 14}
            },
            'right': {
                'value': 11,
                'left': {'value': 12},
                'right': {'value': 13}
            }
        }
    }
}


def invert(node):
    if len(node.keys()) == 1:
        return node
    else:
        node['left'], node['right'] = node['right'], node['left']
        invert(node['left'])
        invert(node['right'])
    return node


print(invert(my_node))
