## exports 0-4 LOD GEO and JSON metadata

import os
import json

# export function 
def exportGeo (kwargs):

    # get parent node
    parent = kwargs['node']
    
    #get the directory from the parm and the window name
    dir = parent.parm('windowLibraryPath').eval()
    window_dir = parent.parm('windowName').eval()
    
    # join the directory and the window name to get the new folders path
    path = os.path.join(dir, window_dir)
    
    # get the export and bevel parms
    export = parent.node("ROP_EXPORT")
    bevel = parent.node("BEVELS/bevel")
    
    # get current values for bevel and window
    currentBevelVal = parent.parm('bevelOn').eval()
    currentVal = parent.parm('showGlass').eval()

    # if the directory is empty, doesnt not exist, or if the window name already exists - throw error
    if not dir:
        raise hou.NodeError("Path is empty. Please input a path")
        
    elif not os.path.exists(dir):
        raise hou.NodeError("Path could not be written to. Please check that the path is valid.")
    
    elif os.path.exists(path):
        raise hou.NodeError("This window name already exists in this directory. Please change the name.")
    
    else:

        # set the glass and bevel to on as well as the bevel divisions to 6
        parent.parm('showGlass').set(1)
        parent.parm('bevelOn').set(1)
        parent.parm('bevel_divisions').set(6)

        # make the folder
        os.mkdir(path)
        
        # get the window ratio and window depth
        window_ratio = parent.parm('windowRatio').evalAsInt()
        window_depth = parent.node('WITH_ATTRIS').geometry().floatAttribValue('windowDepth')
        
        # put the data in a dictionary
        content = {
            "name": window_dir,
            "ratio": window_ratio,
            "depth": window_depth
        }
        
        # get the json directory
        json_dir = os.path.join(path, 'data.JSON')
        
        # open the json file for writing and dump the dictionary into the file
        with open(json_dir, 'w') as out:
            json.dump(content, out, indent = 4, sort_keys = True)
        
        # loop through 5 iterations
        for num in range(5):

            # filename is windowname + LOD + iteration + .fbx
            file = window_dir + '_LOD' + str(num) + '.fbx'

            # get file path from filename and path
            file_path = os.path.join(path, file)
            
            # if its the last iteration turn the bevel off
            if num == 4:
                parent.parm('bevelOn').set(0)
                
            # if its the first iteration set the bevel to 6
            elif num == 0:
                parent.parm('bevel_divisions').set(6)
                
            # if its the second iteration set the bevel to 4
            elif num == 1:
                parent.parm('bevel_divisions').set(4)
                
            # otherwise set the bevel to 4-num
            else:
                parent.parm('bevel_divisions').set(4-num)
                
            # set the output filepath
            parent.parm("sopoutput").set(file_path)
            
            #execute the rop export
            parent.parm("execute").pressButton()
        
        
        # set the glass on, bevel divisions and bevel on, back to what they were originally
        parent.parm('showGlass').set(currentVal)       
        parent.parm('bevel_divisions').set(3)
        parent.parm('bevelOn').set(currentBevelVal)
        