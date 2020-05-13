# Animal-Crossing-Critter-Crosser
A program which sorts and compiles HTML charts of critters from the game Animal Crossing: New Horizons.
The program has a GUI which opens up and allows the user to set the parameters for their game.
The user may then generate an HTML chart which will display the list of critters based on the parameters chosen.

# Status
The program is (as far as I know) stable and functional. I'm new to using Git so there's a chance that something will have gone wrong in the uploading and implementation of the program, though I will address it as I go.

# Plans and Intentions
The program, when built into an EXE file (one file, not one dir), takes a very long time to open. The program was written originally as a console application and became significantly more complex in a feat of unwarranted confidence. Because of this, certain things are still present which are not necessary to be in the main build.
Particularly the generation and loading of the dictionaries each time the program is run is unnecessary. This is static data which will not change. Because of that, it should be built and then saved in a way that can be retrieved without regeneration. Doing this will allow me to remove a couple imports from the gui module (such as pandas) to ideally save some boot time. It may not improve much, though it's still a good exercise in refactoring this code.

I also need to remove functions which are no longer used (from the initial console version), or could be cleaned up or placed in a better home. This is my first project which is moderately complex and perhaps the messiness exhibits that.

# Image Credits
Icons -
	Leaf Icon (Not present on GitHub but I use it when building an EXE)
	https://nookipedia.com/wiki/File:Animal_Crossing_Symbol.png

Fish and Bugs icons are taken from their respective pages on the Animal Crossing Wiki.
  https://animalcrossing.fandom.com/wiki/Fish_(New_Horizons)
  https://animalcrossing.fandom.com/wiki/Bugs_(New_Horizons)

Backgrounds -
	Wood Texture
	https://www.nintendo.es/Juegos/Nintendo-Switch/Animal-Crossing-New-Horizons-1438623.html

	Blue and Green Colored Shapes
	https://www.wallpaperflare.com/animal-crossing-animal-crossing-new-leaf-pattern-logo-minimalism-wallpaper-cmtaw
	(Several Links on that same page)
