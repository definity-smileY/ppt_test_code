from django import forms

# 폼 컨트롤 정의 클래스
class Meanfrm(forms.Form):
    # 히든
    theme_sel_val = forms.CharField(widget=forms.HiddenInput())

    # 주제
    theme = forms.CharField(label='1. 주제(수집할 검색어)', required=True, widget=forms.TextInput(attrs={'placeholder':'수집할 검색어', 'style':'width:200px', 'class':'form-control'}))

    # 수집 컬렉션이름
    ADDR =(
        ('1','검색하세요'),
    ) 
    theme_sel = forms.ChoiceField(choices=ADDR, label='2. 처리/분석')
