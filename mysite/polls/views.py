from genericpath import exists
from django.http import HttpResponse
from django.template import loader
from .models import T_PAYMENT
from polls import my_logic 
from django.shortcuts import render
import datetime
from .forms import T_PAYMENT_FORM
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
import pprint

# ** 
# Payment 遷移
#   
#
# **
def index(request):
    try:
        late_date = request.POST['late_date']
    except:
        late_date = str(datetime.datetime.today().date()+datetime.timedelta(days=1))

    try :
        begin_date = request.POST['begin_date']
    except:
        begin_date  = str(datetime.datetime.today().year)+"-"+str(datetime.datetime.today().month)+"-01"

    payment_obj_list = T_PAYMENT.objects.select_related(
            'customer_id','payment_kind_id'
        ).filter(
            updated_at__range = [begin_date,late_date]
        ).filter(
            payment_valid_flg = True
        )

    #取得したobjectの合計値を算出する
    payment_total = my_logic.total_payment(payment_obj_list)
    payment_form_list  = my_logic.payment_form_list(payment_obj_list)
    template = loader.get_template('polls/index.html')

    nav_key = 0
    payment_info_list = list()

    for payment_obj,payment_form in zip(payment_obj_list,payment_form_list):
        payment_info_list.append([payment_obj,payment_form])
    
    context = {
        'payment_info_list': payment_info_list,
        'payment_total':payment_total,
        'nav_key':nav_key,
        }
    return render(request, 'polls/index.html', context)

# ** 
# Payment 追加処理
#   
#
# **
def addPayment(request):
     #リクエストがPOSTの場合
    if request.method == 'POST':
        #リクエストをもとにフォームをインスタンス化
        userForm = T_PAYMENT_FORM(request.POST)
        if userForm.is_valid():
            userForm.save()

    #user.htmlへデータを渡す
    return redirect(to = '/polls')

# ** 
# Payment 変更処理
#    
#
# **
def savePayment(request,T_PAYMENT_id):
    if request.method == 'POST':
        #リクエストをもとにフォームをインスタンス化
        userForm = T_PAYMENT_FORM(request.POST)
        if userForm.is_valid():
            payment_obj = get_object_or_404(T_PAYMENT, pk=T_PAYMENT_id)
            payment_obj.bank_name           = userForm['bank_name'].data
            payment_obj.payment_money       = userForm['payment_money'].data
            payment_obj.payment_valid_flg   = userForm['payment_valid_flg'].data

            #オブジェクトで格納しないといけない？からこの方法では変更できない
            #payment_obj.customer_id.customer_name         = userForm['customer_id']['customer_name'].data
            #payment_obj.payment_kind_id     = userForm['payment_kind_id'].data

            payment_obj.save()
    #user.htmlへデータを渡す
    return redirect(to = '/polls')

