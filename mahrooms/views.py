from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse
from django.http import Http404

from .models import Board, Topic, Post
from django.contrib.auth.models import User
from .forms import NewTopicForm

from django.contrib.auth.decorators import login_required

def home(request):
     boards=Board.objects.all()
     return render(request, 'home.html', {'boards': boards})


def about(request):
     return render(request,'about.html')

def privacy_policy(request):
     return render(request,'privacy_policy.html')

def board_topics(request, pk):
    board = get_object_or_404(Board,id=pk)
    return render(request, 'topics.html', {'board': board})

@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('board_topics', pk=board.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})

def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    return render(request, 'topic_posts.html', {'topic': topic})
