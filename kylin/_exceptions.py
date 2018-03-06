class ServiceNotFoundException(Exception):
    def __init__(self, service: str) -> None:
        super().__init__('The service: %s are not found, please check if has ben registered' % service)
