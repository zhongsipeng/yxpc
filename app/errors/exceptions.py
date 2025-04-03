class BusinessError(Exception):
    def __init__(self, message="Business Error", details=None):
        self.message = message
        self.details = details
def raiseBusinessMsg(msg):        
    raise BusinessError(message=msg)
