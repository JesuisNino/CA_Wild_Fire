# Name: NAME
# Dimensions: 2

# --- Set up executable path, do not edit ---
import sys
import inspect
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
    #config.wrap = False
    # -------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----

    # town,lake,Forest,chaparral,canyon,burnt,burning
    townColour = (0,0,0)
    lakeColour = (0,165/255,1)
    forestColour = (6/255,109/255,57/255)
    chaparralColour = (179/255,189/255,0)
    canyonColour = (1,1,0)
    burntColour = (100/255,100/255,100/255)
    fireColour = (1,108/255,0)

    config.state_colors = [townColour,lakeColour,forestColour,chaparralColour,canyonColour,burntColour,fireColour]
    config.grid_dims = (50,50)

    config.initial_grid = drawInitialState()

    # ----------------------------------------------------------------------

    # the GUI calls this to pass the user defined config
    # into the main system with an extra argument
    # do not change
    if len(args) == 2:
        config.save()
        sys.exit()
    return config

def drawInitialState():
    initial_grid = np.full((50,50), 3)

    #generate the forest
    initial_grid = drawState(initial_grid,[0,30],[25,15],2)
    initial_grid = drawState(initial_grid,[15,45],[25,30], 2)

    #generate the lake
    initial_grid = drawState(initial_grid,[5,33],[25,30],1)

    #generate the canyon
    initial_grid = drawState(initial_grid,[30,45],[32,10],4)

    #generate the town
    initial_grid = drawState(initial_grid,[18,7],[21,4],0)

    return initial_grid

def drawState(grid, topLeft, bottomRight, state):
    topLeft[1] = len(grid) - topLeft[1]
    bottomRight[1] = len(grid) - bottomRight[1]

    for i in range(topLeft[0], bottomRight[0]):
        for j in range(topLeft[1],bottomRight[1]):
            grid[j][i] = state

    return grid

def transition_function(grid, neighbourstates, neighbourcounts):
    """Function to apply the transition rules
    and return the new grid"""
    #need to store the initial state 

    # for lake state (doesn't burn at all)
    # stay lake no matter what the neighbourhood is

    # for canyon (catches fire very easily and burns out quickly)
    # if >0 neighbours are burning: burn
    # if initial was canyon and currently burning: burnt

    # for chaparral (catches fire quite easily and burns for longer)
    # if >1 neighbours are burning: burn (more likely to catch fire if northern neighbours are burning) 

    # for forest (doesn't catch fire easily but burns for a long time)
    # if >2 neighbours are burning: burn (more likely to catch fire if northern neighbours are burning) 

    return grid


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
