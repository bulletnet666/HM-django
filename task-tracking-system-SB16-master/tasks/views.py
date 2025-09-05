from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from tasks.models import Task, Comment
from tasks.forms import TaskForm, CommentForm
from django.urls import reverse_lazy
from tasks.mixins import UserIsOwnerMixin

# Create your views here.
class TaskListView(ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "tasks/task_list.html"


class TaskDetailView(DetailView):
    model = Task
    context_object_name = "task"
    template_name = "tasks/task_detail.html"

    def get_context_data(self, **kwargs):
        content = super().get_context_data()
        content["comment_form"] = CommentForm()
        return content

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST, request.FILES)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.task = self.get_object()
            comment.save()
            return redirect("task-detail", pk=comment.task.pk)
        else:
            pass

class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_update_form.html"
    success_url = reverse_lazy("task-list")


class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("task-list")


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task-list")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


# View for comments
class CommentEditView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "tasks/comment_edit_form.html"

    def form_valid(self, form):
        comment = self.get_object()
        if comment.author != self.request.user:
            raise PermissionDenied("You cannot edit this comment")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("task-detail", kwargs={"pk": self.object.task.pk})

class CommentDeleteView(LoginRequiredMixin, DetailView):
    model = Comment
    template_name = "tasks/comment_delete.html"

    def get_success_url(self):
        return reverse_lazy("task-detail", kwargs={"pk": self.object.task.pk})