import pytest
from quart import Quart

from kylin import Service, Inject
from kylin.extras.provider import ProviderInject


@pytest.fixture
def app() -> Quart: return Quart(__name__)


@pytest.mark.asyncio
async def test_injection(app: Quart):
    @Service(name="service")
    class TestService: pass

    @Inject(service="service")
    async def get_service(service):
        return service

    async with app.app_context():
        assert isinstance(await get_service(), TestService)


@pytest.mark.asyncio
async def test_provider_injection(app: Quart):
    class Product:

        def __init__(self, id: int):
            self.id = id

    @Service(name='provider')
    class ProductProvider():

        async def provide(self, id: int): return Product(id=id)

    @ProviderInject('product', 'provider')
    async def get_product(product: Product):
        return product

    async with app.app_context():
        id = 1

        product = await get_product(product_id=id)

        assert isinstance(product, Product)
        assert product.id == id
