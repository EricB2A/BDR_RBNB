from app.gui.page import Page
from app.gui.gui import Gui
from app.db.entity_manager import EntityManager
from app.entities.personne import Personne

from .past_rental import PastRental
from .confirmed_rental import ConfirmedRental
from .waiting_rental import WaitingRental 

RentalMenu = Page("MyRentals")
RentalMenu.append_item(PastRental)
RentalMenu.append_item(ConfirmedRental)
RentalMenu.append_item(WaitingRental)


