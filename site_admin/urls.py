from django.urls import path
from site_admin.views import *

urlpatterns = [
    path('', AdminDashboardView.as_view(), name='admin_dashboard'),

]

