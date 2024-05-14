from django.shortcuts import render, get_object_or_404
from .models import CodeReview

def review_list(request):
    reviews = CodeReview.objects.all()
    return render(request, 'reviews/review_list.html', {'reviews': reviews})

def review_detail(request, pk):
    review = get_object_or_404(CodeReview, pk=pk)
    return render(request, 'reviews/review_detail.html', {'review': review})
