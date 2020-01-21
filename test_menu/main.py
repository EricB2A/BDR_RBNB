from consolemenu import *
from consolemenu.items import *


#FIRST LOGIN


#raw = input("Login > ")



menu = ConsoleMenu("Title", "Subtitle")
selection_menu_2 = SelectionMenu(["item1", "item2"])

submenu_test = SubmenuItem("Submenu test", selection_menu_2, menu)
selection_menu = SelectionMenu(["item1", "item2"])

submenu_item = SubmenuItem("Submenu item", selection_menu, menu)

menu.append_item(submenu_item)

# Finally, we call show to show the menu and allow the user to interact
menu.show()