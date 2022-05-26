from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Entry, Topic
from .forms import EntryForm, TopicForm
# Create your views here.
def index(request):
    return render(request, 'index.html')

def topics(request):
    # Усі теми
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'topics.html', context)

def topic(request, topic_id):
    # Одна тема та всі записи
    topic = Topic.objects.get(id = topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'topic.html', context)

def new_topic(request):
    # визначає нову тему
    if request.method != 'POST':
        # Дані не відправились - пуста форма
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topics'))
    context = {'form': form}
    return render(request, 'new_topic.html', context)

def new_entry(request, topic_id):
    topic = Topic.objects.get(id = topic_id)
    
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data = request.POST)
        if form.is_valid():
            new_entry = form.save(commit = False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('topics'))

    context  = {'topic': topic, 'form': form} 
    return render(request, 'new_entry.html', context)
 