import os
import json

### TURN DETAILS ON AND DISABLE ORIGINAL GEO MODIFICATION
def details_ON(kwargs):

    # get node and window library directory from parameter
    parent = kwargs['node']
    dir = parent.parm('libraryDir').eval()
    
    # if the directory is empty - throw an error
    if not dir:
        raise hou.NodeError('No Path inputted: please input a path')
    
    # if the directory is not a valid - throw an error
    elif not os.path.isdir(dir):
        raise hou.NodeError('Path is not a valid directory, please input a valid directory')
        
    # if the directroy does not contain and subdirectories - throw an error
    elif not os.listdir(dir):
        raise hou.NodeError('Path does not have any window directories')
        
    # if the directory is OK
    else:  
        parent.parm('HIDE_TABS').set(1) # set the hide tabs parameter to 1 (controls the visibility of most tabs in the generator)
        parent.parm('input').set(1) # sets the switch turns the details ON

### TURN DETAILS OFF AND MODIFY ORIGINAL GEOMETRY
def details_OFF(kwargs): 
    parent = kwargs['node'] # get parent node
    parent.parm('input').set(0) # sets the switch to turn the details OFF
    parent.parm('HIDE_TABS').set(0) # sets the hide tabs paramter to 0 (controls the visibility of most tabs in the generator)
    
### Resets all parameters to default parameters set originally
def reset_to_defaults(kwargs):
    parent = kwargs['node'] # get parent ndoe
    
    # controls a value in a null node within the network
    # (since the value has changed it forces a recook of the calculations with the same seeds (thus resetting everything to the original values
    parent.parm('cacheinput').set(0)
    parent.parm('cacheinput').set(1) # set the value back to the original value 
    
# Selects an individual building (sets color to green)
def select_building(kwargs):
    parent = kwargs['node'] # get parent node
    buttonParm = kwargs['parm'] # get the paramter name where the button was pressed
    multiparm = buttonParm.parentMultiParm() # get the multi-parm
    instanceTuple = buttonParm.multiParmInstanceIndices() # get a tuple of what instances this button is a part of
    instance = instanceTuple[0] # the first instance of the tuple represents the instance of the first parent multiparm
    instanceNum = multiparm.evalAsInt() #get the amount of instances
    
    # loop through the range of instances
    for x in range(instanceNum):
    
        # create a list containing the names of the RGB paramters of the current iteration
        names = [
        'color' + str(x + 1) + 'r',
        'color' + str(x + 1) + 'g',
        'color' + str(x + 1) + 'b'
        ]
        
        # if the iteration is equal to the instance that the button was a parameter of
        if x + 1 == instance:
            parent.parm(names[0]).set(0) # set the color to (0, 1, 0) or GREEN
            parent.parm(names[1]).set(1)
            parent.parm(names[2]).set(0)
        else:
            parent.parm(names[0]).set(1) # set the color to (1, 1, 1) or WHITE
            parent.parm(names[1]).set(1)
            parent.parm(names[2]).set(1)


# THIS FUNCTION SETS THE WINDOW COLUMNS INSTANCES 
def window_Columns_MultiParm(kwargs):
    
    # get parent node and parent parm
    parent_node = kwargs['node']
    parent_parm = kwargs['parm']
    
    # get the current instance of the parent multiparm
    currentParentInstance = parent_parm.multiParmInstanceIndices()[0]
    
    # get the user inputted value for the needed window columns
    instancesNeeded = parent_parm.evalAsInt()
    
    # get the multiparm name by using the current instance
    multiparmName = 'windowColumns' + str(currentParentInstance)
    multiparm = parent_node.parm(multiparmName) # get the column multiparm
    
    # the needed columns is greater than the current columns set to TRUE
    if instancesNeeded > multiparm.evalAsInt():
        add = True
        
    # the needed columns is less than the current columns set to FALSE
    else:
        add = False
        
    # loop until the columns = the columns needed
    while instancesNeeded != multiparm.evalAsInt():
        
        # if add is true add an instance
        if add == True:
            multiparm.insertMultiParmInstance(multiparm.evalAsInt())
            
        # otherwise subtract an instance
        if add == False:
            multiparm.removeMultiParmInstance(multiparm.evalAsInt() - 1)
            
# LOADS THE LIRBARY FROM THE GIVEN PATH AND RETURNS AS LIST TO USE IN MENU PARAMETER
def loadLibraryMenu(dir): 
    
    # if the directory is empty
    if not dir:
        return []
    # if the path is not a directory
    elif not os.path.isdir(dir):
        return []
    
    # create a list
    window_dirs = []
    
    # loop throgh files in the passed library directory
    for window_dir in os.listdir(dir):
    
        # if the file is a directroy itself, get the path and add to the list
        if os.path.isdir(os.path.join(dir, window_dir)):
            window_dirs.append(window_dir)
    
    # sort the list alphabetically 
    window_dirs.sort(key=str.lower)
    
    # create a list for the menu items
    menu_items = []
    
    # loop throguht the range of window directories
    for i in range(len(window_dirs)):
    
        # append the iteration (represents the value in a menu)
        menu_items.append(str(i))
        
        # append the name of the window 
        menu_items.append(window_dirs[i])
        
    # return the menu
    return menu_items
    
# THIS FUNCTION TAKES A WINDOW DIRECTORY AND SETS PARAMETERS TO THE METADATA OF THE WINDOW
def loadContent(kwargs):

    # get parent node
    node = kwargs['node']
    
    # get the parm
    windowType_parm = kwargs['parm']
    
    # get the current instance of the multiparm
    instanceTuple = windowType_parm.multiParmInstanceIndices()
    instance = instanceTuple[0]
    
    # get the windowDepth and windowRatio parameters (these are container parameters for the metadata for SOPS to acess)
    windowDepth_parm = node.parm('windowDepth' + str(instance))
    windowRatio_parm = node.parm('windowRatio' + str(instance))
    
    # get the directory of the library
    dir = node.parm('libraryDir').eval()
    
    # get the number that the windowType represents
    windowNum = windowType_parm.eval()
    
    # get the label of the window (window name)
    parmLabels = windowType_parm.menuLabels()
    window_name = parmLabels[windowNum]
    
    # get the json directory by joining the directory, window name, and data.JSON file
    json_dir = os.path.join(dir, window_name, 'data.JSON')

    json_file = open(json_dir) # get the json file  
    json_content = json.load(json_file) # get the json content into python dict using json.load
    window_ratio = json_content['ratio'] # from the dict get the ratio
    window_depth = json_content['depth'] # from the dict get the depth
    
    windowDepth_parm.set(window_depth) # set the depth parameter to the depth
    windowRatio_parm.set(window_ratio) # set the ratio parameter to the ratio
        