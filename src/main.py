

import sys, os
sys.path.append(os.path.join(os.getcwd(), "app"))

import app
from app.config import *
from app.db import *
from app.cli.cli_manager import *

app.boot()
app.run()