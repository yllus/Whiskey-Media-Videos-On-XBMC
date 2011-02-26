# Python (system) imports.
import sys

# XBMC imports (if XBMC is present).
use_xbmc = 0
if use_xbmc == 1:
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
            return int(sys.argv[2])
        else:
            return 0
    getPath = Callable(getPath)
    
    def addDirectoryItem( name, handle, url ):
        if use_xbmc == 1:
            listItem = xbmcgui.ListItem(name)
            xbmcplugin.addDirectoryItem(handle, url, listItem)
        else:
            print "Item " + name + " points to URL " + url
    addDirectoryItem = Callable(addDirectoryItem)
    
    def endOfDirectory( handle ):
        if use_xbmc == 1:
            xbmcplugin.endOfDirectory(_handle)
        else:
            print "End of list."
    endOfDirectory = Callable(endOfDirectory)