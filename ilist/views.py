from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages


from .models import Todo
# Create your views here.
def content(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        status = request.POST['status']

        my_cont = Todo(title=title, content=content, status_id=status)
        my_cont.save()
        messages.success(request, 'Your task has been submitted successfully:')
    return render(request, 'todo/todohome.html')

def displayTodo(request):
    alllist = Todo.objects.all()
    context = {
        'allList':alllist
    }
    return render(request, 'todo/viewAll.html', context)