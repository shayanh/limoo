import Queue
# import gi
import os, sys, commands
from subprocess import Popen, PIPE
import threading
from threading import Thread, Timer

# gi.require_version('Playerctl', '1.0')
# from gi.repository import Playerctl, GLib

queue = Queue.Queue()

PLAYER_NAMES = ['spotify', 'rhythmbox', 'vlc', ]  # order is important
    
# def get_player():
#     for player_name in PLAYER_NAMES:
#         player_instance = Playerctl.Player(player_name=player_name)
#         if player_instance.props.status is not None:
#             return player_instance
#     player_instance = Playerctl.Player(player_name=PLAYER_NAMES[0])
#     return player_instance

class Player(object):
    def __init__(self, newTitle, newArtist):
        self.title = newTitle
        self.artist = newArtist
        self.status = "Stopped"

    def get_artist(self):
        return self.artist

    def get_title(self):
        return self.title

player = Player("", "")

class GetPlayer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.timer = None
        self.lastTrack = ""

    def run(self):
        self.timer = Timer(5.0, self.run)
        self.timer.start()
        q = Popen(['osascript', './player.scpt'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True).communicate()
        p = ''.join(q)
        if p == "Stopped\n":
            player.status = "Stopped"
            return
        p = p.split("|")
        player.artist = p[0]
        player.title = p[1]
        player.status = "Playing"
        currTrack = player.artist + "|" + player.title
        if currTrack != self.lastTrack:
            print 'Now playing:'
            print '{artist} - {title}'.format(artist=player.artist, title=player.title)
            queue.put((player.artist, player.title))
            self.lastTrack = currTrack

# def on_track_change(player, e):
#     artist = player.get_artist()
#     title = player.get_title()
#     print 'Now playing:'
#     print '{artist} - {title}'.format(artist=artist, title=title)
#     queue.put((artist, title))

# player = get_player()

