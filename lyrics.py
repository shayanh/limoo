import Queue
import json
import threading
import requests

from cache import LimooCache
from server import sio

LIMOO_SERVER = 'limoo.shayanh.ir'
cache = LimooCache()


class Lyrics(object):
    @staticmethod
    def get(artist, title):
        print 'get_lyrics --> %s by %s' % (title, artist)

        if cache.has(artist, title):
            lyrics = cache.read(artist, title)
            return lyrics

        # get_vars = {'artist': artist, 'title': title}
        # url = 'http://%s/lyrics?%s' % (LYRICS_SERVER, urllib.urlencode(get_vars))
        post_data = {'artist': artist, 'title': title}
        url = 'http://%s/lyrics' % LIMOO_SERVER
        print url
        try:
            # resp = requests.get(url, timeout=10)
            resp = requests.post(url, data=post_data, timeout=10)
        except:
            return 'Cannot connect to server :('
        if resp.status_code != 200:
            return 'No lyrics :('
        lyrics = json.loads(resp.content)['lyrics']
        cache.write(artist, title, lyrics)
        return lyrics


class GetLyrics(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            try:
                artist, title = self.queue.get(True)
                if not self.queue.empty():
                    self.queue.task_done()
                    continue
                sio.emit('song_data', {'artist': artist, 'title': title, 'lyrics': 'Loading...'})
                print 'Thread!', artist, title
                lyrics = Lyrics.get(artist, title)
                sio.emit('song_data', {'artist': artist, 'title': title, 'lyrics': lyrics})
                self.queue.task_done()
            except Queue.Empty:
                continue
