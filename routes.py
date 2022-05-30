from flask import Blueprint, render_template

bp = Blueprint('root', __name__, url_prefix='/', template_folder='templates')


@bp.route('/')
def root_view():
    return render_template('index.html')
