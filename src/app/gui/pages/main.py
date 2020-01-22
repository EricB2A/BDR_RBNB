from app.gui.page import Page
from app.gui.gui import Gui
from .search import search
from .my_rentals import RentalMenu

from .my_properties import manage_properties
from .profil import profil_page
main = Page("main", title="Dashboard")

def change_menu():
   g = Gui()
   user_type = g.user_type

   if user_type == "proprietaire":
      main.append_item(search)
      main.append_item(RentalMenu)
      main.append_item(manage_properties)
      main.append_item(profil_page)
   else:
      main.append_item(search)
      main.append_item(RentalMenu)
      main.append_item(profil_page)

main.set_before_show(change_menu)

# mainMenuPage = Page("Menu principale", should_exit=True)
# mainMenuPage.append_item(search)