from flask import Flask, g
from routes import bp

app = Flask(__name__)
app.register_blueprint(bp)

@app.teardown_appcontext
def teardown_db(excption):
    db = g.pop('db', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8888,
        debug=True,
    )
