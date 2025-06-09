import factory
from factory.fuzzy import FuzzyChoice, FuzzyDecimal
from faker import Faker
from service.models import Product, Category

fake = Faker()

class ProductFactory(factory.Factory):
    """Factory for creating fake Products"""
    class Meta:
        model = Product

    name = FuzzyChoice(['Hat', 'Pants', 'Shirt', 'Apple', 'Banana', 'Pots',
                        'Towels', 'Ford', 'Chevy', 'Hammer', 'Wrench'])

    description = factory.LazyFunction(lambda: fake.text(max_nb_chars=100))

    price = FuzzyDecimal(0.5, 2000.0, precision=2)

    available = FuzzyChoice([True, False])

    category = FuzzyChoice([
        Category.UNKNOWN,
        Category.CLOTHS,
        Category.FOOD,
        Category.HOUSEWARES,
        Category.AUTOMOTIVE,
        Category.TOOLS
    ])
