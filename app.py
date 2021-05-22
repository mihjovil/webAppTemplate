from flask import Flask, render_template
from logic import internal_class
app = Flask(__name__)


@app.route('/')
def hello_world():
    internal = internal_class()
    return render_template('index.html', name=internal.name)


if __name__ == '__main__':
    app.run()
