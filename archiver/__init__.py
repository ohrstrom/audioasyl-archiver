# -*- coding: utf-8 -*-

import logging
import sys

import click
import click_log

from .core import Archiver

__version__ = '0.0.1'

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


@click.group()
@click_log.simple_verbosity_option(logger)
def cli():
    pass


@cli.command()
def version():
    click.echo(__version__)
    sys.exit()


@cli.command()
@click.argument('scope', type=click.Choice(choices=['index', 'program', 'playlist']))
@click.option('--db-url', '-h', 'db_url', type=str, required=True, help='database url: mysql://user:pass@localhost/db')
@click.option('--src', '-s', 'src_dir', type=click.Path(exists=True, writable=True), required=False,
              help='input/source directory')
@click.option('--dst', '-d', 'dst_dir', type=click.Path(exists=True, writable=True), required=True,
              help='output directory')
def archive(scope, db_url, src_dir, dst_dir):
    logger.info('archive scope: {} - src: {} - dst: {}'.format(scope, src_dir, dst_dir))

    a = Archiver(dst_dir=dst_dir, src_dir=src_dir, db_url=db_url)

    if scope == 'index':
        result = a.archive_index()

    if scope == 'program':
        if not src_dir:
            raise Exception('for "program" scope the "--src/-s" option is required.')
        result = a.archive_programs()

    if scope == 'playlist':
        result = a.archive_playlists()
