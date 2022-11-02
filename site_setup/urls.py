from django.urls import path
from site_setup.views import *


urlpatterns = [
    path('site-info', SiteInfoView.as_view(), name='site_info'),
    path('site-info/create', SiteInfoCreateView.as_view(), name='site_info_create'),
    path('site-info/<int:pk>/update', SiteInfoUpdateView.as_view(), name='site_info_update'),

    path('banner/register', SiteHeroCreateView.as_view(), name='banner_create'),
    path('banner/index', SiteHeroListView.as_view(), name='banner_index'),
    path('banner/<int:pk>/edit', SiteHeroUpdateView.as_view(), name='banner_edit'),
    path('banner/<int:pk>/delete', SiteHeroDeleteView.as_view(), name='banner_delete'),

]

