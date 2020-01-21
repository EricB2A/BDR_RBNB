import sys, os
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, "app"))

import app
from app.config import *
from app.db import *
from app.cli.cli_manager import Cli
from app.gui.gui import Gui
from app.gui.pages.home_page import home
config, db = app.boot()

g = Gui()
g.boot(home)
g.run()