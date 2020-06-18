from django import forms

# 폼 컨트롤 정의 클래스
class Devifrm(forms.Form):
    # 주제
    theme = forms.CharField(label='1. 회사이름', required=True,
     widget=forms.TextInput(attrs={'placeholder':'분석대상 회사이름', 'style':'width:200px', 'class':'form-control'}))
