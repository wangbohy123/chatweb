from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import datetime

from django.core.cache import cache

class Ordinary_UserManager(models.Manager):
    # 定义一个普通用户管理器
    def create(self, accountnum, password,
               mail, nickname, image,
               true_name, birth, tel, gender):
        # 写创建对象的方法 创建对象时可以调用该类方法
        ord = Ordinary_User()
        ord.account_number = accountnum
        ord.account_passWord = password
        ord.account_mail = mail
        ord.nickname = nickname
        ord.true_name = true_name
        ord.birth = birth
        ord.tel = tel
        ord.gender = gender
        ord.avatar = image
        ord.save()
        return ord

    def if_has(self, uname):
        try:
            self.get(account_number=uname)
        except:
            return False
        return True

    def modify_password(self, uid, newpass, newmail):
        # 修改信息的时候调用该函数
        user = self.filter(id=uid)

        if newmail != '':
            user.update(account_mail = newmail)

        user.update(account_passWord=newpass)
        return True

class RelationshipManager(models.Manager):
    def create(self, user, friend):
        relation = Relationship()
        relation.user = user
        relation.friend = friend
        relation.user_label = '默认标签'
        relation.friend_label = '默认标签'
        relation.save()
        return relation

    def research(self, user):
        try:
            self.filter(user=user)
        except:
            return ModuleNotFoundError


class Ordinary_User(models.Model):
    # 基本用户
    account_number = models.CharField(max_length=20) # 账号
    account_passWord = models.CharField(max_length=40)# 密码
    account_mail = models.CharField(max_length=30)#邮箱
    nickname = models.CharField(max_length=20, default=' ') # 昵称

    avatar = models.ImageField(upload_to='images/',
                              null=False,
                               blank=True)

    true_name = models.CharField(max_length=30) # 真实姓名
    birth = models.DateField()
    tel = models.CharField(max_length=11)
    gender = models.CharField(max_length=6,
                              choices=(('0', '男'), ('1', '女')))

    users = Ordinary_UserManager()
    # friends = models.ManyToManyField(self)
    def __str__(self):
        return self.account_number

    class Meta:
        # 元选项 修改表的名称
        db_table = 'ordinary_user' # 表名
        ordering = ['id'] # 指定查询的排序规则


class Relationship(models.Model):
    # user 代表用户  friend代表该用户的好友
    user = models.ForeignKey(to=Ordinary_User,
                             on_delete=models.DO_NOTHING,
                             related_name='user')

    friend = models.ForeignKey(to=Ordinary_User,
                               on_delete=models.DO_NOTHING,
                               related_name='friend')


    if_pass = models.BooleanField(default=False) # 是否通过验证

    user_label = models.CharField(max_length=64,
                                  help_text = "备注信息",
                                  default=None)

    friend_label = models.CharField(max_length=64,
                                    help_text = "备注信息",
                                    default=None)

    create_time = models.DateTimeField("添加好友时间", auto_now_add=True)
    update_time = models.DateTimeField("更新分组时间", auto_now=True)

    # resource = models.ForeignKey(ChatFriendResource, to_field="origin", on_delete=models.DO_NOTHING, help_text="好友来源")
    relate = RelationshipManager()

    def __str__(self):
        return self.user.account_number

    class Meta:
        db_table = 'relationship'
        ordering = ['id']
