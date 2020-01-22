import PyInquirer
import sys
import os
import logging
from pprint import pprint


class Page(object):
   parent = None
   name = ""
   title = None
   items = {}
   main_callable = None
   next = None

   def __init__(self, name, parent = None, next = None, should_exit = False, title = None):
      self.name = name
      self.parent = parent
      self.should_exit = should_exit
      self.items = {}

      self.next = next
      self.main_callable = None
      self.title = title

   def set_main(self, fnt):
      """
      A main callable function must always return a boolean
      This boolean is evaluated and defines if we can show 
      the next or previous page
      """
      self.main_callable = fnt
      
   def get_title(self):
      if self.title is not None:
         return self.title
      return self.name

   def show(self):
      logging.debug("Page %s [next=%s, parent=%s]", self.name,self.next, self.parent)
      self.clear()
      if self.main_callable is not None:
         res = self.main_callable()
         if res:
            self.clear()
            if self.next is not None:
               return self.next.show()
            elif self.parent is not None:
               return self.parent.show()
            else:
               self.quit()
         else:
            self.quit()

      questions = list(self.items.keys())
      logging.debug("ITEMS %s", self.items)
      questions.append("Exit") # self.quit 

      inqQuestion = [ {
        'type': 'list',
        'name': 'choicePage',
        'message': self.get_title(),
        'choices': questions,
      }]
      questionResponse=PyInquirer.prompt(inqQuestion)

      if questionResponse is None:
         self.quit()
         return
         
      if questionResponse['choicePage'] == "Exit":
         self.quit()
         return
      
      choice = self.items[questionResponse['choicePage']]

      if isinstance(choice, Page):
         self.clear()
         choice.show()

      elif callable(choice):
         res = choice()
         if res is not None and res is True:
            if self.next is not None:
               self.next.show()
         else:
            self.show() #re show this screen

   def set_next(self, next):
      self.next = next
      return self

   def set_parent(self, cls):
      self.parent = cls
      return self

   def append_item(self, item, name = None):
      if isinstance(item, Page):
         item.set_parent(self)
         self.items[item.get_title()] = item
      else:
         self.items[ name ] =  item
      
      return self
   def quit(self):
      if self.should_exit:
         self._exit()
      else:
         if self.parent is not None:
            self.clear()
            self.parent.show()
         else:
            self._exit()

   def _exit(self):
      sys.exit(0)
      
   @staticmethod
   def clear():
      os.system('cls' if os.name == 'nt' else 'clear')
   @staticmethod
   def wait_input():
      input("Appuyez sur entrée pour continuer...")
if __name__ == "__main__":

   from pages.home_page import home
   home.show()