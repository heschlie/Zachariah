import monster
import npc
import environment

# Dict of monster classes
monsters = {
    'standing': monster.Standing,
    'walker': monster.Walker,
    'jumper': monster.Jumper
}

# Dict of NPC classes
npc = {
    'dino_male': npc.DinoMale
}

env = {
    'wind': environment.Wind
}

# Dict of levels and specific values for the level
levels = {
    'test': {
        'name': 'test',
        # Images for the parallax layers
        'para': {0: 'images/backgrounds/clouds.png',
                 1: 'images/backgrounds/mid-BG - forest.png',
                 2: 'images/backgrounds/mid-BG - forest2.png' },
        # Speed at which the parallax images...parallax
        'para_speed': {0: 6,
                       1: 4,
                       2: 2 },
        # Starting tuple (x, y) for each image
        'para_start': {0: (0, -70),
                       1: (0, 120),
                       2: (0, 120) },
        'para_offset': 880,
        'bg_color': (0, 191, 255)
    }
}