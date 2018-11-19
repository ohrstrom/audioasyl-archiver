# -*- coding: utf-8 -*-

from mutagen.id3 import ID3, TIT2, TPE1, TALB, UFID, TPUB, TDRC, TRSN

ENCODING_ID = 3

def write_tags(path, title=None, artist=None, album=None, publisher=None, date=None, data=None):

    tags = ID3()

    tags.add(TRSN(
        encoding=ENCODING_ID,
        text='audioasyl.net')
    )

    if title:
        tags.add(TIT2(
            encoding=ENCODING_ID,
            text=title)
        )

    if artist:
        tags.add(TPE1(
            encoding=ENCODING_ID,
            text=artist)
        )

    if album:
        tags.add(TALB(
            encoding=ENCODING_ID,
            text=album)
        )

    if publisher:
        tags.add(TPUB(
            encoding=ENCODING_ID,
            text=album)
        )

    if date:
        tags.add(TDRC(
            encoding=ENCODING_ID,
            text=date)
        )

    if data:
        tags.add(UFID(
            encoding=ENCODING_ID,
            owner='audioasyl.net',
            data=data)
        )

    tags.save(path)

    return tags
