from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(IncomeSource)
admin.site.register(Expenses)
admin.site.register(Transactions)
