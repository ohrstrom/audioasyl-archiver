# -*- coding: utf-8 -*-

import codecs
import json
import logging
import os
import shutil

import click

from orator.exceptions.query import QueryException

from .db import Broadcast, Program
from .tags import write_tags
from .utils import encode_data, parse_db_url

JSON_DUMP_OPTIONS = {
    'indent': 4
}

logger = logging.getLogger(__name__)


class Archiver(object):
    _archived_broadcasts = []
    _archived_programs = []

    def __init__(self, dst_dir=None, src_dir=None, db_url=None):

        self.dst_dir = dst_dir
        self.src_dir = src_dir

        self.abs_dst_dir = os.path.abspath(dst_dir) if dst_dir else None
        self.abs_src_dir = os.path.abspath(src_dir) if src_dir else None

        if db_url:
            # not the most elegant way... pass db settings for orator
            from orator import DatabaseManager, Model
            self.db = DatabaseManager({
                'default': parse_db_url(db_url)
            })
            Model.set_connection_resolver(self.db)


    def prepare_db(self):

        from orator import Schema
        schema = Schema(self.db)

        if not schema.has_column('program', 'file_missing'):
            logger.info('adding "file_missing" column to program table')
            with schema.table('program') as table:
                table.boolean('file_missing').default(False)
        else:
            logger.debug('"file_missing" column present in program table')

        qs = Program.with_('broadcasts', 'broadcasts.artists')\
            .has('broadcasts') \
            .where('file_missing', '=', False)

        num_missing = 0
        num_total = qs.count()

        logger.info('total {} programs in db'.format(num_total))

        for program in qs.get():

            path = os.path.join(self.abs_src_dir, str(program.id), 'default.mp3')

            if not os.path.isfile(path):
                logger.warning('file missing: {}'.format(path))
                program.file_missing = True
                program.save()
                num_missing += 1

        logger.info('total {} programs (out of {}) without audio file'.format(num_missing, num_total))





    def archive_programs(self):

        qs = Program.with_('broadcasts', 'broadcasts.artists') \
            .left_join('cat_program_broadcast', 'program.program_id', '=', 'cat_program_broadcast.program_id') \
            .has('broadcasts') \
            .where('file_missing', '=', False) \
            .order_by('cat_program_broadcast.broadcast_id')

        logger.info('archiving {} programs'.format(qs.count()))

        os.makedirs(os.path.join(self.abs_dst_dir), exist_ok=True)

        # generate index file
        programs_index = [{
            'id': p.id, 'title': p.title, 'dir': p.dir
        } for p in qs.get()]

        # as json
        with codecs.open(os.path.join(self.abs_dst_dir, 'programs.json'), 'w', 'utf-8') as f:
            json.dump(programs_index, f, **JSON_DUMP_OPTIONS)

        for program in qs.get():

            if program.broadcast and not program.broadcast.id in self._archived_broadcasts:
                self.archive_broadcast(program.broadcast)

            self.archive_program(program)

    def archive_broadcast(self, broadcast):

        dir = os.path.join(self.abs_dst_dir, broadcast.dir)
        os.makedirs(dir, exist_ok=True)

        # write broadcast data as json
        with codecs.open(os.path.join(dir, 'broadcast.json'), 'w', 'utf-8') as f:
            json.dump(broadcast.serialize(), f, **JSON_DUMP_OPTIONS)

        # human readable txt
        with codecs.open(os.path.join(dir, 'broadcast.txt'), 'w', 'utf-8') as f:
            f.write('{}\n\n'.format(broadcast.title))
            f.write('{}\n\n'.format(', '.join([a.name for a in broadcast.artists]).rstrip(', ')))
            f.write('--\n{}'.format(broadcast.description))

        self._archived_broadcasts.append(broadcast.id)
        logger.info('archived broadcast: "{}" - id: {} - dir: {}'.format(broadcast.title, broadcast.id, dir))

    def archive_program(self, program):

        dir = os.path.join(self.abs_dst_dir, program.dir)
        os.makedirs(dir, exist_ok=True)

        # write program data as json
        with codecs.open(os.path.join(dir, 'program.json'), 'w', 'utf-8') as f:
            json.dump(program.serialize(), f, **JSON_DUMP_OPTIONS)

        # copy audio file
        # TODO: just testing - using dummy input file
        #src_path = '/Users/ohrstrom/Documents/Code/audioasyl-archiver/data/in/dummy_1s.mp3'
        src_path = os.path.join(self.abs_src_dir, str(program.id), 'default.mp3')
        dst_path = os.path.join(dir, 'default.mp3')

        if not os.path.isfile(src_path):
            click.secho('file missing! {}'.format(src_path), fg='red')
            return

        # copy file
        shutil.copy(src_path, dst_path)

        _data = program.serialize()
        _data.update({
            'broadcast': program.broadcast.serialize()
        })

        # add tags
        write_tags(
            dst_path,
            title=program.title,
            artist=', '.join(a['name'] for a in program.artists),
            album=program.broadcast.title,
            date=str(program.time_start.year) if program.time_start else None,
            data=encode_data(_data)
        )

        logger.debug('copy: {} to {}'.format(src_path, dst_path))

        self._archived_programs.append(program.id)
        logger.info('archived program: "{}" - id: {} - dir: {}'.format(program.title, program.id, dir))

    def archive_index(self):

        qs = Broadcast.with_('artists', 'programs') \
            .order_by('broadcast_name')

        logger.info('archiving index to: {}'.format(self.abs_dst_dir))

        os.makedirs(os.path.join(self.abs_dst_dir), exist_ok=True)

        # generate broadcasts index files
        broadcasts_index = [{
            'id': b.id, 'title': b.title, 'dir': b.dir
        } for b in qs.get()]

        # as json
        with codecs.open(os.path.join(self.abs_dst_dir, 'broadcasts.json'), 'w', 'utf-8') as f:
            json.dump(broadcasts_index, f, **JSON_DUMP_OPTIONS)

        # as human readable txt
        with codecs.open(os.path.join(self.abs_dst_dir, 'broadcasts.txt'), 'w', 'utf-8') as f:
            for b in broadcasts_index:
                f.write('{id:>4}\t{title}\n'.format(**b))

        # create complete dump as json
        # admitted, this is far from elegant :)
        _dump = []
        for b in qs.get():
            _b = b.serialize()
            _b['programs'] = []

            for p in b.programs.where('file_missing', False):
                _p = p.serialize()
                _p.update({
                    'dir': p.dir,
                    'path': os.path.join(p.dir, 'default.mp3'),
                })

                _b['programs'].append(_p)

            _dump.append(_b)

        # as json
        with codecs.open(os.path.join(self.abs_dst_dir, 'full-dump.json'), 'w', 'utf-8') as f:
            json.dump(_dump, f, **JSON_DUMP_OPTIONS)

    def archive_playlists(self):

        qs = Broadcast.with_('artists', 'programs') \
            .order_by('broadcast_name')

        logger.info('archiving playlists to: {}'.format(self.abs_dst_dir))

        dir = os.path.join(self.abs_dst_dir, 'playlists')

        os.makedirs(dir, exist_ok=True)

        for b in qs.get():
            path = os.path.join(dir, '{}.m3u'.format(b.title))
            with codecs.open(path, 'w', 'utf-8') as f:
                f.write('#EXTM3U\n\n')
                for p in b.programs.where('file_missing', False):
                    f.write('#EXTINF:,{}\n'.format(p.title))
                    f.write('{}\n\n'.format(os.path.join('..', p.path)))
