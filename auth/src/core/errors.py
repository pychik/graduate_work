class InvalidResponseError(Exception):
    """
    Generic exception for an invalid JSON response.
    Provide a custom message when raising, if necessary.
    """
    def __init__(self, msg='Invalid response'):
        super().__init__(msg)


class APIRouterError(Exception):
    def __init__(self, msg='Select API service'):
        super().__init__(msg)
