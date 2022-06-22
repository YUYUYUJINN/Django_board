from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    contents = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    # 어떤 모델과 관계를 맺을지 작성
    # User 모델을 만든 적이 없지만 장고에서 이미 만들어 두었기에 사용 가능
    # 사용자가 탈퇴할 경우 관련 게시글 삭제할 수 있도록 설정 (on_delete=models.CASCADE)

