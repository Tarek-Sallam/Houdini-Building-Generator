# get node and geo
node = hou.pwd()
geo = node.geometry()

# get parent node (alley way gen node)
parent = node.parent().parent()

# get the multiparm
parent_multiparm = node.parm('buildings')

# find the iteration by referencing the detail attribute of the for loop metadata node
iteration = node.inputs()[1].geometry().intAttribValue('iteration')

# define the multiparm name by using the iteration value
multiparm_name = 'windowColumns' + str(iteration + 1)

# get the paramter needed to access
multiparm = parent.parm(multiparm_name)

# unhide the paramter
multiparm.hide(False)

# get the column instances attriute value
columninstances = geo.intAttribValue('windowAmount')


# for each iteration, insert an instnace into the multiparm and set it to the attribute value calculated
for instance in range(columninstances):
    multiparm.insertMultiParmInstance(instance)
    columnVal = geo.intAttribValue('column' + str(instance))
    name = 'window_column' + str(iteration + 1) + '_' + str(instance + 1)
    parent.parm(name).set(columnVal)