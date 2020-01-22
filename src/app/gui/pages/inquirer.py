from PyInquirer import style_from_dict, Token, prompt as prompt_, Separator, Validator, ValidationError
import regex

class EmailValidator(Validator):
    def validate(self, document):
        ok = regex.match(r".+\@.+\..+", document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid email',
                cursor_position=len(document.text))  # Move cursor to end

def Text(name, message = None, default = "", validate = None):
   return {
      'type': 'input',
      'name': name,
      'message': message if message is not None else name,
      'default' : default,
      'validate' : validate,
   }
def Email(name, message = None, default = ""):
   return Text(name, message, default, EmailValidator )

def Password(name, message = None, default = "", validate = None):
   return {
      'type': 'password',
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
def Checkbox(name, message = None, choices=[], validate=None, filter_=None, default=[], qmark = "-"):
   choices_mapping = []
   for i in choices:
      choices_mapping.append({
            'name': i,
            'checked': i in default
      })
         
   return {
      'type': 'checkbox',
      'name': name,
      'qmark': qmark,
      'message' : message if message is not None else name, 
      'choices' : choices_mapping,
      'filter' : filter_, 
      'validate' : validate, 
   }
def Confirm(name, message = None, default = True):
   return {
      'type': 'confirm',
      'message': message if message is not None else name,
      'name': name,
      'default': default,
    }
def prompt(questions):
   return prompt_(questions)