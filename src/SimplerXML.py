from xml.dom.minidom import Node

class Callable:
    def __init__( self, anycallable ):
        self.__call__ = anycallable
        
class SimplerXML:
    def getSubNodeText( nodelist, tagname ):
        retval = ''
        L = nodelist.getElementsByTagName(tagname)
        for node2 in L:
            for node3 in node2.childNodes:
                if node3.nodeType == Node.TEXT_NODE:
                    retval += node3.data
        return retval
    getSubNodeText = Callable(getSubNodeText)
    
    def getText( nodelist, tagname ):
        retval = ''
        for node2 in nodelist.childNodes:
            if node2.nodeType == Node.TEXT_NODE:
                retval += node2.data
        return retval
    getText = Callable(getText)
