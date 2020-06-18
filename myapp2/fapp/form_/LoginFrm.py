from django import forms
# 폼 컨트롤 정의 클래스
class LoginFrm(forms.Form):
    userid = forms.CharField(max_length=80,label='아이디', required=True)