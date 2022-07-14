


class CustomError(Exception):
    """Base class for other exceptions"""
    pass

class SomethingBadHappened(CustomError):
    """Raised when something bad happens"""
    
    # def __init__(self, param1, message="this is a message"):
    #     self.param1 = param1
    #     self.message = message
    #     super().__init__(self.message)
        
    # def __str__(self):
    #     return f'{self.param1} -> {self.message}'        