from .page import Page
from .gui import Gui
#from .page_repository import main

mode_select_page = Page("User type select")
def set_user_mode(mode):
   def s_():
      g = Gui()
      g.user_type = mode
      return True

mode_select_page.append_item("Propriétaire", set_user_mode("proprietaire"))
mode_select_page.append_item("Locataire", set_user_mode("locataire"))
#mode_select_page.set_next(main)