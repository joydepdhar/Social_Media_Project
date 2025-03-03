from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text', 'image']
        widgets = {
            # 'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'What’s on your mind?'}),
            'text': forms.Textarea(attrs={'class': 'w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'What’s on your mind?'}),
            'image': forms.ClearableFileInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'}),
        
        }
