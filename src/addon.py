# Python (system) imports.
import sys
import xml.dom.minidom
import urllib
from urlparse import urlparse

# XBMC imports.
import xbmcgui
import xbmcplugin

# Custom (this plugin) imports.
from Site import Site
from Feed import Feed
from SimplerXML import SimplerXML
from XBMCExtensions import XBMCExtensions

# Get environmental settings.
_path = sys.argv[0]
_handle = XBMCExtensions.getHandle()
_argv = sys.argv[2]

# Retrieve and set the video quality level.
video_quality = 'high'

# Store the list of sites and feeds inside them.
array_sites = []

def displayFeedListing( name_site ):
    listItem = xbmcgui.ListItem("Feed item")
    xbmcplugin.addDirectoryItem(_handle, '', listItem)
    xbmcplugin.endOfDirectory(_handle)

def displaySiteListing():    
    # Build the top-level directory containing the names of the various Whiskey Media websites.
    for site in array_sites:
        listItem = xbmcgui.ListItem(site.name)
        xbmcplugin.addDirectoryItem(_handle, _path + '?action=1&value=' + urllib.quote_plus(site.name), listItem)
        print site.name
    
    xbmcplugin.endOfDirectory(_handle)

def getActionValue( name_action ):
    o = urlparse(_argv)
    params = o.query.split('&')
    for i in params:
        arr_action = i.split('=', 1)
        if arr_action[0] == name_action:
            return arr_action[1]

def getSitesAndFeeds():
    doc = xml.dom.minidom.parse('sites.xml')
    
    # Iterate through the list of sites in the XML feed.
    for node_site in doc.getElementsByTagName('site'):
        # Instantiate a Site object and assign its name.
        site = Site()
        site.name = node_site.getAttribute('name')
    
        # Retrieve the name of each feed to build the top-level menu.
        for node_feed in node_site.getElementsByTagName('feed'):
            feed = Feed()
            feed.name = node_feed.getAttribute('name')
            for node_url in node_feed.getElementsByTagName('url'):
                url_quality = node_url.getAttribute('quality')
                feed.urls[url_quality] = SimplerXML.getText(node_url, 'url')
    
        array_sites.append(site)

# Always load the list of sites and feeds.
getSitesAndFeeds()

# Call an action based on the parameters the script is run using.
print "_argv = " + _argv
if not _argv:
    displaySiteListing()
else:
    if getActionValue('action') == '1':
        displayFeedListing(getActionValue('value'))
    elif getActionValue('action') == '2':
        print "Displaying the content of a feed."
    else
        displaySiteListing()