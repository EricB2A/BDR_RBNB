from app.gui.page import Page
from app.gui.gui import Gui
from .search import search

main = Page("main")
main.append_item(search)

# mainMenuPage = Page("Menu principale", should_exit=True)
# mainMenuPage.append_item(search)