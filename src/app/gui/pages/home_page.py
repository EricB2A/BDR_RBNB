from app.gui.page import Page
from app.gui.gui import Gui

from .register import register_page
from .login import login
home = Page("home", title="Accueil")

home.append_item(register_page)
home.append_item(login)