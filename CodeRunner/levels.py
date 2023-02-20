# required score to reach the next level
reqs = [10, 20, float('inf')]

# enemies in each level

enemies = [
    ['fly', 'snail', 'lion', 'dragon'],
    ['fly', 'snail'],
    ['fly', 'snail', 'lion', 'dragon']
]

probabilities = [
    [1/2, 1/2, 0, 0],
    [1/4, 3/4],
    [1/6, 2/6, 2/6, 1/6]
]

# text input
texts = ['',

'''# Good job on your first run! You did good, but what if you could play perfectly? Let's try writing some code to help out.

# Below, you will see a function that has the player's x and y values as input, as well as info about each obstacle.

# 'info' is a list of tuples of the form (x, y, type), where x and y are coordinates and type is a string like "snail".

# The function should True if you wish to jump and False otherwise.

# Give this a shot!

def jump(x, y, info):
    ''',

'''# Great job coding! This is the last set level; try to see how far you can go!

# There are four types of obstacles, which you can distinguish based on their type: 'snail', 'fly', 'lion', and 'dragon'.

# Good luck!

def jump(x, y, info):
    '''
]