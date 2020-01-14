from os import listdir
from os.path import isfile, join
import functools
"""
Singleton meta class
"""
class Singleton(type):
    def __init__(cls,name,bases,dict):
        super(Singleton,cls)\
          .__init__(name,bases,dict)
        original_new = cls.__new__
        def my_new(cls,*args,**kwds):
            if cls.instance == None:
                cls.instance = \
                  original_new(cls,*args,**kwds)
            return cls.instance
        cls.instance = None
        cls.__new__ = staticmethod(my_new)

"""
Singelton decorator
"""
def singleton(class_):
  class class_w(class_):
    _instance = None
    def __new__(class_, *args, **kwargs):
      if class_w._instance is None:
          class_w._instance = super(class_w,
                                    class_).__new__(class_,
                                                    *args,
                                                    **kwargs)
          class_w._instance._sealed = False
      return class_w._instance
    def __init__(self, *args, **kwargs):
      if self._sealed:
        return
      super(class_w, self).__init__(*args, **kwargs)
      self._sealed = True
  class_w.__name__ = class_.__name__
  return class_w

def get_files_in_path(path):
  return [join(path,f) for f in listdir(path) if isfile(join(path, f))]

def sanitize(data):
  return str(data)

def compose(*funcs):
  return functools.reduce(lambda f,g: lambda x: f(g(x)),funcs, lambda x: x)