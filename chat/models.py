from django.db import models
from client.models import Ordinary_User
# Create your models here.

class MassageManager(models.Manager):
    def create(self, from_user, to_user, text):
        m = Massage()
        m.sender = from_user
        m.receiver = to_user
        m.massage = text
        m.save()
        return m

class Massage(models.Model):

    sender = models.ForeignKey(Ordinary_User,
                               on_delete=models.DO_NOTHING,
                               related_name='sender')

    receiver = models.ForeignKey(Ordinary_User,
                                 on_delete=models.DO_NOTHING,
                                 related_name='receiver')

    massage = models.TextField(default=None)
    massages = MassageManager()

    def __str__(self):
        return self.sender.account_number

    class Meta:
        db_table = 'massages'
        ordering = ['id']
