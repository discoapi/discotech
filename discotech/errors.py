__package__ = 'discotech'

class discotechError(Exception):
    def __init__(self, error):
        super(self.__class__,self).__init__(error)
        self.error = error
