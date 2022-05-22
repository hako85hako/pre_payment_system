from django import forms
from .models import T_PAYMENT
 
class T_PAYMENT_FORM(forms.ModelForm):
    class Meta:
        model = T_PAYMENT
        fields = ('bank_name','payment_date', 'payment_money','payment_memo','customer_id','payment_kind_id', 'payment_valid_flg' )
        labels={
            'bank_name'         :'銀行名',
            'payment_date'      :'支払い日',
            'payment_money'     :'支払い金額',
            'payment_memo'      :'メモ',
            'customer_id'       :'客先ID',
            'payment_kind_id'   :'支払い種別ID',
            'payment_valid_flg' :'有効',
           }