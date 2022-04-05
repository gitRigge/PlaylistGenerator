#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import io
import logging
import os
import sys
from datetime import datetime

import eyed3

log_stream = io.StringIO()
logging.basicConfig(stream=log_stream, level=logging.INFO)

mp3files = []
albums_by_id = {}
mp3files_genres = {}
extension = ('.mp3')
spinner = ['-','\\','|','/']

print('Enter path to MP3 collection:')
path = input()

print('{} Start reading files'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
counter = 0
for root, dirs, files in os.walk(path, topdown = True):
    for file in files:
        print('{}'.format(spinner[counter % 4]), end='\r')
        if file.endswith(extension):
            mp3files.append(os.path.join(root, file))
        counter += 1
print('{} Reading files stopped ({} files)'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), counter))


print('{} Start reading ID3 data'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
genre_id = 1
album_id = 1
counter = 0
for mp3file in mp3files:
    print('{}'.format(spinner[counter % 4]), end='\r')
    audiofile = eyed3.load(mp3file)
    llog = log_stream.getvalue()
    if llog:
        log_stream.truncate(0)
    try:
        _genre = audiofile.tag.genre.name
        _album = audiofile.tag.album
        _track = audiofile.tag.track_num[0]
    except:
        continue
    _album_id = album_id
    if _track == None:
        _track = 1
    if not _album in list(albums_by_id.keys()):
        albums_by_id[_album] = album_id
        album_id = album_id + 1
    else:
        _album_id = albums_by_id[_album]
    if _genre in mp3files_genres.keys():
        mp3files_genres[_genre].append(
            {'album': _album_id, 'track': _track, 'filename': mp3file})
    else:
        mp3files_genres[_genre] = [{'album': _album_id, 'track': _track, 'filename': mp3file}]        
    counter += 1
print('{} Reading ID3 data stopped ({} mp3 files)'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), counter))

print('{} Start writing playlist files'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
counter = 0
for genre in list(mp3files_genres.keys()):
    output = sorted(mp3files_genres[genre], key = lambda i: (i['album'], i['track']))
    outputfilename = '{}.m3u8'.format(genre)
    with open(outputfilename, 'w', encoding="utf-8") as f:
        f.write('\ufeff')
        for file in output:
            f.write('{}\n'.format(file['filename']))
            print('{}'.format(spinner[counter % 4]), end='\r')
            counter += 1
print('{} Writing playlist files stopped ({} mp3 files)'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), counter))

sys.exit()
