# Documentation - Audioasyl Archive

## Archive File- & Directory Structure

**Note about the naming:**  
"Broadcast" stands for the *container*, and synonymously could be named "Show" or "Format". Example: "Andaground"  
A "Broadcast" can have many "programs", where a "program" describes the specific "event" / "emission". 

```shell
$ <archive root>
├── broadcasts
│   ├── <broadcast id>
│   │   ├── broadcast.json
│   │   ├── broadcast.txt
│   │   └── programs
│   │       ├── <program id>
│   │       │   ├── default.mp3
│   │       │   └── program.json
│   │       ├── <program id>
│   │       │   ├── default.mp3
│   │       │   └── program.json
│   │       ├── ...
│   ├── <broadcast id>
│   │   ├── broadcast.json
│   │   ├── broadcast.txt
│   │   └── programs
│   │       ├── <program id>
│   │       │   ├── default.mp3
│   │       │   └── program.json
│   │       ├── <program id>
│   │       │   ├── default.mp3
│   │       │   └── program.json
│   │       ├── ...
│   ├── ...
├── playlists
│   ├── <playlist name>.m3u
│   ├── <playlist name>.m3u
│   ├── ...
├── broadcasts.txt
├── broadcasts.json
├── full-dump.json
└── programs.json
```


### About The Dump-Files

All `json`-files are encoded in `UTF-8`.  
All references to directories and files are **relative to the archive's root**.

#### `broadcasts.json`

Contains the index about all archived broadcasts, like:

```json
[
    {
        "id": 87,
        "title": "1337 mus33k",
        "dir": "broadcasts/87"
    },
    ...
]
```

#### `programs.json`

Contains the index about all archived programs, like:

```json
[
    {
        "id": 23,
        "title": "tek-lounge - 2003-04-03",
        "dir": "broadcasts/7/programs/23"
    },
    ...
]
```

#### `full-dump.json`

Contains the complete dump of the archive's metadata.  
This is the file that should be used when working with the whole archive, e.g. when importing all data into a new
system.


### About The Audio-Files

All audio files are in `MP3` format. They contain a minimal set of ID3v2.4 metadata (so there is at least some
information displayed when using an audio-player).

In addition there is a `base64` encoded `json` dataset in each file, stored in the `UFID:audioasyl.net` frame. 




