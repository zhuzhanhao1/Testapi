from django import forms
from .models import *

class LoginForm(forms.ModelForm):
    class Meta:
        #指定关联的Ｍｏｄｅｌ
        model = User
        #指定要生成控件的属性们
        fields = ['uphone','upwd']
        #指定控件们对应的标签
        labels = {
            'uphone':'手机号码',
            'upwd':'密码'
        }
        #指定控件对应的小部件
        widgets = {
            'uphone':forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'请输入11位的手机号码',
                    'id':'uphone'
                }
            ),
            'upwd':forms.PasswordInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'请输入密码',
                    'id':'upwd'
                }
            )
        }
