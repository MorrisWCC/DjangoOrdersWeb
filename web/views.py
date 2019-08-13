from django.shortcuts import render
from django.db import transaction
from django.db.models import Sum
from django.conf import settings as djangoSettings
from django.http import JsonResponse, HttpResponseBadRequest
from web.models import Product, Order
from web.help_functions import is_in_stock, is_vip, is_order_exist

import os
import json
import uuid
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.jobstores import register_events
from django_apscheduler.jobstores import register_job

@is_in_stock
@is_vip
@transaction.atomic
def create_order(request):
    rtn_msg = {}
    if request.method == 'POST':
        selected_item = request.POST['selected_item']
        purchase_num = int(request.POST.get('purchase_num', 0))
        is_vip = request.POST['is_vip']

        selected_item = Product.objects.get(product_id=selected_item)
        selected_item.stock_pcs -= purchase_num
        selected_item.save()
        
        order_id = uuid.uuid4()
        order_info = Order(order_id=order_id,
                           product_id=selected_item.product_id,
                           qty=purchase_num,
                           price=selected_item.price,
                           shop_id=selected_item.shop_id)
        order_info.save()

        rtn_msg = {'purchase_receipt': {'product_id': selected_item.product_id,
                                        'order_id': order_id,
                                        'qty': purchase_num,
                                        'price': selected_item.price,
                                        'shop_id': selected_item.shop_id},
                   'product_stock_pcs': selected_item.stock_pcs,}

        return JsonResponse(rtn_msg)
    else:
        return HttpResponseBadRequest()

@is_order_exist
@transaction.atomic
def delete_order(request, order_id):
    if request.method == 'DELETE':
        deleted_order = Order.objects.get(order_id=order_id)
        
        deleted_product_id = deleted_order.product_id
        add_back_stock_pcs = deleted_order.qty
        
        product_info = Product.objects.get(product_id=deleted_product_id)
        if not product_info.stock_pcs:
            product_id = product_info.product_id
            system_console_msg = f"刪除訂單成功，商品 {product_id} 到貨"
        else:
            system_console_msg = "刪除訂單成功"
        
        product_info.stock_pcs += add_back_stock_pcs

        product_info.save()
        deleted_order.delete()

        return JsonResponse({'deleted_product_id': deleted_product_id,
                             'product_stock_pcs': product_info.stock_pcs,
                             'system_console_msg': system_console_msg})
    else:
        return HttpResponseBadRequest()

def index(request):
    products = Product.objects.all().values()
    orders = Order.objects.all().values()
    context = {'product_info': Product.get_attr(),
               'products': list(products),
               'order_info': Order.get_attr(),
               'orders': list(orders)}

    return render(request, 'index.html', context)

def get_order_stat(request):
    rtn_data = {'top1': 'No Top1',
                'top2': 'No Top2',
                'top3': 'No Top3'}

    sold_stat = Order.objects.values('product_id').annotate(sold_qty=Sum('qty')).order_by('-sold_qty')
    top3_product = sold_stat[:3]

    for idx in range(len(top3_product)):
        product_id = sold_stat[idx]['product_id']
        sold_qty = sold_stat[idx]['sold_qty']
        rtn_data[f'top{idx+1}'] = f'product-{product_id}, sold_qty: {sold_qty}'

    return JsonResponse(rtn_data)

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")
register_events(scheduler)

def get_shop_stat():
    orders_info = pd.DataFrame(list(Order.objects.all().values()))
    if orders_info.empty:
        return
    shops_list = Product.objects.values_list('shop_id',
                                             flat=True).distinct()
    statistic_name = ['total_sold_amount',
                      'total_sold_qty',
                      'total_orders']

    output = pd.DataFrame(columns=shops_list, index=statistic_name)
    shops_info = orders_info.groupby('shop_id')
    
    for shop_id, shop_info in shops_info:
        total_sold_amount = (shop_info['qty'] * shop_info['price']).sum()
        total_sold_qty = shop_info['qty'].sum()
        total_orders = shop_info.shape[0]
        shop_stat = [total_sold_amount,
                     total_sold_qty,
                     total_orders]

        output[shop_id] = shop_stat
    
    #static/output.csv
    csv_file_name = 'report_csv.csv'
    csv_path = os.path.join(djangoSettings.STATICFILES_DIRS[0], csv_file_name)
    output.to_csv(csv_path, na_rep=0)

scheduler.add_job(get_shop_stat,
                  "interval",
                  id='get_shop_stat',
                  hours=1)
scheduler.start()



