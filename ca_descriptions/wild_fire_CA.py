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
    # -------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----

    # town,lake,Forest,chaparral,canyon,burnt,burning
    townColour = (0,0,0)
    lakeColour = (0,165/255,1)
    forestColour = (6/255,109/255,57/255)
    chaparralColour = (179/255,189/255,0)
    canyonColour = (1,1,0)
    burntColour = (20/255,20/255,20/255)
    fireColour = (1,108/255,0)

    config.state_colors = [townColour,lakeColour,forestColour,chaparralColour,canyonColour,burntColour,fireColour]
    config.grid_dims = (50,50)

    config.initial_grid = np.full(config.grid_dims, 3)

    drawInitialState(config)

    # ----------------------------------------------------------------------

    # the GUI calls this to pass the user defined config
    # into the main system with an extra argument
    # do not change
    if len(args) == 2:
        config.save()
        sys.exit()
    return config

def drawInitialState(config):
    #generate the forest
    drawState(config,[0,30],[25,15],2)
    drawState(config,[15,45],[25,30], 2)
    
    #generate the lake
    drawState(config,[5,33],[25,30],1)

    #generate the canyon
    drawState(config,[30,45],[32,10],4)

    #generate the town
    drawState(config,[18,7],[21,4],0)

def drawState(self, topLeft, bottomRight, state):
    topLeft[1] = self.grid_dims[1] - topLeft[1]
    bottomRight[1] = self.grid_dims[1] - bottomRight[1]

    for i in range(topLeft[0], bottomRight[0]):
        for j in range(topLeft[1],bottomRight[1]):
            self.initial_grid[j][i] = state

def transition_function(grid, neighbourstates, neighbourcounts):
    """Function to apply the transition rules
    and return the new grid"""
    # YOUR CODE HERE
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