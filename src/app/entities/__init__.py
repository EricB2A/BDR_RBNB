from .personne import Personne
from .location import Location
from .addrese import Addresse
from .bien_immobilier import BienImmobilier
from .commune import Commune
from .fourniture import Fourniture
from .message import Message
from .pays import Pays
from .type_fourniture import TypeFourniture
from .type_bien import TypeBien

entity_registrar = {
   "personne" : Personne,
   "location" : Location,
   "addresse" : Addresse,
   "bien_immobilier": BienImmobilier,
   "commune": Commune,
   "fourniture": Fourniture,
   "message": Message,
   "pays": Pays,
   "type_fourniture": TypeFourniture,
   "type_bien": TypeBien
}