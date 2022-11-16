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
    config.num_generations = 250
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

    # Controls the scale for the map by multiplying the standard map by scale eg. scale 2 = 100 by 100 grid
    scale = 3
    config.grid_dims = (50*scale,50*scale) # must be a multiple of 50

    # sets the grid to a predefined initial state represeted as a 2d list of integers between 0 and 6
    config.initial_grid = drawInitialState(True, scale)

    # ----------------------------------------------------------------------

    # the GUI calls this to pass the user defined config
    # into the main system with an extra argument
    # do not change
    if len(args) == 2:
        config.save()
        sys.exit()
    return config

# Function that returns a 2d list of the initial states of the map
# includes a parameter to select whether fire is included
def drawInitialState(addFire, scale):
    initial_grid = np.full((50*scale,50*scale), 3)

    #generates the forest
    initial_grid = drawState(initial_grid,scale,[0,30],[25,15],2)
    initial_grid = drawState(initial_grid,scale,[15,45],[25,30], 2)

    #generates the lake
    initial_grid = drawState(initial_grid,scale,[5,33],[25,30],1)

    #generates the canyon
    initial_grid = drawState(initial_grid,scale,[30,45],[32,10],4)

    #generates the town
    initial_grid = drawState(initial_grid,scale,[18,7],[21,4],0)

    if addFire:
        # generates starting fire near the power plant
        #initial_grid = drawState(initial_grid,scale,[1,49],[4,48],6)

        # generates starting fire near the incinerator
        initial_grid = drawState(initial_grid,scale,[46,49],[49,48],6)

    return initial_grid

# Function that sets a rectangle of indices to a specified state
def drawState(grid, scale, topLeft, bottomRight, state):

    # scales the input appropriately
    topLeft[0] *= scale
    bottomRight[0] *= scale
    # reverses the y coordinate to allign with the map in the breif
    topLeft[1] = len(grid) - topLeft[1]*scale
    bottomRight[1] = len(grid) - bottomRight[1]*scale

    #sets the indices inside the rectangle to the specified state
    for i in range(topLeft[0], bottomRight[0]):
        for j in range(topLeft[1],bottomRight[1]):
            grid[j][i] = state

    return grid

def transition_function(grid, neighbourstates, neighbourcounts):
    """Function to apply the transition rules
    and return the new grid"""

    # These are some constant parameters that change different attributes about the simulation
    # controls how many neighbours need to be burning to catch fire
    CANYON_NEIGHBOURS = 1 #default 1
    CHAPARRAL_NEIGHBOURS = 2 #default 2
    FOREST_NEIGHBOURS = 3 #default 3

    # closer to 0 means it is more likely to catch fire
    CANYON_BURN_CHANCE = 0 #default 0
    CHAPARRAL_BURN_CHANCE = 0.3 #default 0.3
    FOREST_BURN_CHANCE = 0.8 #default 0.8

    # closer to 1 means it burns out faster
    CANYON_BURN_TIME = 1/2 #default 1
    CHAPARRAL_BURN_TIME = 1/14 #default 1/7
    FOREST_BURN_TIME = 1/60 #default 1/30

    # closer to 1 means it regrows faster
    CANYON_REGROWTH = 1/14 #default 1/14
    CHAPARRAL_REGROWTH = 1/30 #default 1/30

    scale = int(len(grid)/50)

    # Town 0, Lake 1, Forest 2, Chaparral 3, Canyon 4, Burnt 5, Burning 6

    # set the wind direction
    WIND_DIRECT = [1, 1]     # [north, east]

    # nw, n, ne, w, e, sw, s, se = neighbourstates # used for implementing wind
    wind_direct_weight = weightByWind(WIND_DIRECT)
    burning_weighted = ((neighbourstates==6) * wind_direct_weight[:, None, None]).sum(axis=0)

    # tn,lk,fr,ch,ca,bnt,burning = neighbourcounts
    burning = burning_weighted

    INITIAL_GRID = drawInitialState(False,scale)

    town = grid==0
    lake = grid==1

    # Calculates which cells should be burnt

    burningForest = (grid==6) & (INITIAL_GRID==2)
    burningChaparral = (grid==6) & (INITIAL_GRID==3)
    burningCanyon = (grid==6) & (INITIAL_GRID==4)

    burnt = (grid==5)

    burnt = burnt | (burningForest & randomMatrix(grid, FOREST_BURN_TIME))
    burnt = burnt | (burningChaparral & randomMatrix(grid, CHAPARRAL_BURN_TIME))
    burnt = burnt | (burningCanyon & randomMatrix(grid, CANYON_BURN_TIME))

    # calculates which cells should remain as they were
    forest = (grid==2) & (burning < FOREST_NEIGHBOURS)
    chaparral = (grid==3) & (burning < CHAPARRAL_NEIGHBOURS)
    canyon = (grid==4) & (burning < CANYON_NEIGHBOURS)

    forest = forest | (grid==2) & (burning >= FOREST_NEIGHBOURS) & randomMatrix(grid,FOREST_BURN_CHANCE)
    chaparral = chaparral | (grid==3) & (burning >= CHAPARRAL_NEIGHBOURS) & randomMatrix(grid,CHAPARRAL_BURN_CHANCE)
    canyon = canyon | (grid==4) & (burning >= CANYON_NEIGHBOURS) & randomMatrix(grid, CANYON_BURN_CHANCE)

    # Calculates which cells regrow
    chaparral = chaparral | (burnt & (burning == 0) &(INITIAL_GRID == 3) & randomMatrix(grid, CHAPARRAL_REGROWTH))
    canyon = canyon | (burnt & (burning == 0) &(INITIAL_GRID == 4) & randomMatrix(grid, CANYON_REGROWTH))

    # sets the entire grid to burning
    grid[:, :] = 6

    # alters the grid to add the other states back in based on the calculations above
    grid[town] = 0
    grid[lake] = 1
    grid[burnt] = 5
    grid[forest] = 2
    grid[chaparral] = 3
    grid[canyon] = 4
    

    return grid

def randomMatrix(grid, weight):
    ret = np.random.uniform(0,1,len(grid)*len(grid[0])).reshape(len(grid),len(grid[0])) < weight
    return ret

def weightByWind(wind_direction):
    wind_direction = np.array(wind_direction)
    wind_direction = wind_direction / np.linalg.norm(wind_direction)
    # nw, n, ne, w, e, sw, s, se
    eight_directions = np.array([
        [-1, 1],
        [0, 1],
        [1, 1],
        [-1, 0],
        [1, 0],
        [-1, -1],
        [0, -1],
        [1, -1],
    ])
    eight_directions = eight_directions / np.linalg.norm(eight_directions, axis=1)[:, None]
    weights = ((wind_direction[None, :] * eight_directions).sum(axis=-1) + 1.0)
    return weights


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
