Zachariah
=========

Zachariah is pre-alpha at the moment.  It will be a side scrolling platformer with some RPG elements to it, if all goes to plan.  This is our first project and is being developed by beginners, so the code may be sloppy but will hopefully work. 

Levels:

We have set Zachariah up to allow for custom built levels, the best way to do it is to use Tiled to make a level.

In order for it to work you will need to have at least 2 layers, 'terrain' and 'spawns' (without the quotes and case matters)
 the spawns layer need to be an object layer, and load a tilesheet using something like Pyxel Edit.  The tiles can be any 
size, and in theory can be rectangles (not tested yet) and in tiled you can make the map any size you would like.

Any ground or terrain that you want to be able to collide with, on a more or less pixel perfect level, you will need to
add to the terrain level, you walls, floor, ceiling, etc...  The spawns layer will be used to spawn the player, monsters, and
anything else you would like to spawn into the level that we have made classes for.  In order for that to work you will
need to add the 'object' to the map, right click it, and give it an attribe of enemy, and a value of the name of the monster
that you wish to spawn.