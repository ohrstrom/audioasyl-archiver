# -*- coding: utf-8 -*-

import os

from orator import Model
from orator.orm import belongs_to_many, accessor

from .utils import fix_text

config = {
    'mysql': {
        'driver': 'mysql',
        'host': 'localhost',
        #'database': 'audioasyl',
        'database': 'audioasyl_dev',
        'user': 'root',
        'password': 'root',
        'prefix': ''
    }
}

#db = DatabaseManager(config)
#Model.set_connection_resolver(db)


class Artist(Model):

    __table__ = 'artist'
    __primary_key__ = 'artist_id'

    __appends__ = [
        'id',
        'name',
    ]

    __visible__ = [
        'id',
        'name',
    ]

    @accessor
    def id(self):
        return self.get_raw_attribute('artist_id')

    @accessor
    def name(self):
        return fix_text(self.get_raw_attribute('artist_name'))


#######################################################################
# `Program` is the actual event/emission.
#######################################################################
class Program(Model):

    __table__ = 'program'
    __primary_key__ = 'program_id'

    __dates__ = [
        'program_start',
        'program_end',
    ]

    __appends__ = [
        'id',
        'title',
        'description',
        'active',
        'archived',
        'artists',
        'guests',
        'genre',
        'sub_genre',
        'broadcast_id',
    ]

    __visible__ = [
        'id',
        'title',
        'description',
        'active',
        'archived',
        'artists',
        'guests',
        'genre',
        'sub_genre',
    ]

    @belongs_to_many('cat_program_broadcast', 'program_id', 'broadcast_id')
    def broadcasts(self):
        return Broadcast

    @accessor
    def broadcast(self):
        return self.broadcasts.first()

    @accessor
    def broadcast_id(self):
        return self.broadcast.id

    @accessor
    def title(self):
        _title = self.broadcast.title
        if self.time_start:
            _title = '{} - {}'.format(
                _title,
                self.time_start.strftime('%Y-%m-%d')
            )
        return _title

    @accessor
    def artists(self):
        artists = []
        for a in self.broadcast.artists.all():
            artists += [{'id': a.id, 'name': '{}'.format(a.name)}]
        # prepend 'program' artist if not already present
        # if self.program_artist and not list(filter(lambda n: n.get('name') == self.program_artist.strip(), artists)):
        #     artists = [{'id': None, 'name': '{}'.format(self.program_artist.strip())}] + artists
        return artists

    @accessor
    def id(self):
        return self.get_raw_attribute('program_id')

    @accessor
    def active(self):
        return self.get_raw_attribute('program_state') == 'A'

    @accessor
    def archived(self):
        return self.get_raw_attribute('program_archive_state') == 'A'

    @accessor
    def time_start(self):
        return self.get_raw_attribute('program_start')

    @accessor
    def guests(self):
        return fix_text(self.get_raw_attribute('program_by'))

    @accessor
    def style(self):
        return fix_text(self.get_raw_attribute('program_style'))

    @accessor
    def description(self):
        try:
            text = fix_text(self.get_raw_attribute('program_text'))
            return '\n'.join(text.splitlines())
        except AttributeError:
            return

    @accessor
    def genre(self):
        return self.broadcast.genre

    @accessor
    def sub_genre(self):
        return fix_text(self.style) if self.style else None

    @accessor
    def dir(self):
        return os.path.join(self.broadcast.dir, 'programs', str(self.id))

    @accessor
    def path(self):
        return os.path.join(self.dir, 'default.mp3')


#######################################################################
# `Broadcast` is the main 'container', a.k.a. "Show". for example "Andaground".
# a Broadcast can have multiple `Program`s
#######################################################################
class Broadcast(Model):

    __table__ = 'broadcast'
    __primary_key__ = 'broadcast_id'

    __appends__ = [
        'id',
        'title',
        'active',
        'artists',
        'description',
        'genre',
        'host',
        'website',
        'dir',
    ]

    __visible__ = [
        'id',
        'title',
        'active',
        'artists',
        'description',
        'genre',
        'host',
        'website',
        'dir',
    ]

    @belongs_to_many('cat_artist_broadcast', 'broadcast_id', 'artist_id')
    def artists(self):
        return Artist

    @belongs_to_many('cat_program_broadcast', 'broadcast_id', 'program_id')
    def programs(self):
        return Program

    @accessor
    def id(self):
        return self.get_raw_attribute('broadcast_id')

    @accessor
    def active(self):
        return self.get_raw_attribute('broadcast_state') == 'A'

    @accessor
    def title(self):
        return fix_text(self.get_raw_attribute('broadcast_name'))

    @accessor
    def host(self):
        return fix_text(self.get_raw_attribute('broadcast_by'))

    @accessor
    def website(self):
        try:
            url = fix_text(self.get_raw_attribute('broadcast_url'))
            return url if url else None
        except AttributeError:
            return

    @accessor
    def style(self):
        return fix_text(self.get_raw_attribute('broadcast_default_style'))

    @accessor
    def description(self):
        try:
            text = fix_text(self.get_raw_attribute('broadcast_text'))
            return '\n'.join(text.splitlines())

        except AttributeError:
            return

    @accessor
    def genre(self):
        return fix_text(self.style) if self.style else None

    @accessor
    def dir(self):
        return os.path.join('broadcasts', str(self.id))
