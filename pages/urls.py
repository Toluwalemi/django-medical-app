from django.urls import path

from pages.views.general import StatPageView, HomePageView
from pages.views.patients import show_login, show_signup, show_logout, PatientCreateView
from pages.views.practitioner import login_page, logout_page, signup_page, show_doc_info

app_name = 'pages'

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('stat/', StatPageView.as_view(), name='stat_page'),
    path('report/', PatientCreateView.as_view(), name='patient_home'),
    path('dashboard/', show_doc_info, name='practitioner_home'),
    path('accounts/login/', show_login, name='patient_login'),
    path('accounts/signup/', show_signup, name='patient_signup'),
    path('accounts/logout/', show_logout, name='patient_logout'),
    path('accounts/p/login/', login_page, name='practitioner_login'),
    path('accounts/p/signup/', signup_page, name='practitioner_signup'),
    path('accounts/p/logout/', logout_page, name='practitioner_logout'),
]
