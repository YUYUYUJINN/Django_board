from django import forms
from board.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'contents')  # 입력 받고 싶음
        exclude = ('writer', )  # 입력 받고 싶지 않음
