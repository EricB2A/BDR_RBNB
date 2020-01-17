from .create import Create
from .create_db import CreateDb
from .find import Find
from .reset_db import ResetDb
available_commands = {
   "create" : Create,
   "create_db": CreateDb,
   "find": Find,
   "reset_db": ResetDb
}