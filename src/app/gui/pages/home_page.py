from app.gui.page import Page
from app.gui.gui import Gui

from .register import register_page
from .login import login
from .mode_select import mode_select_page
home = Page("home", title="Accueil")

home.append_item(register_page)
home.append_item(login)

#mode_select_page.set_next(main)