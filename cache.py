import os
import threading
from slugify import slugify

APP_NAME = 'limoo'


class LimooCache(object):
    def __init__(self):
        self.lock = threading.Lock()
        self.cache_dir = os.path.join(os.path.expanduser('~'), '.cache/', APP_NAME)
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def __get_filename(self, artist, title):
        slug = slugify(artist + ' ' + title)
        filename = os.path.join(self.cache_dir, slug)
        return filename

    def has(self, artist, title):
        filename = self.__get_filename(artist, title)
        return os.path.isfile(filename)

    def read(self, artist, title):
        if not self.has(artist, title):
            raise Exception('cannot read from cache')

        filename = self.__get_filename(artist, title)
        with open(filename, 'r') as f:
            lyrics = ''
            for line in f.readlines():
                lyrics += line
            return lyrics

    def write(self, artist, title, lyrics):
        filename = self.__get_filename(artist, title)
        lyrics = lyrics.encode('utf-8')
        with open(filename, 'w') as f:
            self.lock.acquire()
            f.write(lyrics)
            self.lock.release()

    def delete(self, artist, title):
        if not self.has(artist, title):
            return
        filename = self.__get_filename(artist, title)
        os.remove(filename)
