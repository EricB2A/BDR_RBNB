import sys, os
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(dir_path, "app"))

import app
from app.config import *
from app.db import *
from app.cli.cli_manager import Cli

config, db = app.boot()
cli = Cli(config, db)
cli.run()