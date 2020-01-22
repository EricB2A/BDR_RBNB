from PyInquirer import style_from_dict, Token, prompt as prompt_, Separator

def Text(name, message = None, default = "", validate = None):
   return {
      'type': 'input',
      'name': name,
      'message': message if message is not None else name,
      'default' : default,
      'validate' : validate,
   }
def List(name, message = None, choices = [], default = "", filter_ = None):
   return {
      'type': 'list',
      'name': name,
      'message': message,
      'choices': choices,
      'filter': filter_
   }
def Checkbox(name, message = None, choices=[], validate_=None, filter_=None, default=[], qmark = "-"):
   return {
      'type': 'checkbox',
      'name': name,
      'qmark': qmark,
      'message' : message if message is not None else name, 
      'choices' : choices,
      'filter' : filter_, 
      'validate' : validate_, 
      'default' : default_
   }

def prompt(questions):
   return prompt_(questions)