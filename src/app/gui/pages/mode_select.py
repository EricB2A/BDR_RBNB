from app.gui.page import Page
from app.gui.gui import Gui
#from .page_repository import main

mode_select_page = Page("User type select")

def set_user_mode(mode):
   g = Gui()
   g.user_type = m
   return True

mode_select_page.append_item(lambda : set_user_mode("proprietaire"), "Propriétaire")
mode_select_page.append_item(lambda : set_user_mode("locataire"), "Locataire")
#mode_select_page.set_next(main)