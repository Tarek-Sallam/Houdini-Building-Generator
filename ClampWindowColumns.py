# get node and geo
node = hou.pwd()
geo = node.geometry()

#get the parent node (alleyway node)
alleyway_node = node.parent().parent()

# get the iteration from the for loop metadata
iteration = node.inputs()[1].geometry().intAttribValue('iteration')

# get the window value from the window menu paramter which controls the window type
window_value = alleyway_node.parm('windowNum' + str(iteration + 1))

# set the window type and execute the callback script which will update the other information of the window (depth, ratio)
alleyway_node.parm('windowType' + str(iteration + 1)).set(window_value)
alleyway_node.parm('windowType' + str(iteration + 1)).pressButton()