from django.urls import path
# from rest_framework.urlpatterns import format_suffix_patterns

from jcanayls import views

urlpatterns = [
    path(r'baseManage/', views.baseManage, name='baseManage'),
    path(r'qiuduiinfo/', views.qiuduiinfo, name='qiuduiinfo'),
    path(r'guangshiqujian', views.guangshiqujian, name='guangshiqujian'),
    path(r'qujianpeilv/', views.qujianpeilv, name='qujianpeilv'),
    path(r'uploadFile/', views.uploadFile, name='uploadFile'),
    path(r'baseanayls/',views.baseanayls,name='baseanayls'),
    path(r'vsData/', views.vsData, name='vsData'),
    path(r'searchQD/', views.searchQD, name='searchQD'),
    # path(r'vsSaiGuo/', views.vsSaiGuo, name='vsSaiGuo'),
    # path(r'lookUpResult/', views.lookUpResult, name='lookUpResult'),
    # path(r'savepinglun/', views.savepinglun, name='savepinglun'),
    # path(r'filedown/',views.filedown,name='filedown'),
    # path(r'saiguo/',views.saiguo,name='saiguo'),
    # path(r'searchsaigou/',views.searchsaigou,name='searchsaigou'),
    path(r'teamHistory/',views.teamHistory),
    path(r'zhanjiMangg/',views.zhanjiMangg),
    path(r'getteamlist/',views.getteamlist),
    path(r'oddstatist/',views.oddstatist),
    path(r'odd_prase',views.odd_prase),
    path(r'article_generation/', views.article_generation),
    path(r'get_generated_article/', views.get_generated_article),
    path(r'news_show/', views.news_show),
    path(r'get_original_article_url/', views.get_original_article_url),

]

# urlpatterns = format_suffix_patterns(urlpatterns)
