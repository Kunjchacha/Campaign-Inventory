import requests
import json

# Fetch data from API
response = requests.get('http://localhost:5000/api/inventory')
data = response.json()

# Get unique products
products = set()
for item in data:
    if item.get('product'):
        products.add(item['product'])

print("Available products in the API:")
print("=" * 40)
for product in sorted(products):
    print(f"- {product}")

print(f"\nTotal unique products: {len(products)}")
