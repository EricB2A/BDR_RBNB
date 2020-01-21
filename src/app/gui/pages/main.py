from app.gui.page import Page
from app.gui.gui import Gui
from .search import search
from .my_properties import manage_properties
main = Page("main", title="Dashboard")
main.append_item(search)
main.append_item(manage_properties)
# mainMenuPage = Page("Menu principale", should_exit=True)
# mainMenuPage.append_item(search)