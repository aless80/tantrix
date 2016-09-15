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
possible to manually resize the board?
add shifts to history
impossible tile: it avoids that, but problem after it. see bug
Final phase: 
	if cfg.turnUpDown < 44 - 12:
Help button
Dialogs: colors for solitaire
	confirm dialog when quit
	winner is..
Quit game goes back to room


#BUG
1 forced tile is shown even if it leads to an impossible place because of 3 colors
	highlight_forced_and_matching finds matches for forced spaces. There, check if each match is_confirmed.
	first change find_matching_tiles to also yield the necessary rotations
	then run is_confirmed with the new tile virtually stored

#BUG when after a move there is a forced tile. also in tantrix12
	post_confirm see 
		TODO this fails when forced is after a move!