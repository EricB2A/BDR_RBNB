from .create import Create
from .create_db import CreateDb
from .find import Find
from .update import Update
from .reset_db import ResetDb
available_commands = {
   "create" : Create,
   "create_db": CreateDb,
   "find": Find,
   "reset_db": ResetDb,
   "update": Update
}