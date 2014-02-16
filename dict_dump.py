import monster
import npc

monsters = {
    'standing': monster.Standing,
    'walker': monster.Walker,
    'jumper': monster.Jumper
}

npc = {
    'dino_male': npc.DinoMale
}

levels = {
    'test': {
        'name': 'test',
        'para': {0: 'images/backgrounds/clouds.png', 1: 'images/backgrounds/mid-BG - forest.png', 2: 'images/backgrounds/mid-BG - forest2.png'},
        'para_speed': {0: 6, 1: 4, 2: 2},
        'para_start': {0: (0, -70), 1: (0, 120), 2: (0, 120) }
    }
}