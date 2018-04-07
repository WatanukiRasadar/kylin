from typing import Generic, TypeVar, Union, Dict, List, AnyStr, Type, Any
from asyncio import wait
from .validator import Validator
from .._scope import Scope
from .._context import Context

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
    def scope(self): return Scope()

    @property
    def context(self): return Context()

    async def create(self, *args, **kwargs) -> Union[T, Dict[AnyStr, List[AnyStr]]]:
        kwargs = await self.clean(**kwargs)
        valid = await self.validate(*args, **kwargs)
        if valid is True:
            return self.klzz(*args, **kwargs)
        return valid

    async def validate_field(self, field_name: AnyStr, value: Any, validators: list, errors: dict):
        for validator in validators:
            try:
                await validator.validate(value)
            except ValueError as error:
                errors.setdefault(field_name, []).append(str(error))


    async def validate(self, *args, **kwargs) -> Union[bool, Dict[AnyStr, List[AnyStr]]]:
        validators = await self.validators()
        errors = {}
        tasks = []
        for argument_name, argument_value in kwargs.items():
            argument_validator = validators.get(argument_name) or []
            if isinstance(argument_validator, Validator):
                argument_validator = [argument_validator]
            if isinstance(argument_validator, list):
                tasks.append(self.validate_field(argument_name, argument_value, argument_validator, errors))
        await wait(tasks)
        return True if not errors else errors

    async def clean(self, *args, **kwargs) -> dict:
        return kwargs

    async def validators(self) -> Dict[AnyStr, Union[Validator, List[Validator]]]:
        scope = self.scope
        context = self.context
        validators = {}
        keys = set(scope.keys())
        keys.update(set(context.keys()))
        validators_names = [validator_name for validator_name in keys if
                            validator_name.startswith(self.validator_prefix)]
        for validator_name in validators_names:
            validator = self.scope[validator_name]
            name = validator_name.replace('%s.' % self.validator_prefix, '')
            validators.setdefault(name, []).append(validator)
        return validators
