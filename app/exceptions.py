class InvalidSplitError(ValueError):
    pass


class InvalidBalancesError(ValueError):
    pass


class InvalidExpenseError(ValueError):
    pass


class EntityNotFoundError(LookupError):
    pass