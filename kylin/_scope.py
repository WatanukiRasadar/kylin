from enum import Enum

SCOPES = {
    'DEFAULT': 'default'
}

CACHE = None

class Scope:

    @classmethod
    def register(cls, name:str, value:str):
        global SCOPES
        SCOPES[name] = value

    @classmethod
    def build_class(cls):
        global SCOPES
        global CACHE
        if not CACHE:
            CACHE = Enum('Scope', SCOPES)
        return CACHE
