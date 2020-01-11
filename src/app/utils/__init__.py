from os import listdir
from os.path import isfile, join

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
    
def get_files_in_path(path):
  return [join(path,f) for f in listdir(path) if isfile(join(path, f))]