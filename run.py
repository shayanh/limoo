from threading import Thread

from player_utils import on_track_change, queue, player
from server import run_server
from lyrics import GetLyrics
from gi.repository import GLib

if __name__ == '__main__':
    player.on('metadata', on_track_change)
    lyricsd = GetLyrics(queue)
    server = Thread(target=run_server)

    lyricsd.setDaemon(True)
    server.setDaemon(True)
    lyricsd.start()
    server.start()

    GLib.MainLoop().run()

    lyricsd.join()
    server.join()
