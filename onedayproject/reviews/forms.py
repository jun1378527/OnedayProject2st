from django import forms
from .models import CodeReview, Comment

class CodeReviewForm(forms.ModelForm):
    class Meta:
        model = CodeReview
        fields = ['title', 'content']
class TreeForm(forms.Form):
    elements = forms.CharField(label='요소들을 입력하세요 (공백으로 구분)')
    traversal_type = forms.ChoiceField(
        choices=[('preorder', '전위'), ('inorder', '중위'), ('postorder', '후위')],
        label='순회 유형을 선택하세요'
    )

class QuickSortForm(forms.Form):
    elements = forms.CharField(label='요소들을 입력하세요 (공백으로 구분)')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']