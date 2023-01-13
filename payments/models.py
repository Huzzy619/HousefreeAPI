from django.db import models
from django.contrib.auth import get_user_model
import secrets

class Payment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField()
    amount = models.PositiveIntegerField()
    txn_ref = models.CharField(max_length=200, unique=True)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)
        verbose_name_plural = 'Payments'

    def __str__(self):
        return f"Payment of {self.amount} by {self.user} on {self.date_created}"

    def save(self, *args, **kwargs):
        if not self.txn_ref:
            self.txn_ref = secrets.token_urlsafe(50)
        super().save(*args, **kwargs)
