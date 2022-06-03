import sqlite3
from typing import Union
from pathlib import Path
from os import listdir
from flask import g


class VideosDatabase(object):

    def __init__(self, path: Union[None, str, Path] = None, videos_path=Path.cwd() / 'videos'):
        if not path:
            db_file = Path.cwd() / 'database.db'
        else:
            db_file = path

        self._db = sqlite3.connect(db_file)
        self._video_path = videos_path

        # create table videos if not exist
        # columns id, name, viewed
        self._db.execute('''CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            viewed INTEGER);''')
        self._db.commit()
        self._diff_db()

    def _diff_db(self):
        """
        Sync `self._video_path` with `self._db`
        if new file is added, add it to db
        if a file is removed, remove it from db 
        """
        files = listdir(self._video_path)
        cur = self._db.cursor()
        all_entries = cur.execute("SELECT name FROM videos").fetchall()
        all_entries = [entry[0] for entry in all_entries]
        to_add = []
        to_remove = []
        for file in files:
            if file not in all_entries:
                to_add.append(file)

        for entry in all_entries:
            if entry not in files:
                to_remove.append(entry)

        for f in to_add:
            cur.execute('INSERT INTO videos (name, viewed) VALUES (?, 0)', (f,))

        for f in to_remove:
            cur.execute('DELETE FROM videos WHERE name = ?', (f,))
        cur.close()
        self._db.commit()

    def __del__(self):
        self._db.close()

    def close(self):
        self._db.close()

    @property
    def viewed_videos(self) -> list:
        cur = self._db.cursor()
        res = cur.execute('SELECT name FROM videos WHERE viewed = 1').fetchall()
        cur.close()
        return [item[0] for item in res]

    @property
    def unviewed_videos(self) -> list:
        cur = self._db.cursor()
        res = cur.execute('SELECT name FROM videos WHERE viewed = 0').fetchall()
        cur.close()
        return [item[0] for item in res]

    def set_video_status(self, name: str, status: int):
        cur = self._db.cursor()
        cur.execute('UPDATE videos SET viewed = ? WHERE name = ?', (status, name))
        cur.close()
        self._db.commit()


def get_db():
    if 'db' not in g:
        g.db = VideosDatabase(videos_path='./static/videos')
    return g.db
