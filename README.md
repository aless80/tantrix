# Tantrix
Python code for the Tantrix game

## Launch server and two clients
cd ~/tantrix/
python ./server.py
python ./tantrix.py
python ./tantrix.py

## Description of version 12
Fixed several bugs with change of turn, see post_confirm in deck.py. cfg.history records the moves.
->A known bug to fix happens when a forced tile cannot be placed because it causes an impossible tile with three colors. 
Player name cannot be already taken and must start with non-numeric character
Seed for random generator is decided by server when game starts. No seed if solitaire (or 0 seed for testing)
Score was broken, now it works again
Added confirm property in Tile object so that you cannot place a table in tab1 to tab2 or viceversa.
I removed or commented cfg.TRYING
remove rowcol from playConfirmedMove. NB: in server.py I commented this: self._confirmedgame.append(rowcolnum)
Improved waiting room title and changing name
gameinprogress is now in config so that I can use it everywhere with no problems
All classes extend object

## TODO
impossible tile: clean code. get_neighboring_colors needs rct_rot_num_obl
possible to manually resize the board? sticky = (N,S,E,W) but it is on canvas not on create_rectangle (#cover canvas on the right)
Final phase: 
	if cfg.turnUpDown < 44 - 12:
Help button
Chat
Server occasionally checks clients
Dialogs:
	confirm dialog when quit
	winner is..
Quit game goes back to room
