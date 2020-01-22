from app.gui.page import Page
from app.gui.gui import Gui
from .search import search
from .my_properties import manage_properties
from .profil import profil_page
main = Page("main", title="Dashboard")
main.append_item(search)
main.append_item(manage_properties)
main.append_item(profil_page)
# mainMenuPage = Page("Menu principale", should_exit=True)
# mainMenuPage.append_item(search)