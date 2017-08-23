from threading import Thread

import player
from server import sio, app
from lyrics import GetLyrics
from gi.repository import GLib


if __name__ == '__main__':
    plyr = player.get_player()
    plyr.on('metadata', player.on_track_change)
    lyricsd = GetLyrics(player.queue)
    server = Thread(target=sio.run, args=(app, ))

    lyricsd.setDaemon(True)
    server.setDaemon(True)
    lyricsd.start()
    server.start()

    player.queue.put((plyr.get_artist(), plyr.get_title()))
    GLib.MainLoop().run()

    lyricsd.join()
    server.join()
