from web.models import Product, Order
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from functools import wraps

def is_in_stock(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        product_id = args[0].POST.get('selected_item', None)
        if not product_id:
            return JsonResponse(status=400,
                                data={'error_msg': 'no_selected_item'})
        
        product_info = Product.objects.get(product_id=product_id)
        if not product_info:
            return JsonResponse(status=400,
                                data={'error_msg': 'no_this_selected_item'})
        
        cur_stock_pcs = product_info.stock_pcs
        purchase_num = args[0].POST.get('purchase_num', None)
        if not purchase_num:
            return JsonResponse(status=400,
                                data={'error_msg': 'purchase_num_error'})
        
        if cur_stock_pcs < int(purchase_num):
            return JsonResponse(status=400,
                                data={'error_msg': 'out_of_stock'})

        return func(*args, **kwargs)
    return wrapper

def is_vip(func): 
    @wraps(func)
    def wrapper(*args, **kwargs): 
        is_vip = args[0].POST.get('is_vip', None)
        if is_vip is None:
            return JsonResponse(status=400,
                                data={'error_msg': 'is_vip error'})

        product_id = args[0].POST.get('selected_item', None)
        if not product_id:
            return JsonResponse(status=400,
                                data={'error_msg': 'no_selected_item'})

        product_info = Product.objects.get(product_id=product_id)
        if not product_info:
            return JsonResponse(status=400,
                                data={'error_msg': 'no_this_selected_item'})

        product_auth = product_info.vip
        is_vip = True if is_vip == 'true' else False
        if product_auth and not is_vip:
            return JsonResponse(status=403,
                                data={'error_msg': 'no_auth'})

        return func(*args, **kwargs) 
    return wrapper

def is_order_exist(func):
    @wraps(func)
    def wrapper(*args, **kwargs): 
        order_id = kwargs['order_id']
        order_info = Order.objects.filter(order_id=order_id)
        if not order_info.exists():
            return JsonResponse(status=404,
                                data={'error_msg': 'no_this_order'})
        return func(*args, **kwargs) 
    return wrapper

