from django.test import TestCase
from web.models import Product, Order
from web.views import get_shop_stat
from django.conf import settings as djangoSettings
from django.urls import reverse
import os
import pandas as pd

class WebAPITest(TestCase):
    def setUp(self):
        test_products_params = [('test1', 10, 10, 'test_shop1', False),
                                ('test2', 10, 1009, 'test_shop2', True),
                                ('test3', 20, 1, 'test_shop3', False)]

        test_orders_params = [('test_order1', 'test1', 20, 10, 'test_shop1'),
                              ('test_order2', 'test2', 2, 1009, 'test_shop2')]
        
        for param in test_products_params:
            Product.objects.create(product_id=param[0],
                                   stock_pcs=param[1],
                                   price=param[2],
                                   shop_id=param[3],
                                   vip=param[4])
        
        for param in test_orders_params:
            Order.objects.create(order_id=param[0],
                                 product_id=param[1],
                                 qty=param[2],
                                 price=param[3],
                                 shop_id=param[4])

    def tearDown(self):
        Product.objects.all().delete()
        Order.objects.all().delete()

    def test_create_order(self):
        url = reverse('create_order')
        
        # positive testing
        res = self.client.post(url, {"selected_item": 'test1',
                                     "purchase_num": 1,
                                     "is_vip": 'false'})

        self.assertEqual(res.status_code, 200)
        
        res = self.client.post(url, {"selected_item": 'test2',
                                     "purchase_num": 1,
                                     "is_vip": 'true'})

        self.assertEqual(res.status_code, 200)
        

        res = self.client.post(url, {"selected_item": 'test3',
                                     "purchase_num": 1,
                                     "is_vip": 'false'})

        self.assertEqual(res.status_code, 200)

        # cur_stock_pcs = (test1, 9), (test2, 9), (test3, 19)
        # negative testing
        
        res = self.client.post(url, {"selected_item": 'test1',
                                     "purchase_num": 100,
                                     "is_vip": 'false'})

        self.assertEqual(res.status_code, 400)

        res = self.client.post(url, {"selected_item": 'test2',
                                     "purchase_num": 1,
                                     "is_vip": 'false'})

        self.assertEqual(res.status_code, 403)

        # buy until no stock_pcs
        _ = self.client.post(url, {"selected_item": 'test3',
                                   "purchase_num": 19,
                                   "is_vip": 'false'})

        res = self.client.post(url, {"selected_item": 'test3',
                                     "purchase_num": 1,
                                     "is_vip": 'false'})

        self.assertEqual(res.status_code, 400)

    def test_delete_order(self):
        test_url1 = reverse('delete_order', kwargs={'order_id': 'test_order1'})
        test_url2 = reverse('delete_order', kwargs={'order_id': 'test_order2'})
        test_url3 = reverse('delete_order', kwargs={'order_id': 'test_order3'})

        # positive testing
        res = self.client.delete(test_url1)
        self.assertEqual(res.status_code, 200)
        test1_product_info = Product.objects.filter(product_id='test1')
        self.assertEqual(test1_product_info[0].stock_pcs, 30)

        res = self.client.delete(test_url2)
        self.assertEqual(res.status_code, 200)
        test2_product_info = Product.objects.filter(product_id='test2')
        self.assertEqual(test2_product_info[0].stock_pcs, 12)

        # negative testing
        res = self.client.delete(test_url3)
        self.assertEqual(res.status_code, 404)

    def test_get_order_stat(self):
        url = reverse('get_order_stat')
        
        res = self.client.get(url)        
        self.assertEqual(res.status_code, 200)

        self.assertJSONEqual(
            str(res.content, encoding='utf8'),
            {'top1': 'product-test1, sold_qty: 20',
             'top2': 'product-test2, sold_qty: 2',
             'top3': 'No Top3',}
        )
        
        _ = self.client.post(reverse('create_order'),
                            {"selected_item": 'test3',
                             "purchase_num": 1,
                             "is_vip": 'false'})
        
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertJSONEqual(
            str(res.content, encoding='utf8'),
            {'top1': 'product-test1, sold_qty: 20',
             'top2': 'product-test2, sold_qty: 2',
             'top3': 'product-test3, sold_qty: 1',}
        )
        
    def test_get_shop_stat(self):
        get_shop_stat()
        csv_file_name = 'report_csv.csv'
        csv_path = os.path.join(djangoSettings.STATICFILES_DIRS[0],
                                csv_file_name)

        shop_stat = pd.read_csv(csv_path)
        self.assertEqual(shop_stat['test_shop1'].to_list(),
                         [200, 20, 1])
        self.assertEqual(shop_stat['test_shop2'].to_list(),
                         [2018, 2, 1])
        self.assertEqual(shop_stat['test_shop3'].to_list(),
                         [0, 0, 0])

        # insert two records of product test3
        _ = self.client.post(reverse('create_order'),
                            {"selected_item": 'test3',
                             "purchase_num": 1,
                             "is_vip": 'false'})
        _ = self.client.post(reverse('create_order'),
                            {"selected_item": 'test3',
                             "purchase_num": 1,
                             "is_vip": 'false'})
        
        get_shop_stat()
        
        shop_stat = pd.read_csv(csv_path)
        self.assertEqual(shop_stat['test_shop1'].to_list(),
                         [200, 20, 1])
        self.assertEqual(shop_stat['test_shop2'].to_list(),
                         [2018, 2, 1])
        self.assertEqual(shop_stat['test_shop3'].to_list(),
                         [2, 2, 2])


