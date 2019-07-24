import plistlib
from PyLyrics import *
import os
import subprocess

LYRIC_FILE = 'songMeta.plist'


def main():
    current = None

    while True:
        command = ['osascript', 'get_current_track.applescript']
        subprocess.run(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        with open(LYRIC_FILE, 'rb') as f:
            pl = plistlib.load(f)

        artist = pl['artistName']
        title = pl['songName']

        if (artist, title) == current:
            continue
            
        current = artist, title

        artist_song_file = os.path.join('songs', artist, f'{title}.plist')
        os.makedirs(os.path.join('songs', artist), exist_ok=True)
        if not os.path.exists(artist_song_file):
            with open(artist_song_file, 'wb') as f:
                plistlib.dump(pl, f)

        print(f'{artist}: {title}')

        lyric_file = os.path.join('songs', artist, f'{title}.txt')
        lyrics = PyLyrics.getLyrics(artist, title)

        # check if not none
        with open(lyric_file, 'w') as f:
            f.write(lyrics)

        print(lyrics)


if __name__ == '__main__':
    main()
