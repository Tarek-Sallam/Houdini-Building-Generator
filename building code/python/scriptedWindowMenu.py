node = hou.pwd()
dir = node.parm('libraryDir').eval()

return node.hdaModule().loadLibraryMenu(dir)