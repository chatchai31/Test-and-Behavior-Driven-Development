import unittest
import json
from service import routes
from service.common import status
from service import  db

BASE_URL = "/products"

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = routes.app
        
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        

    def _create_products(self, count=1):
        products = []
        for i in range(count):
            product_data = {
                "name": f"Product {i}",
                "description": f"Description for product {i}",
                "category": "TOOLS",
                "price": 10.0 + i,
                "available": i % 2 == 0
            }
            response = self.client.post(BASE_URL,
                                        data=json.dumps(product_data),
                                        content_type="application/json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            products.append(response.get_json())
        return products

    def test_get_product(self):
        product = self._create_products(1)[0]
        response = self.client.get(f"{BASE_URL}/{product['id']}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], product["name"])

    def test_update_product(self):
        product = self._create_products(1)[0]
        update_data = {
            "name": "Updated Product",
            "description": "Test Updated2025",
            "category": "TOOLS",
            "price": 99.99,
            "available": True
        }
        response = self.client.put(f"{BASE_URL}/{product['id']}",
                                   data=json.dumps(update_data),
                                   content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], update_data["name"])
        self.assertAlmostEqual(float(data["price"]), update_data["price"],places=2)

    def test_delete_product(self):
        product = self._create_products(1)[0]
        response = self.client.delete(f"{BASE_URL}/{product['id']}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Verify deleted by trying to get it again
        response = self.client.get(f"{BASE_URL}/{product['id']}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_all_products(self):
        self._create_products(3)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertTrue(len(data) >= 3)  # At least 3 products returned

    def test_list_products_by_name(self):
        product = self._create_products(1)[0]
        name = product["name"]
        response = self.client.get(f"{BASE_URL}?name={name}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertTrue(any(p["name"] == name for p in data))

    def test_list_products_by_category(self):
        self._create_products(1)
        response = self.client.get(f"{BASE_URL}?category=TOOLS")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertTrue(all(p["category"] == "TOOLS" for p in data))

    def test_list_products_by_availability(self):
        # Create products with alternating availability
        self._create_products(4)
        response = self.client.get(f"{BASE_URL}?available=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertTrue(all(p["available"] is True for p in data))


