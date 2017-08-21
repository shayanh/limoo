import Queue
import json
import threading
import urllib
import requests

from cache import LimooCache

LYRICS_SERVER = 'ec2-52-26-245-255.us-west-2.compute.amazonaws.com'
cache = LimooCache()


class Lyrics(object):
    @staticmethod
    def get(artist, title):
        print 'get_lyrics --> %s by %s' % (title, artist)

        if cache.has(artist, title):
            lyrics = cache.read(artist, title)
            return lyrics

        get_vars = {'artist': artist, 'title': title}
        url = 'http://%s/lyrics?%s' % (LYRICS_SERVER, urllib.urlencode(get_vars))
        print url
        try:
            resp = requests.get(url, timeout=10)
        except requests.ReadTimeout:
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
                artist, title = self.queue.get(True, timeout=1)
                print 'Thread!', artist, title
                lyrics = Lyrics.get(artist, title)
                print lyrics
                self.queue.task_done()
            except Queue.Empty:
                continue

