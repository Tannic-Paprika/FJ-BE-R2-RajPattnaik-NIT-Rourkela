"""
URL configuration for Fj_task project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from main_app.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('home/', home, name='home'),
    path('admin/', admin.site.urls),
    path('login/', login_page, name='login_page'),
    path('register/', register_page, name='register'),
    path('add_income/', add_income, name='add_income'),
    path('edit_income/<int:pk>/', edit_income, name='edit_income'),
    path('delete_income/<int:pk>/', delete_income, name='delete_income'),
    path('add_expense/', add_expense, name='add_expense'),
    path('edit_expense/<int:pk>/', edit_expense, name='edit_expense'),
    path('delete_expense/<int:pk>/', delete_expense, name='delete_expense'),
    path('add_transaction/', add_transaction, name='add_transaction'),
    path('edit_transaction/<int:pk>/', edit_transaction, name='edit_transaction'),
    path('delete_transaction/<int:pk>/', delete_transaction, name='delete_transaction'),
    path('budget-goals/add/', add_budget_goal, name='add_budget_goal'),
    path('budget-goals/edit/<int:budget_goal_id>/', edit_budget_goal, name='edit_budget_goal'),
    path('budget-goals/delete/<int:budget_goal_id>/', delete_budgetgoal, name='delete_budget_goal'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()