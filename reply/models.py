from django.contrib.auth.models import User
from django.db import models


class Reply(models.Model):
    contents = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)  # 회원 가입 되어 있는 사용자만 사용할 수 있음
