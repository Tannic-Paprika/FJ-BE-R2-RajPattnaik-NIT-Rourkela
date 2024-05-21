from django.db import models
from django.contrib.auth.models import User
from datetime import date
# Create your models here.

class IncomeSource(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return self.description

class Expenses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField() 
    shared_by = models.PositiveIntegerField(default=1)
    receipt = models.FileField(upload_to='receipts/', null=True, blank=True)  

    def __str__(self):
        return f"{self.amount} / {self.shared_by}"
    
    @property
    def split_amount(self):
        if self.shared_by > 0:
            return round(self.amount / self.shared_by, 2)
        return self.amount
    

class Transactions(models.Model):
    user=  models.ForeignKey(User, on_delete=models.CASCADE)
    date= models.DateField()
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    description= models.TextField(max_length=255)

    def __str__(self):
        return self.description
    
class BudgetGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Expenses, on_delete=models.CASCADE)
    goal_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.category.category}"