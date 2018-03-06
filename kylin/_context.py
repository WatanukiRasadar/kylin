class Context(dict):
    """
        class to register the services of application
        is a singleton to application
    """

    __instance__ = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance__ is None:
            cls.__instance__ = super().__new__(cls) if super().__new__ is object.__new__ else super().__new__(cls,
                                                                                                              *args,
                                                                                                              **kwargs)
        return cls.__instance__
