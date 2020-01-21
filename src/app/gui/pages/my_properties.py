from app.gui.page import Page
from app.gui.gui import Gui
import termtables as tt
import logging
def my_properties_():
   Page.clear()

   g = Gui()
   current_user = g.user
   logging.debug(current_user)

my_properties = Page("my_properties", title="Gérer mes biens")
my_properties.set_main(my_properties)

pending_locations = Page("pending_locations", title="Locations en attente")

manage_properties = Page("manage_properties", title="Gérer mes propriétés")
manage_properties.append_item(my_properties)
manage_properties.append_item(pending_locations)

#En mode Locataire
#Afficher les locations passé
#Afficher les locations futurs
#Manager mes biens --> seulement proprio