import sys

class Callable:
    def __init__( self, anycallable ):
        self.__call__ = anycallable
        
class XBMCExtensions:
    def getHandle(self):
        if len(sys.argv) >= 2:
            return int(sys.argv[1])
        else:
            return 0
    getHandle = Callable(getHandle)