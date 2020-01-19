from .page import Page
from .register import register_page
from .page_repository import login
home = Page("home", title="Accueil")

home.append_item(register_page)
home.append_item(login)