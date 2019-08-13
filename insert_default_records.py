from web.models import Product

default_params = [('1', 6, 150, 'um', False),
                  ('2', 10, 110, 'ms', False),
                  ('3', 20, 900, 'ps', False),
                  ('4', 2, 1899, 'ps', True),
                  ('5', 8, 35, 'ms', False),
                  ('6', 5, 60, 'um', False),
                  ('7', 5, 800, 'ps', True)]

for params in default_params:
    product = Product(product_id=params[0],
                      stock_pcs=params[1],
                      price=params[2],
                      shop_id=params[3],
                      vip=params[4])
    product.save()

