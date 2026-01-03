class DomainException(Exception):
    pass

class UserBannedException(DomainException):
    pass

class InvalidPlanException(DomainException):
    pass

class InvalidStatusTransition(DomainException):
    pass