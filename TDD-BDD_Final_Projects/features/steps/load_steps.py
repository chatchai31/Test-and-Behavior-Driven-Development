import requests
from behave import given

@given('the following pets')
def step_impl(context):
    """Refresh all Pets in the database"""

    # List all of the pets and delete them one by one
    response = requests.get(f"{context.base_url}/pets")
    assert response.status_code == 200
    for pet in response.json():
        response = requests.delete(f"{context.base_url}/pets/{pet['id']}")
        assert response.status_code == 204

    # load the database with new pets
    for row in context.table:
        payload = {
            "name": row['name'],
            "category": row['category'],
            "available": row['available'] in ['True', 'true', '1'],
            "gender": row['gender'],
            "birthday": row['birthday']
        }
        response = requests.post(f"{context.base_url}/pets", json=payload)
        assert response.status_code == 201