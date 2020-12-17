from django.db import models
from client.models import Ordinary_User
# Create your models here.

class CommentManager(models.Manager):

    def create(self, sender, recevier, saying):
        comment = Comment()
        comment.sender = sender
        comment.recevier = recevier
        comment.saying = saying
        comment.save()
        return comment


class Comment(models.Model):

    saying = models.TextField()

    sender = models.ForeignKey(Ordinary_User,
                               related_name='send_comm',
                               on_delete=models.DO_NOTHING)

    recevier = models.ForeignKey(Ordinary_User,
                                 related_name='receiv_comm',
                                 on_delete=models.DO_NOTHING)
    comments = CommentManager()

    def __str__(self):
        return self.sender.account_number

    class Meta:
        db_table = 'comments'
        ordering = ['id']
