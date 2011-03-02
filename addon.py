# Python (system) imports.
import sys
import os
import xml.dom.minidom
import urllib
from urlparse import urlparse

# Custom (this plugin) imports.
from Site import Site
from Feed import Feed
from SimplerXML import SimplerXML
from XBMCExtensions import XBMCExtensions

# Get environmental settings.
_path = sys.argv[0]
_pwd = os.getcwd()
_handle = XBMCExtensions.getHandle()
_argv = XBMCExtensions.getPath()

# Retrieve settings for the plugin.
plugin_id = 'plugin.video.whiskeymedia'
plugin_settings = XBMCExtensions.getSettings(plugin_id)
video_quality = plugin_settings.getSetting('video_quality')
wm_username = plugin_settings.getSetting('username')
wm_password = plugin_settings.getSetting('password')

# Store the list of sites and feeds inside them.
array_sites = []

# For the selected site and feed, create a list of menu items for the videos in the feed.
def displayVideoListing( name_site, name_feed ):
    # Turn the ENUM value for video quality into a named string.
    if video_quality == '1':
        vq = 'hd'
    elif video_quality == '2':
        vq = 'low'
    elif video_quality == '3':
        vq = 'mobile'
    else:
        vq = 'high'
    
    # Get the URL from the site's definition.
    url = ''
    for site in array_sites:
        if site.name == urllib.unquote_plus(name_site):
            for feed in site.feeds:
                if feed.name == urllib.unquote_plus(name_feed):
                    # Swap the username and password into the URL.
                    url = feed.urls[vq]
                    url = url.replace('${USERNAME}', wm_username)
                    url = url.replace('${PASSWORD}', wm_password)
    
    try:
        doc = xml.dom.minidom.parseString(urllib.urlopen(url).read())
    except:
        XBMCExtensions.showDialog('Error', 'Could not retrieve list of videos.', 'Please ensure your username/password is valid.')
        return 0
    
    # Iterate through the list of items in the feed.
    for node_item in doc.getElementsByTagName('item'):
        for node_title in node_item.getElementsByTagName('title'):
            title = SimplerXML.getText(node_title, 'title')
        for node_link in node_item.getElementsByTagName('link'):
            link = SimplerXML.getText(node_link, 'link')
        XBMCExtensions.addDirectoryItem(title, _handle, link, '', False)
        
    XBMCExtensions.endOfDirectory(_handle)

# For the selected site, create a list of menu items for the site's feeds.
def displayFeedListing( name_site ):
    for site in array_sites:
        if site.name == urllib.unquote_plus(name_site):
            for feed in site.feeds:
                path = _path + '?action=2&site=' + urllib.quote_plus(site.name) + '&feed=' + urllib.quote_plus(feed.name)
                XBMCExtensions.addDirectoryItem(feed.name, _handle, path, '', True)
            XBMCExtensions.endOfDirectory(_handle)

# For the top-level menu, create a list of menu items naming each of the Whiskey Media websites.
# Also create one menu item that opens the settings page.
def displaySiteListing():    
    for site in array_sites:
        path =  _path + '?action=1&site=' + urllib.quote_plus(site.name)
        XBMCExtensions.addDirectoryItem(site.name, _handle, path, _pwd + '/' + site.image, True)
    path =  _path + '?action=3'
    XBMCExtensions.addDirectoryItem('Change Settings', _handle, path, '', False)
    XBMCExtensions.endOfDirectory(_handle)

def getAuthenticationSuccess():
    url = array_sites[0].feeds[0]['high']
    try:
        urllib.urlopen(url).read()
    except:
        return 0
    return 1

# Get the value of a given URL parameter.
def getActionValue( name_action ):
    args_start = _argv.find('?') + 1
    args_end = len(_argv)
    args = _argv[args_start:args_end]
    params = args.split('&')
    for i in params:
        arr_action = i.split('=', 1)
        if arr_action[0] == name_action:
            return arr_action[1]

# Read a list of sites and feeds from an XML file into memory.
def getSitesAndFeeds():
    doc = xml.dom.minidom.parse(_pwd + '/sites.xml')
    
    # Iterate through the list of sites in the XML feed.
    for node_site in doc.getElementsByTagName('site'):
        # Instantiate a Site object and assign its name.
        site = Site()
        site.name = node_site.getAttribute('name')
        site.image = node_site.getAttribute('image')
    
        # Retrieve the name of each feed to build the top-level menu.
        for node_feed in node_site.getElementsByTagName('feed'):
            feed = Feed()
            feed.name = node_feed.getAttribute('name')
            for node_url in node_feed.getElementsByTagName('url'):
                url_quality = node_url.getAttribute('quality')
                feed.urls[url_quality] = SimplerXML.getText(node_url, 'url')
            site.feeds.append(feed)
    
        array_sites.append(site)

# Always load the list of sites and feeds.
getSitesAndFeeds()

# Call an action based on the parameters the script is run using.
if not _argv:
    displaySiteListing()
else:
    if getActionValue('action') == '1':
        displayFeedListing(getActionValue('site'))
    elif getActionValue('action') == '2':
        displayVideoListing(getActionValue('site'), getActionValue('feed'))
    elif getActionValue('action') == '3':
        plugin_settings.openSettings()
    else:
        displaySiteListing()

# If the username or password is left blank, pop up the settings screen.
if wm_username == '' or wm_password == '':
    plugin_settings.openSettings()