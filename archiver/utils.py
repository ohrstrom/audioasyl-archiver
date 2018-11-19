# -*- coding: utf-8 -*-

import base64
import json
import urllib.parse

from html import unescape


urllib.parse.uses_netloc.append('mysql')

def parse_db_url(url):
    _url = urllib.parse.urlparse(url)
    config = {
        'driver': _url.scheme or 'mysql',
        'host': _url.hostname or 'localhost',
        'database': _url.path[1:],
        'port': _url.port or 3306,
        'user': _url.username or None,
        'password': _url.password or None,
    }
    return config

def fix_text(text):
    if not text:
        return
    _text = text.strip()
    try:
        _text = unescape(_text)
    except (TypeError):
        pass
    return _text


def encode_data(data):
    _json = json.dumps(data)
    _data = base64.b64encode(_json.encode('utf-8'))
    return _data


def decode_data(data):
    _data = base64.b64decode(data).decode('utf-8')
    _json = json.loads(_data)
    return _json
