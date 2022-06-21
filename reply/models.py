from django.contrib.auth.models import User
from django.db import models

from board.models import Post


class Reply(models.Model):
    contents = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # 댓글 모델과 포스트 모델 관계를 맺음
    writer = models.ForeignKey(User, on_delete=models.CASCADE)  # 회원 가입 되어 있는 사용자만 사용할 수 있음
