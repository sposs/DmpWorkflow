# Set the path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask.ext.script import Manager, Server, Shell
from core import app, db
import models

def _make_context():
    return dict(app=app, db=db, models=models)

manager = Manager(app)
# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = '0.0.0.0')
)

manager.add_command("shell", Shell(make_context=_make_context))

if __name__ == "__main__":
    manager.run()