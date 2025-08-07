from django.shortcuts import render
from django.contrib import messages


from .models import Todo, Status
# Create your views here.
def content(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        statusId = request.POST['status']
        
        status_obj = Status.objects.get(statusName=statusId)
        my_cont = Todo(title=title, content=content, status=status_obj)
        my_cont.save()
        messages.success(request, 'Your task has been submitted successfully:')
    statuses = Status.objects.all()
    return render(request, 'todo/todohome.html', {'statuses':statuses})

def displayTodo(request):
    alllist = Todo.objects.all()
    context = {
        'allList':alllist
    }
    return render(request, 'todo/viewAll.html', context)

