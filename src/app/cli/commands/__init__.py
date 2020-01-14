from .create import Create
from .create_db import CreateDb
from .find import Find

available_commands = {
   "create" : Create,
   "create_db": CreateDb,
   "find": Find
}