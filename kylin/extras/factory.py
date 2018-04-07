from typing import Generic, TypeVar, Union, Dict, List, AnyStr, Type

from .validator import Validator
from .._scope import Scope

T = TypeVar('T')


class Factory(Generic[T]):
    """
    Generic factory
    and class to data instantiation
    Need a validator_prefix to identify a data validation
    """

    def __init__(self, klzz: Type[T], validator_prefix: str):
        self.klzz = klzz
        self.validator_prefix = validator_prefix

    @property
    def scope(self):
        return Scope()

    async def create(self, *args, **kwargs) -> Union[T, Dict[AnyStr, List[AnyStr]]]:
        valid = await self.validate(*args, *kwargs)
        if valid is True:
            return self.klzz(*args, **(await self.clean(**kwargs)))
        return valid

    async def validate(self, *args, **kwargs) -> Union[bool, Dict[AnyStr, List[AnyStr]]]:
        validators = await self.validators()
        errors = {}
        for argument_name, argument_value in kwargs.items():
            argument_validator = validators.get(argument_name) or []
            if isinstance(argument_validator, Validator):
                argument_validator = [argument_validator]
            if isinstance(argument_validator, list):
                for validator in argument_validator:
                    try:
                        await validator.validate(argument_value)
                    except ValueError as error:
                        errors.setdefault(argument_name, []).append(str(error))
        return True if not errors else errors

    async def clean(self, *args, **kwargs) -> dict:
        return kwargs

    async def validators(self) -> Dict[AnyStr, Union[Validator, List[Validator]]]:
        scope = self.scope
        validators = {}
        validators_names = [validator_name for validator_name in scope.keys() if
                            validator_name.startswith(self.validator_prefix)]
        for validator_name in validators_names:
            validator = self.scope[validator_name]
            name = validator_name.replace(self.validator_prefix, '')
            validators.setdefault(name, []).append(validator)
        return validators
