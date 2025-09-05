from django import forms
from tasks.models import Task, Comment

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "status", "priority", "end_time"]

        widgets = {
            "end_time": forms.DateTimeInput(attrs={"type": "date", "class": "form-control"})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

        self.fields["end_time"].widget.attrs["class"] += " "


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["content", "media"]
        widgets = {
            "content": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Write your comment here..."}),
            "media": forms.FileInput(
                attrs={"class": "form-control"}
            )
        }