import app.gui.pages.inquirer as inquirer

from app.entities.commune import Commune

def get_address():
   communes = Commune.find()
   commune_mapping = { x.nom + "(" + x.pays_nom + ")":x.nom for x in communes }
   fields = [
      inquirer.RequiredText("rue", message="Rue"),
      inquirer.RequiredText("numero", message="Numéro"),
      inquirer.RequiredText("complement_rue", message="Complément"),
      inquirer.Numeric("npa", message="Npa"),
      #inquirer.Text("ville", message="Ville"),
      inquirer.List("commune_nom", message="Commune", choices=list(commune_mapping.keys()))
   ]
   answers = inquirer.prompt(fields)
   if answers is None and not len(answers.keys()):
      return None
   answers["commune_nom"] = commune_mapping[answers["commune_nom"]]
   return answers
