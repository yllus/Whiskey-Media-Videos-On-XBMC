# Python (system) imports.
import sys

# XBMC imports.
import xbmcgui
import xbmcplugin
import xbmcaddon

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
    
    def showDialog( heading, line1, line2 ):
        dialog = xbmcgui.Dialog()
        ok = dialog.ok(heading, line1, line2)
    showDialog = Callable(showDialog)
    
    def getSettings( plugin_id ):
        return xbmcaddon.Addon(plugin_id)
    getSettings = Callable(getSettings)
    
    def addDirectoryItem( name, handle, url, image, isfolder ):
        listItem = xbmcgui.ListItem(name)
        if image != '':
            listItem.setIconImage(image)
        xbmcplugin.addDirectoryItem(handle, url, listItem, isfolder)
    addDirectoryItem = Callable(addDirectoryItem)
    
    def endOfDirectory( handle ):
        xbmcplugin.endOfDirectory(handle)
    endOfDirectory = Callable(endOfDirectory)