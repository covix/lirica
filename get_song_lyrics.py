import plistlib
from PyLyrics import *
import os
import subprocess

LYRIC_FILE = 'songMeta.plist'


def clean_title(title):
    title = title.split(' - Live')[0]
    title = title.split(' - Remastered')[0]
    title = title.split(' - ')[0]
    return title


def main():
    current = None

    while True:
        command = ['osascript', 'get_current_track.applescript']
        subprocess.run(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        with open(LYRIC_FILE, 'rb') as f:
            pl = plistlib.load(f)

        artist = pl['artistName']
        title = pl['songName']

        title = clean_title(title)

        if (artist, title) == current:
            continue
            
        current = artist, title

        title_path = title.replace('/', ' ')

        artist_song_file = os.path.join('songs', artist, f'{title_path}.plist')
        os.makedirs(os.path.join('songs', artist), exist_ok=True)
        if not os.path.exists(artist_song_file):
            with open(artist_song_file, 'wb') as f:
                plistlib.dump(pl, f)

        print(f'{artist}: {title}')

        lyric_file = os.path.join('songs', artist, f'{title_path}.txt')
        try:
            lyrics = PyLyrics.getLyrics(artist, title)
            with open(lyric_file, 'w') as f:
                f.write(lyrics)
            print(lyrics)

        except ValueError as e:
            print(e)
            print(f'Artist: {artist}, Title: {title}')


if __name__ == '__main__':
    main()
