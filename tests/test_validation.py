import pytest
from quart import Quart
from kylin import Service, Inject
from kylin.extras.validator import Validator
from kylin.extras.factory import Factory



@pytest.fixture
def app() -> Quart: return Quart(__name__)


@pytest.mark.asyncio
async def test_factory_validation(app: Quart):

    class Product:

        def __init__(self, name: str, price: int = 0):
            self.name = name
            self.price = price

    @Service(name='factories.product')
    class ProductFactory(Factory[Product]):

        def __init__(self):
            super().__init__(Product, 'validators.product')

    @Service(name='validators.product.name')
    class ProductNameValidator(Validator):

        async def validate(self, value):
            if not isinstance(value, str):
                raise ValueError('Invalid name')

    @Service(name='validators.product.price')
    class ProductPriceValidator(Validator):
        async def validate(self, value):
            if not isinstance(value, int):
                raise ValueError('Invalid price')


    @Inject(factory='factories.product')
    async def create_product(factory: Factory[Product], **kwargs):
        return await factory.create(**kwargs)

    async with app.app_context():
        name = 'test'
        product = await create_product(name=name)
        assert isinstance(product, Product)
        assert product.name == name

        product = await create_product(name=1, price=1.2)

        assert isinstance(product, dict)
        assert 'name' in product.keys()
        assert 'Invalid name' in product['name']

        assert 'price' in product.keys()
        assert 'Invalid price' in product['price']

