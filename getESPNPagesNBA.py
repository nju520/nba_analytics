"""
This file grabs complete play-by-play pages and box score pages for games
specified; run from terminal with:

python getESPNPagesNBA.py date|gameidfile|gameid [outputname]

where the first arg can be: a date with the form YYYYMMDD, a file containing
a list of ESPN game ids, or a single ESPN game id; the second, optional arg
is the root name of the output pickle files, one for the play-by-play raw
pages, and the other for the box score raw pages; data format is dictionaries
with the ESPN game ids as keys and the raw pages as values; if a date is used
as input, the program attempts to locate that page, and extracts the
ESPN game ids from the scores summary page for that date;
"""

import sys, os
import re
import datetime
import urllib2

from BeautifulSoup import BeautifulSoup as Soup

import toStrucDocESPNPages
'''
nba_root    = "http://scores.espn.go.com/nba/scoreboard?date=" + date
nba_pbp_all = "http://scores.espn.go.com/nba/playbyplay?gameId=" + gameID + "&period=0"
nba_box     = "http://scores.espn.go.com/nba/boxscore?gameId=" + gameID
ncaa_root   = "http://scores.espn.go.com/ncb/scoreboard?date=" + date
'''
'''Links and paths'''
nba_root        = "http://scores.espn.go.com/nba/scoreboard?date="
nba_ext         = "http://scores.espn.go.com/nba/recap?gameId="
nba_box         = "http://scores.espn.go.com/nba/boxscore?gameId="
nba_pbp         = "http://scores.espn.go.com/nba/playbyplay?gameId="
nba_shots       = "http://sports.espn.go.com/nba/gamepackage/data/shot?gameId="

ncaa_root       = "http://scores.espn.go.com/ncb/scoreboard?date="

default_path    = "/Users/sinn/NBA-Data-Stuff/DataFiles"

root_dict       = {'NBA':nba_root,
                   'NCAM':ncaa_root,
                   }
null_value      = '&nbsp;'
space_holder = u'\xc2\xa0'                  # curiousior and curiousior (sp?)
max_args        = 2


class NBAGame():


    def __init__(self, gameId,):
        self.gameId


    def retreiveData(self):
        self.retrieveRecap()
        self.retrievePBP()
        self.retrieveBoxScore()
        self.retrieveShots()


    def retrieveRecap(self):
        """
        Really this is the recap page, but also grabs some other info like game
        location and time, etc; also story analysis of game;
        """
        
        try:
            url = nba_ext + str(self.gameId)
            print url
            ext = toStrucDocESPNPages.structureESPNPage(url)
        except ValueError:
            # need some stuff to spit out error info...
            print('Failed to retreive recap for game ' + str(gameid))
            ext = dict()
        self.recap = ext
    

    def retrievePBP(self):
        """
        Given an ESPN game ID grabs play-by-play page, forms it into a
        structured doc;
        """
        
        try:
            url = nba_pbp + str(self.gameId) + "&period=0"
            print url
            pbp = toStrucDocESPNPages.structureESPNPage(url)
        except ValueError:
            # need some stuff to spit out error info...
            print('Failed to retreive play-by-play for game ' + str(gameid))
            pbp = dict()
        self.play_by_play = pbp
    

    def retrieveBoxScore(self):
        """
        Given an ESPN game ID grabs the box score feed page, turns it into
        a structured doc;
        """
        
        try:
            url = nba_box + str(self.gameId)
            print url
            box = toStrucDocESPNPages.structureESPNPage(url)
        except ValueError:
            # need some stuff to spit out error info...
            print('Failed to retreive box score for game ' + str(gameid))
            box = dict()
        self.box_score = box
        

    def retrieveShots(self):
        '''
        Given an ESPN game ID grabs the shot placement for the game; makes
        structured doc;
        '''
        try:
            url = nba_shots + str(self.gameId)
            print url
            shots = toStrucDocESPNPages.structureESPNPage(url)
        except ValueError:
            # need some stuff to spit out error info...
            print('Failed to retreive box score for game ' + str(gameid))
            shots = list()
        self.shot_locations = shots


###################

def runmain(gameids, argdict, out=False):
    """
    OH GOD WHYYYYY IS THIS HERE?!??!
    """
    
    pbp_store = dict()
    box_store = dict()
    #ext_stire = dict()
    sht_store = dict()
    '''Grab data from pages'''
    print "Grabbing data from pages..."
    for gameid in gameids:
        print('Grabbing game ' + str(gameid) + '...')
        pbp_store[gameid] = getpbp(gameid)
        box_store[gameid] = getbox(gameid)
        #ext_store[gameid] = getext(gameid)
        sht_store[gameid] = getshot(gameid)
    if out:
        print "Pages retreived; returning data..."
        return {'pbp':pbp_store,
                'box':box_store,
                'sht':sht_store}
    else:
        print "Pages retreived; storing data..."
        out_args = NBADB.NBADBHandle(pbp=pbp_store,
                                     box=box_store,
                                     ext=ext_store)
        return 1



'''For running from terminal;'''
if __name__=='__main__':
    """
    Default run from terminal; grab the text file with a list of game
    id's and get the raw pbp and box score pages for each; pickle results
    """
    args = sys.argv[1:]
    argdict = dict()
    argdict['date']     = args[0]
    argdict['outname']  = args[1]
    argdict['path'] = default_path
    if argdict:
        if argdict.has_key('file'): 
            if os.path.isfile(argdict['file']):
                gameids = getidsfile(argdict['file'])
            elif os.path.isfile(os.path.join(default_path, argdict['file'])):
                gameids = getidsfile(os.path.join(default_path, argdict['file']))
        elif argdict.has_key('date'):
            gameids = getidswebs(argdict['date'])
        if not gameids:
            msg = 'No valid game ids provided. Terminating program.'
            raise ValueError, msg
        else:
            '''If everything is OK up to this point, run the main code'''
            if runmain(gameids, argdict):
                print "Process complete."
                
