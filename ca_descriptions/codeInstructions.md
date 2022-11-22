
## Code Instructions

This file details how to launch and run our wildfire model as well as how to edit parameters in code to vary the results.
## To run the code:
    
**Add CA_Wild_fire to Capyle**
From our project .zip file, extract all and move __CA_Wild_Fire.py__ into __/ca_descriptions__ in your Capyle folder.

**Running the Simulation**
Launch Capyle and navigate to File/Open and click __CA_Wild_Fire.py__ .

The simulation should automatically generate the initial configuration so click __Save & Run configuration__.
If the button at the bottom of the panel is off the bottom of the screen, go to Simulation on the tool bar and click __Run Configuration_

## Changing Simulation Paramaters: 
In order to change parameters, you will need to change them in the code. You are free to change parameter as you 
wish but default values have been provided in comments so you can restore the original simulation.

**Change Setup Parameters** 
Open __CA_Wild_Fire.py__ in your preferred python editor and navigate to the __setup()__ method on *line 21*.
Inside this function you can edit Parameters for the simulation as a whole such as the title, scale or number of generations.

**Note that the simulation will need to be reloaded in Capyle in order for any setup changes to take effect.**

## Changing Model Parameters 
Open __CA_Wild_Fire.py__ as above and navigate to __transition_function(grid, neighbourstates, neighbourcounts)__ on *line 109*.

Below will be sets of parameters that will change aspects of the model, such as the neighbours requires for a terrain type to catch fire or 
the random weights to control how quickly each terrain type burns out once it catches to name a few. All of these parameters are clearly commented 
along with their default values so you can restore the default simulation should you wish to.

## Changing The Initial State 
Navigate to __drawInitialState()__ on *Line 67* in __CA_Wild_Fire.py__ as above. 
This method is responsible for creating the grid of values that will become the inital state. The method consists of several calls to the 
__drawState()__ method which is responsible for setting specific grid values to a given starting state.
It must be passed __initial_grid__ and __scale__ to calculate correctly as well as the coordinates of the top-left and bottom-rigth corners of the area
you would like to change, followed by the state you wish to change it to.

| terrain | state code |
| --- | --- |
| town | 0 |
| lake | 1 |
| forest | 2 |
| chaparral | 3 |
| canyon | 4 |
| burnt | 5 |
| burning | 6 |
