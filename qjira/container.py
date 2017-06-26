
class Container(dict):

    def __new__(cls):

        if not hasattr(cls, 'instance'):
            cls.instance = super(Container, cls).__new__(cls)

        return cls.instance
    
