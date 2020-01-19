from .page import Page
from .mode_select import mode_select_page
def login_():
   username  = input("Username: ")
   password = input("Password: ")
   return True

def search_():
   query = ""
   criteria = [
      "username",
   ]
   for i in criteria:
      res = input(i)
      if res is not None:
         query += "{} = {} AND".format(i,res)
   res = User.where("username = 'asd' ")

   print("WHAT do you want to search")
   input(">")
   
   # res = inquirer.prompt([
   #    inquirer.List("action", message="What do you want to do", choice=[
   #       ('Reservez', fnt)
   #    ])
   # ])
   # res["action"]()

   
   return True

search = Page("search")
search.set_main(search_)

main = Page("main", should_exit=True)
main.append_item(search)
main.append_item("TEST", lambda : print("AISDASD"))


login = Page("Login")
login.set_main(login_)
login.set_next(mode_select_page)
