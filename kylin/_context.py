class Context(dict):
    """
        class to register the services of application
        is a singleton to application
    """

    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = dict.__new__(cls, *args, **kwargs)
        return cls.__instance
