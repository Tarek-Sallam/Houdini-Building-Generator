node = hou.pwd()
geo = node.geometry()

#Find parent node
parent = node.parent().parent()

#Find iteration number
iteration = node.inputs()[1].geometry().intAttribValue('iteration')

#Find multiparm
multi_parm = parent.parm('buildings')

#dictionary for attributes matched to their paramter names
attribDict = {
    'storeys': geo.intAttribValue('storeyamount'),
    'roofType': geo.floatAttribValue('randSwitch'),
    'roofScale': geo.floatAttribValue('randScale'),
    'roofWidth': geo.floatAttribValue('randW'),
    'roofHeight': geo.floatAttribValue('randH'),
    'firstStoreyHeight': geo.floatAttribValue('firststoreyheight'),
    'storeyHeight': geo.floatAttribValue('storeyheight'),
    'storeyDivide': geo.floatAttribValue('storeyDivideON'),
    'storeyDivideAmount': geo.floatAttribValue('storeyDivideValue'),
    'firstFloorDivision': geo.floatAttribValue('storeyDivideFirstFloorON'),
    'firstFloorDivisionAmount': geo.floatAttribValue('storeyDivideFirstFloorValue'),
    'windowAmount': geo.intAttribValue('windowAmount'),
    'doorLoc' : geo.floatAttribValue('doorLoc'),
    'windowNum': geo.intAttribValue('windowNum'),
    'firstFloorWindowOn': geo.floatAttribValue('firstFloorWindowOn')
}


# for each key and value in the dictionary (attribute name, value) set the parameter of the instance to the value
for attribute, value in attribDict.items():
    name = attribute + str(iteration + 1)
    parent.parm(name).set(value)