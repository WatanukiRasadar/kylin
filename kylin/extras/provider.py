"""
    This module use a provider pattern to inject a data into a decorated function, to this
    are necessary to implement a Provider class protocol and decorate a function to value injections.

>>  @Service(name='providers.product')
>>  class ProductProvider(Provider[Product]):
>>
>>      async def provide(self, id: int) -> Product: return await Product.objects.filter(id=id).first()
>>
>>
>>  @ProviderInject('product', 'providers.product')
>>  async def clear_product_stock(product: Product):
>>      product.stock = 0
>>      await product.save()
>>
>>  loop.run_until_complete(clear_product_stock(product_id = 1))
"""

from typing import Generic, TypeVar

from .._injector import Inject, Injector

T = TypeVar('T')


class Provider(Generic[T]):
    """
        Generic provider
    """

    async def provide(self, *args, **kwargs) -> T:
        raise NotImplementedError('please implement this method')


class ProviderInjector(Injector):
    """
        Get the argument provider and call provider method with function called argument if a arguments names starts with
        a argument to be provided
    """

    async def __call__(self, *args, **kwargs):
        argument_name = self.dependencies['argument']
        print(self.dependencies)
        kwargs.update({
            argument_name: kwargs.get(argument_name) or await self.scope[self.dependencies.get('provider')] \
                .provide(**
                         {kwarg_name.replace('%s_' % argument_name, ''): kwarg_value for kwarg_name, kwarg_value in
                          kwargs.items() if
                 kwarg_name.startswith(argument_name)})
        })
        kwargs = {kwarg_name: kwarg_value for kwarg_name, kwarg_value in kwargs.items() if
                  not kwarg_name.startswith(argument_name) or kwarg_name == argument_name}
        return await self.fun(*args, **kwargs)


class ProviderInject(Inject):
    """
        class decorator to build a referent provider injector
    """


    __injector__ = ProviderInjector

    def __init__(self, argument: str, provider_name: str):
        super().__init__(provider=provider_name, argument=argument)