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
        'para': ['images/background/mid-BG - forest.png', 'images/background/mid-BG - forest2.png']
    }
}