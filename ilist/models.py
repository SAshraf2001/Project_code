from django.db import models

# Create your models here.

class Status(models.Model):
    statusName = models.CharField(max_length=20)

    def __str__(self):
        return self.statusName

class Todo(models.Model):
    todo_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    content = models.TextField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
