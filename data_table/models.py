from django.db import models
from client.models import Ordinary_User
# Create your models here.

class DateManager(models.Manager):

    def create(self, user, thing_name, remark):
        date = Date()
        date.user = user
        date.thing_name = thing_name
        date.remark = remark
        date.save()

class Date(models.Model):

    thing_name = models.CharField(max_length=100)

    remark = models.TextField()

    user = models.ForeignKey(Ordinary_User,
                             related_name='date',
                             on_delete=models.DO_NOTHING)

    status = models.BooleanField(default=False)

    # 添加的日期
    riqi = models.DateField(auto_now=True)
    tables = DateManager()


    def __str__(self):
        return self.thing_name

    class Meta:
        db_table = 'date_table'
        ordering = ['id']