from flask import Blueprint, render_template, redirect, request
from database import get_db

bp = Blueprint('root', __name__, url_prefix='/', template_folder='templates')


@bp.route('/')
@bp.route('/unprocessed')
def root_view():
    db = get_db()
    videos = db.unviewed_videos
    print([type(video) for video in videos])
    return render_template('index.html', videos=videos, index_status=["active", ""])


@bp.route('/process_video/<string:name>/')
def proces_video(name: str):
    val = request.args['setval']
    val = int(val)
    db = get_db()
    db.set_video_status(name, val)
    if val == 1:
        return redirect('/', 302)
    else:
        return redirect('/processed', 302)


@bp.route('/processed')
def processed_view():
    db = get_db()
    videos = db.viewed_videos
    print('processed')
    print(videos)
    return render_template('processed.html', videos=videos, index_status=["", "active"])
