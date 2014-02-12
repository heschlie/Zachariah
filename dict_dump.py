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
        'para': {0: 'images/backgrounds/mid-BG - forest.png', 1: 'images/backgrounds/mid-BG - forest2.png'},
        'para_speed': {0: 3, 1: 1.5}
    }
}