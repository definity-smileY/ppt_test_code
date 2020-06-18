"""fapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from fapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.doMessage, name="message"),
    #빈도수 검색기 폼화면
    path("fapp/message/", views.doMessage, name="message"),
    #ajax가 리퀘스트 URL과 함수
    path("fapp/message2/", views.doMessage2, name="message2"),
    path("fapp/date/",views.doDate, name="date"),
    path("fapp/time/",views.doTime, name="time"),
    #공적마스크재고수량 폼화면
    path("fapp/mask/", views.doMask, name="mask"),
    path("fapp/mask2/", views.doMask2, name="mask2"),
    #공적마스그 폼화면
    path("fapp/map/", views.domap, name="map"),

    # ajax가 리퀘스트 url과 함수
    path("fapp/message_graph_pie2/", views.message_graph_pie2, name="message_graph_pie2"),
    path("fapp/message_graph_pie/", views.message_graph_pie, name="message_graph_pie"),

    path("fapp/graph_pie2/",views.graph_pie2,name="graph_pie2"),
    path("fapp/graph_pie/",views.graph_pie,name="graph_pie"),

    path("fapp/chart_pie", views.chart_pie,name="chart_pie"),

    # 폼화면
    path("fapp/page_move1/", views.page_move1, name="page_move1"),
    # AJAX 네이버 요청
    path("fapp/page_move1_proc/", views.page_move1_proc, name="page_move1_proc"),

    # 폼화면
    path("fapp/page_class/",views.page_class,name="page_class"),

    # 다중상속폼화면
    path("fapp/page_class_mp/", views.page_class_mp, name="page_class_mp"), 
    
    # 인터페이스폼화면
    path("fapp/page_inserface_mp/", views.page_inserface_mp, name="page_inserface_mp"),

    # 로그인 폼
    path("fapp/go_login/", views.go_login, name="go_login"),
    # ajax
    path("fapp/go_login_proc/", views.go_login_proc, name="go_login_proc"),
    
    # 주소
    # 폼
    path("fapp/go_juso/", views.go_juso, name="go_juso"),
    # 에이작스
    path("fapp/go_juso_proc/",views.go_juso_proc,name="go_juso_proc"),

    # world
    path("fapp/world_view/", views.world_view, name="world"),
    # 평균
    # 폼
    path("fapp/go_gmean/", views.go_gmean, name="go_gmean"),
    # 수집/저장
    path("fapp/go_gmean_save/", views.go_gmean_save, name="go_gmean_save"),
    # 처리
    path("fapp/go_gmean_proc/", views.go_gmean_proc, name="go_gmean_proc"),
    #편차
    # 폼
    path("fapp/go_deviation/", views.go_deviation, name="go_deviation"),
    # 수집/저장/처리/분석
    path("fapp/go_deviation_save/", views.go_deviation_save, name="go_deviation_save"),
]
