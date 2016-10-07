class NotConnectedException(Exception):
    """ Exception raised if the user has not authenticated and is trying to access an authenticated-only action. """
    pass
