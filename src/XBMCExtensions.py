# Python (system) imports.
import sys

# XBMC imports (if XBMC is present).
import xbmcgui
import xbmcplugin

class Callable:
    def __init__( self, anycallable ):
        self.__call__ = anycallable
        
class XBMCExtensions:
    def getHandle():
        if len(sys.argv) >= 2:
            return int(sys.argv[1])
        else:
            return 0
    getHandle = Callable(getHandle)
    
    def getPath():
        if len(sys.argv) >= 3:
            return sys.argv[2]
        else:
            return ''
    getPath = Callable(getPath)
    
    def addDirectoryItem( name, handle, url, image, isfolder ):
        listItem = xbmcgui.ListItem(name, image, image)
        xbmcplugin.addDirectoryItem(handle, url, listItem, isfolder)
    addDirectoryItem = Callable(addDirectoryItem)
    
    def endOfDirectory( handle ):
        xbmcplugin.endOfDirectory(handle)
    endOfDirectory = Callable(endOfDirectory)