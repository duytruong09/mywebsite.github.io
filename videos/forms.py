from django import forms


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form_control',
            'placeholder': 'Leave a comment',
        }
    ))