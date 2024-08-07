from django.urls import path
from .views import home, register_customer, register_driver, about, SignInView, logout_view, mission, services, pricing, create_schedule, cancel_schedule, settings, issues_dashboard, report_issue


urlpatterns = [
    path('', home, name='home'),
    path('register/customer/', register_customer, name='register_customer'),
    path('register/driver/', register_driver, name='register_driver'),
    path('about/', about, name='about'),
    path('mission/', mission, name='mission'),
    path('services/', services, name='services'),
    path('pricing/', pricing, name='pricing'),
    path('settings/', settings, name='settings'),
    path('create_schedule/', create_schedule, name='create_schedule'),
    path('cancel-schedule/<int:schedule_id>/', cancel_schedule, name='cancel_schedule'),
    path('issues/', issues_dashboard, name='issues_dashboard'),
    path('report-issue/', report_issue, name='report_issue'),
    path('sign_in/customer/', SignInView.as_view(), name='sign_in_customer'),
    path('logout/', logout_view, name='logout'),
]
