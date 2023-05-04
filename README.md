Uncle Stormtrooper<br />
~By Swapnil Srivastava
<br />
Introduction
<br />

Uncle Stormtrooper is a 2D platformer game centering around a stormtrooper in his mid-life crisis. We must help uncle stormtrooper navigate his way through a horde of monsters to reach his beloved dog. This game’s architecture and code were significantly changed in the last few days to make this game scalable. We hope to keep adding to the functionalities of this game to make it a complete 2d shooter platformer game.<br />

The game can be found here: https://github.com/swapnil1198s/Uncle-Stormtrooper
<br />
Requirements: pygame 2.1.3 (SDL 2.0.22, Python 3.8.3)
<br />
Instructions: <br />
After downloading the files and required software, run the uncle_stormtrooper.py file to play the game.<br />
Avoid touching monsters and getting hit by them<br /> 
Use the teleportation grenade to teleport at the destination where the grenade lands.<br />

 <img width="1440" alt="game_snap" src="https://user-images.githubusercontent.com/46658528/236312069-722c9b66-efd4-403b-be0f-7b467b6bc5ae.png">
 <br />
Controls:<br />
<br />
Up arrow key to Jump(tap when in air to double jump)<br />
Left Arrow key to Move character to the left<br />
Right Arrow Key to Move character to the right<br />
Tab to Throw teleportation grenade (If thrown, teleport to location of grenade)<br />
Mouseclick to Shoot<br />

Game Design<br />
Mechanics/Technology<br />
The gameplay loop housed within the main method acts as a controller of the game. The player inputs, game states, and updating of views is all handled by this game loop.<br />
The gimmick of this game is the use of a teleportation grenade. The player can teleport to the location of this grenade once it is thrown by pressing the spacebar.<br />
I think making the use of a teleportation grenade is not something I have seen in other platformer games.<br />


Story<br />
Uncle Stormtrooper is a 2D platformer game centering around a stormtrooper in his mid-life crisis. We must help uncle stormtrooper navigate his way through a horde of monsters to reach his beloved dog.<br />
	
Player Experience<br />
The player has to use good timing and coordination to get through the various map levels as falling results in instant death<br />
The player can shoot monster to increase their score<br />
The current score can be seen at the top of the screen <br />
Through the use of images to represent the various dynamic components of the game, the player’s experience is enhanced.<br />


Game Design Changes<br />
Although the original design for the game hoped for animation to be implemented, the tight timeline made it so that the functionality of the game was prioritized. The aiming mechanics for the bullets and grenades seemed to be challenging. They would work accurately to a certain extent but bug out in certain cases. So the aiming mechanics were omitted for this milestone. The game’s architecture and code was edited in the last few days to account for scalability. We hope to keep adding to the functionalities of this game to make it a complete 2d shooter platformer game. Including the implementation of different bullet types with varying aiming mechanics. The biggest challenge of the game development so far was tackling the moving components in the game in line with physics.
Game Development & Documentation<br />
The main() method acts as a controller for the game and handles all events including player input.<br />
The Player class is the model for our player object that moves around and jumps.<br />
This object has various properties such as speed, gravity, and vertical speed.<br />
The TeleportationGrenade class handles the view and model of the grenade object used for teleportation.<br />
The Box object is used to create the floor in varying combinations depending on the level.<br />
generate_floor() handles the arrangement of the boxes depending on the current level<br />
The Bullet object handles the view and behavior of the bullets fired.<br />
game_over() function handles the view and inputs for the game over screen<br />
The Monster class provides the model for different types of monsters and their characteristics. It also handles the behavior and view for monster entities.<br />
The Bullet class models the behavior and handles view of all fired bullets.<br />
Tools used: VS code and github<br />
Group Member Roles, Tasks, and Performance<br />
All work was done by myself<br />

Milestone 1:<br />
Task 1: Player Controller:<br />
Inputs via keyboards are now working to control the player movement.<br />
Implemented Jump, but restrictions apply.<br />
Double jump mechanics implemented<br />
Task 2: The floor and scene:<br />
The floor is implemented by a group of ‘box’ objects.<br />
Collision detection is implemented to prevent player from falling through the floor<br />
Design for other variations of the scene have been finished.<br />
Task 3: Bullet mechanics:<br />
Bullet mechanics are not finished and will roll over to the next milestone.<br />

Milestone 2: April 12<br />
Task 1: Bullet mechanics: Deadline: April 11<br />
Implemented shooting mechanism upon mouse click.<br />
Updated bullet functionality for simplification.<br />

Task 2: Monster mechanics: Deadline: April 11<br />
Implemented monster movement<br />
Implemented monster attacks and game termination on contact.<br />
Postponed termination of monsters to final submission<br />

Task 3: Make map sections 1 to 3: Deadline: April 11<br />
Implemented new map sections based on player position.<br />
These update once the player moves out of the screen edge. Giving a feeling of a larger world.<br />

Task 4: Polish up jumping mechanics”<br />
Jumps are no longer clunky.<br />
Double jumps are adjusted to fit the game map more appropriately.<br />
<br />
Final Game Submission: April 26<br />
Implemented different monster types<br />
Implemented the teleportation grenade.<br />
Implemented win condition.<br />
Completed and polished game<br />
Completed Game Document game<br />
Demo Video<br />
There is a video named gameplay.mov running through the game at: https://github.com/swapnil1198s/Uncle-Stormtrooper

