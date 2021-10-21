from flask import Flask, render_template
from logic import internal_class


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        # This was done to show how to send python objects to the jinja templates.
        internal = internal_class.ExampleClass()
        return render_template('index.html', name=internal.name)

    if __name__ == '__main__':
        app.run()
    return app

# region help for deployment
"""
requirements.txt is needed and pip freeze will create that file with all the packages in the environment
that might be an overkill, given that the project could use less packages than that.
Use the following command on your terminal
- pip install pipreqs

use the following command to create requiremetns.txt file
- pipreqs path/to/project

that should create the file in the selected path with only the required packages

"""
# endregion
