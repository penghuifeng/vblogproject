from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

#定义自己的用户模型
class User(AbstractUser):
    nickname = models.fields.CharField('昵称', max_length=32)
    email = models.fields.EmailField('邮箱')

    class Meta(AbstractUser.Meta):
        pass

    def __str__(self):
        return self.email + self.nickname