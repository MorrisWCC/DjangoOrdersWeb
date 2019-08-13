function create_order(){
    var url ="/order/";
    var selected_item = $('select.selected_item').val();
    var purchase_num = $('#purchase_num').val();
    var is_vip = $('#is_vip').is(":checked");
    var customer_id = $('#customer_id').val();
    var csrf_token = $("[name='csrfmiddlewaretoken']").val()
    
    if(isNaN(purchase_num)){
        alert("Must input numbers");
        return false;
    }
    
    $.ajax({
           type:"POST",
           url: url,
           data: {"selected_item": selected_item,
                  "purchase_num": purchase_num,
                  "is_vip": is_vip,
                  "csrfmiddlewaretoken": csrf_token},
           success: function(result){
               new_order_record = `
                <tr id='order-${result.purchase_receipt.order_id}'>
                    <td>${result.purchase_receipt.order_id}</td>
                    <td>${result.purchase_receipt.product_id}</td>
                    <td>${result.purchase_receipt.qty}</td>
                    <td>${result.purchase_receipt.price}</td>
                    <td>${result.purchase_receipt.shop_id}</td>
                    <td>${customer_id}</td>
                    <td><button onclick="delete_order('${result.purchase_receipt.order_id}')" class="delete_btn">－</button></td>
                <tr>
               `
               $("#order_history tbody").append(new_order_record);

               var cur_product_stock_pcs = result.product_stock_pcs;
               $("#product-" + selected_item).find('td:eq(1)').html(cur_product_stock_pcs);
                $("#system_console").html('下訂成功');
           },
           error: function(result){
                console.log(result)
               if(result.status == 403){
                    $("#system_console").html('權限不足');
               }
               else if(result.responseJSON.error_msg == 'out_of_stock'){
                    $("#system_console").html('庫存不足');
               }
           }});
    
    return false;
};

function delete_order(delete_order_id){
    var url = "/order/" + delete_order_id;
    var csrf_token = $("[name='csrfmiddlewaretoken']").val()

    $.ajax({
            type: "DELETE",
            url: url,
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            },
            success:function(result){
                var deleted_product_id = result.deleted_product_id;
                var product_stock_pcs = result.product_stock_pcs;
                var system_console_msg = result.system_console_msg;

                $("#product-" + deleted_product_id).find('td:eq(1)').html(product_stock_pcs);
                $('#order-' + delete_order_id).remove();
                $("#system_console").html(system_console_msg)

            },
            error: function(result){
                    if(result.status == 404){
                        $("#system_console").html("查無此單");
                    }
                    else{
                        $("#system_console").html("刪除失敗");
                    }
            }});
        
    return false;
};

function get_order_static(){
    var url = "stat/order";
    $.ajax({
            type: "GET",
            url: url,
            success:function(result){
                top3_info = `
                            <h1>TOP1: ${result.top1}</h1>
                            <h2>TOP2: ${result.top2}</h2>
                            <h3>TOP3: ${result.top3}</h3>
                            `;
                $("#top3_info").html(top3_info);
            },
            error: function(result){
                alert("Get order stat failed");
            }});
    
    return false;
};

