# Name: NAME
# Dimensions: 2

# --- Set up executable path, do not edit ---
import sys
import inspect
import random
this_file_loc = (inspect.stack()[0][1])
main_dir_loc = this_file_loc[:this_file_loc.index('ca_descriptions')]
sys.path.append(main_dir_loc)
sys.path.append(main_dir_loc + 'capyle')
sys.path.append(main_dir_loc + 'capyle/ca')
sys.path.append(main_dir_loc + 'capyle/guicomponents')
# ---

from capyle.ca import Grid2D, Neighbourhood, randomise2d
import capyle.utils as utils
import numpy as np


def setup(args):
    """Set up the config object used to interact with the GUI"""
    config_path = args[0]
    config = utils.load(config_path)
    # -- THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED --
    config.title = "Wild Fire CA"
    config.dimensions = 2
    config.states = [0,1,2,3,4,5,6]
    config.wrap = False
    # -------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----

    # Defines the colours that represent each state
    # Town 0, Lake 1, Forest 2, Chaparral 3, Canyon 4, Burnt 5, Burning 6
    townColour = (0,0,0) # Black
    lakeColour = (0,165/255,1) # Light Blue
    forestColour = (6/255,109/255,57/255) # Dark Green
    chaparralColour = (179/255,189/255,0) # Dark Yellow
    canyonColour = (1,1,0) # Yellow
    burntColour = (100/255,100/255,100/255) # Grey
    fireColour = (1,108/255,0) # Orange

    config.state_colors = [townColour,lakeColour,forestColour,chaparralColour,canyonColour,burntColour,fireColour]
    config.grid_dims = (50,50)

    # sets the grid to a predefined initial state represeted as a 2d list of integers between 0 and 6
    config.initial_grid = drawInitialState()

    # ----------------------------------------------------------------------

    # the GUI calls this to pass the user defined config
    # into the main system with an extra argument
    # do not change
    if len(args) == 2:
        config.save()
        sys.exit()
    return config

# Function that returns a 2d list of the initial states of the map
def drawInitialState():
    initial_grid = np.full((50,50), 3)

    #generates the forest
    initial_grid = drawState(initial_grid,[0,30],[25,15],2)
    initial_grid = drawState(initial_grid,[15,45],[25,30], 2)

    #generates the lake
    initial_grid = drawState(initial_grid,[5,33],[25,30],1)

    #generates the canyon
    initial_grid = drawState(initial_grid,[30,45],[32,10],4)

    #generates the town
    initial_grid = drawState(initial_grid,[18,7],[21,4],0)

    initial_grid = drawState(initial_grid,[1,49],[4,48],6)

    return initial_grid

# Function that sets a rectangle of indices to a specified state
def drawState(grid, topLeft, bottomRight, state):

    # reverses the y coordinate to allign with the map in the breif
    topLeft[1] = len(grid) - topLeft[1]
    bottomRight[1] = len(grid) - bottomRight[1]

    #sets the indices inside the rectangle to the specified state
    for i in range(topLeft[0], bottomRight[0]):
        for j in range(topLeft[1],bottomRight[1]):
            grid[j][i] = state

    return grid

def transition_function(grid, neighbourstates, neighbourcounts):
    """Function to apply the transition rules
    and return the new grid"""
    # constant parameters to control how many neighbours need to be burning to catch fire
    CANYON_NEIGHBOURS = 1 #default 1
    CHAPARRAL_NEIGHBOURS = 2 #default 2
    FOREST_NEIGHBOURS = 3 #default 3

    # constant parameters to control the threshold for the random chance a cell will catch fire
    # not yet implemented
    CANYON_BURN_CHANCE = 1 #default 1
    CHAPARRAL_BURN_CHANCE = 0.7 #default 0.7
    FOREST_BURN_CHANCE = 0.2 #default 0.2

    # constant parameters to control the threshold for the random length of time a cell will burn for

    CANYON_BURN_TIME = 1 #default 1 (1 day on average)
    CHAPARRAL_BURN_TIME = 1/7 #default 1/7 (1 week on average)
    FOREST_BURN_TIME = 1/30 #default 1/30 (1 month on average)

    # constant parameters to control the threshold for the random regrowth speed of Chaparral and Canyon
    # forest will not regrow in the timeframe of the simulation

    CANYON_REGROW = 1/7 #default 1/7 (1 week on average)
    CHAPARRAL_REGROW = 1/30 #default 1/30 (1 month on average)


    # Town 0, Lake 1, Forest 2, Chaparral 3, Canyon 4, Burnt 5, Burning 6
    newGrid = drawInitialState()
    
    for x in range (len(grid)):
        for y in range (len(grid[0])):

            # for lake state (doesn't burn at all) no transition function is required

            # no functions for town state either 

            # for canyon (catches fire very easily and burns quickly)
            if newGrid[x][y] == 4:
                
                # if enough neighbours are burning: burn
                if (neighbourstates==6).sum() >= CANYON_NEIGHBOURS and grid[x][y] == 4:
                    newGrid[x][y] = 6

                # sets the cell state to burnt if it was burning (weighted random)
                elif grid[x][y] == 6 and random.uniform(0,1) < CANYON_BURN_TIME:
                    newGrid[x][y] == 5

                # if the random failed then keep burning
                elif grid[x][y] == 6:
                    newGrid[x][y] = 6

                # regrows the cell to its initial state (weighted random)
                elif grid[x][y] == 5 and random.uniform(0,1) > CANYON_REGROW:
                    newGrid[x][y] = 5
                
            # for chaparral (catches fire quite easily and burns for longer)
            elif newGrid[x][y] == 3: 
            
                # if enough neighbours are burning: burn 
                if (neighbourstates==6).sum() >= CHAPARRAL_NEIGHBOURS and grid[x][y] == 3:
                    newGrid[x][y] = 6

                # sets the cell state to burnt if it was burning (weighted random)
                elif grid[x][y] == 6 and random.uniform(0,1) < CHAPARRAL_BURN_TIME:
                    newGrid[x][y] = 5

                # if the random failed then keep burning
                elif grid[x][y] == 6:
                    newGrid[x][y] = 6
                
                # regrows the cell to its initial state (weighted random)
                elif grid[x][y] == 5 and random.uniform(0,1) > CHAPARRAL_REGROW:
                    newGrid[x][y] = 5
            
            # for forest (doesn't catch fire easily but burns for a long time)
            elif newGrid[x][y] == 2: 

                # if enough neighbours are burning: burn
                if (neighbourstates==6).sum() >= FOREST_NEIGHBOURS and grid[x][y] == 2:
                    newGrid[x][y] = 6
                
                # sets the cell state to burnt if it was burning (weighted random)
                elif grid[x][y] == 6 and random.uniform(0,1) < FOREST_BURN_TIME:
                    newGrid[x][y] = 5

                # if the random failed then keep burning
                elif grid[x][y] == 6:
                    newGrid[x][y] = 6

                # regrows the cell to its initial state (weighted random)
                elif grid[x][y] == 5:
                    newGrid[x][y] = 5

    return newGrid


def main():
    """ Main function that sets up, runs and saves CA"""
    # Get the config object from set up
    config = setup(sys.argv[1:])

    # Create grid object using parameters from config + transition function
    grid = Grid2D(config, transition_function)

    # Run the CA, save grid state every generation to timeline
    timeline = grid.run()

    # Save updated config to file
    config.save()
    # Save timeline to file
    utils.save(timeline, config.timeline_path)

if __name__ == "__main__":
    main()
