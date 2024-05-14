from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from .models import CodeReview, Comment
from .forms import CodeReviewForm, CommentForm
from django.contrib.auth.decorators import login_required
import matplotlib
matplotlib.use('Agg') 

def home(request):
    return render(request, 'reviews/home.html')

def review_list(request):
    reviews = CodeReview.objects.all()
    return render(request, 'reviews/review_list.html', {'reviews': reviews})

def review_detail(request, pk):
    review = get_object_or_404(CodeReview, pk=pk)
    comments = review.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.review = review
            comment.save()
            return redirect('review_detail', pk=review.pk)
    else:
        comment_form = CommentForm()
    return render(request, 'reviews/review_detail.html', {'review': review, 'comments': comments, 'comment_form': comment_form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('review_list')
        else:
            messages.error(request, '유효한 걸로 다시 해주세요')
    return render(request, 'reviews/login.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '가입에 성공하셨습니다. 이제 로그인 하시면 됩니다')
            return redirect('login')
        else:
            messages.error(request, '가입에 실패하셨습니다. 유효한 아이디와 비밀번호로 가입해주세요')
    else:
        form = UserCreationForm()
    return render(request, 'reviews/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def create_review(request):
    if request.method == 'POST':
        form = CodeReviewForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user  # 작성자를 현재 사용자로 설정
            form.save()
            return redirect('review_list')
    else:
        form = CodeReviewForm()
    return render(request, 'reviews/create_review.html', {'form': form})

@login_required
def delete_review(request, pk):
    review = get_object_or_404(CodeReview, pk=pk)
    if request.method == 'POST':
        review.delete()
        return redirect('review_list')
    return render(request, 'reviews/delete_review.html', {'review': review})

def graph_visualization(request):
    return render(request, 'reviews/graph_visualization.html')

def heap_tree(request):
    if request.method == 'POST':
        elements = request.POST.get('elements')
        elements = list(map(int, elements.split()))
        # 힙 트리 생성 및 시각화 로직 추가
        # 예를 들어, 힙 정렬 과정을 시각화하기 위한 데이터를 생성
        visualization_data = heap_sort_visualization(elements)
        return render(request, 'reviews/heap_tree.html', {'data': visualization_data})
    return render(request, 'reviews/heap_tree.html')

import matplotlib
matplotlib.use('Agg')  # 백엔드를 Agg로 설정

import matplotlib.pyplot as plt
import networkx as nx
from collections import deque
import io
import urllib, base64
import numpy as np
from django.shortcuts import render
from .forms import TreeForm, QuickSortForm

# 한글 폰트를 설정합니다.
plt.rcParams['font.family'] = 'NanumGothic'

class Node:
    def __init__(self, data=None):
        self.data = data
        self.left_child = None
        self.right_child = None

    def insert(self, data):
        if self.data is None:
            self.data = data
        else:
            queue = deque([self])
            while queue:
                current = queue.popleft()
                if not current.left_child:
                    current.left_child = Node(data)
                    break
                else:
                    queue.append(current.left_child)

                if not current.right_child:
                    current.right_child = Node(data)
                    break
                else:
                    queue.append(current.right_child)

def draw_tree(tree_root, visited=None):
    if not tree_root or not visited:
        return

    G = nx.DiGraph()
    labels = {}
    pos = {}

    def _draw(node, x=0, y=0, level=1):
        if node:
            pos[node.data] = (x, y)
            labels[node.data] = str(node.data)
            if node.left_child:
                G.add_edge(node.data, node.left_child.data)
                _draw(node.left_child, x - 1 / level, y - 1, level + 1)
            if node.right_child:
                G.add_edge(node.data, node.right_child.data)
                _draw(node.right_child, x + 1 / level, y - 1, level + 1)

    _draw(tree_root)
    color_map = ['green' if node in visited else 'lightblue' for node in G]
    fig, ax = plt.subplots(figsize=(10, 6))
    nx.draw(G, pos, labels=labels, with_labels=True, node_size=500, node_color=color_map, font_size=10, font_color='darkred', arrowstyle='-|>')
    plt.title('트리 구조')
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    plt.close(fig)
    return uri

def interactive_traversal(root, traversal_type):
    steps = []
    def preorder(node, path=[]):
        if node:
            path.append(node.data)
            steps.append(list(path))
            preorder(node.left_child, path)
            preorder(node.right_child, path)
            path.pop()

    def inorder(node, path=[]):
        if node:
            inorder(node.left_child, path)
            path.append(node.data)
            steps.append(list(path))
            inorder(node.right_child, path)
            path.pop()

    def postorder(node, path=[]):
        if node:
            postorder(node.left_child, path)
            postorder(node.right_child, path)
            path.append(node.data)
            steps.append(list(path))
            path.pop()

    if traversal_type == "preorder":
        preorder(root)
    elif traversal_type == "inorder":
        inorder(root)
    elif traversal_type == "postorder":
        postorder(root)
    else:
        return None

    images = []
    for step in steps:
        img_uri = draw_tree(root, visited=set(step))
        images.append(img_uri)
    return images

def binary_tree(request):
    if request.method == 'POST':
        form = TreeForm(request.POST)
        if form.is_valid():
            elements = list(map(int, form.cleaned_data['elements'].split()))
            traversal_type = form.cleaned_data['traversal_type']
            root = Node(elements[0])
            for el in elements[1:]:
                root.insert(el)
            images = interactive_traversal(root, traversal_type)
            return render(request, 'reviews/binary_tree.html', {'form': form, 'images': images})
    else:
        form = TreeForm()
    return render(request, 'reviews/binary_tree.html', {'form': form})

def heapify(arr, n, i, steps):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and arr[i] < arr[l]:
        largest = l

    if r < n and arr[largest] < arr[r]:
        largest = r

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        steps.append(arr.copy())
        heapify(arr, n, largest, steps)

def heap_sort(arr):
    n = len(arr)
    steps = [arr.copy()]

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, steps)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        steps.append(arr.copy())
        heapify(arr, i, 0, steps)

    return steps

def draw_heap_tree(arr):
    fig, ax = plt.subplots(figsize=(10, 6)) # 크기 조정
    n = len(arr)
    levels = np.floor(np.log2(np.arange(1, n + 1))).astype(int)
    positions = np.arange(1, n + 1) - 2 ** levels + 1
    width = 2 ** (np.max(levels) + 1)
    pos_x = positions / width
    pos_y = 1 - levels / (np.max(levels) + 2)

    G = nx.DiGraph()
    labels = {}
    pos = {}

    for i in range(n):
        pos[arr[i]] = (pos_x[i], pos_y[i])
        labels[arr[i]] = str(arr[i])
        if 2 * i + 1 < n:
            G.add_edge(arr[i], arr[2 * i + 1])
        if 2 * i + 2 < n:
            G.add_edge(arr[i], arr[2 * i + 2])

    color_map = ['lightgreen'] * n
    nx.draw(G, pos, labels=labels, with_labels=True, node_size=500, node_color=color_map, font_size=10, font_color='darkred', arrowstyle='-|>')
    plt.title('힙 트리 구조')
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    plt.close(fig)
    return uri

def heap_tree(request):
    if request.method == 'POST':
        elements = request.POST.get('elements')
        elements = list(map(int, elements.split()))
        steps = heap_sort(elements)
        images = [draw_heap_tree(step) for step in steps]
        return render(request, 'reviews/heap_tree.html', {'images': images})
    return render(request, 'reviews/heap_tree.html')

# Quick Sort 시각화를 위한 코드
def quick_sort_visualize(arr):
    steps = []

    def _quick_sort(arr, low, high, depth=0):
        if low < high:
            pi = partition(arr, low, high)
            steps.append((arr.copy(), depth))
            _quick_sort(arr, low, pi - 1, depth + 1)
            _quick_sort(arr, pi + 1, high, depth + 1)

    def partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    _quick_sort(arr, 0, len(arr) - 1)
    steps.append((arr.copy(), -1))  # 마지막 정렬 완료 단계
    return steps

def draw_quick_sort_tree(arr, depth):
    fig, ax = plt.subplots(figsize=(10, 6))
    n = len(arr)
    levels = np.zeros(n, dtype=int)
    if depth != -1:
        for i in range(n):
            levels[i] = depth
    positions = np.arange(1, n + 1)
    width = n
    pos_x = positions / width
    pos_y = 1 - levels / (np.max(levels) + 2)

    G = nx.DiGraph()
    labels = {}
    pos = {}

    for i in range(n):
        pos[arr[i]] = (pos_x[i], pos_y[i])
        labels[arr[i]] = str(arr[i])
        if 2 * i + 1 < n:
            G.add_edge(arr[i], arr[2 * i + 1])
        if 2 * i + 2 < n:
            G.add_edge(arr[i], arr[2 * i + 2])

    color_map = ['lightgreen'] * n
    nx.draw(G, pos, labels=labels, with_labels=True, node_size=500, node_color=color_map, font_size=10, font_color='darkred', arrowstyle='-|>')
    plt.title('퀵 정렬 과정')
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    plt.close(fig)
    return uri

def quick_sort(request):
    if request.method == 'POST':
        form = QuickSortForm(request.POST)
        if form.is_valid():
            elements = list(map(int, form.cleaned_data['elements'].split()))
            steps = quick_sort_visualize(elements)
            images = [draw_quick_sort_tree(step, depth) for step, depth in steps]
            return render(request, 'reviews/quick_sort.html', {'form': form, 'images': images})
    else:
        form = QuickSortForm()
    return render(request, 'reviews/quick_sort.html', {'form': form})

