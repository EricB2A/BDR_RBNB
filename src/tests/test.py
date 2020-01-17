

import sys, os
sys.path.append(os.path.join(os.getcwd(), "app"))
sys.path.append(os.path.join(os.getcwd()))
print(os.getcwd())
import app
from app.config import *
from app.db import *
from app.cli.cli_manager import *

app.boot()

from entities.user import User
from entities.location import Location

# u = User()
# u.name = "asd"
# u.password="asdasd"
# u.locations = [
#    Location(name="test location"),
#    Location(name="test location"),
#    Location(name="test location")
# ]
# u.save()

# print(u.id)
# print(u.render())


l = Location(name="test")
l.user = User(name="asd", password="asdasd")
l.save()