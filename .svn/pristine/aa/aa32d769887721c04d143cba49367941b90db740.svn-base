from django.urls import path, re_path
from django.views.static import serve

from auto_ui.settings import MEDIA_ROOT
from home import views

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    # url(r'^.*\.html', views.gentella_html, name='gentella'),

    # The home page
    path(r'', views.index, name='index'),
    re_path(r'image/(?P<path>.*)/', serve, {"document_root": MEDIA_ROOT}),
    path(r'login/', views.login_action),
    path(r'logout/',views.logout),
]
