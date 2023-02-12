from django import forms
from .models import Post, PostImage
from socialapp.models import Group


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that only members of the current user
                are given as options"""

        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['group'].queryset = Group.objects.filter(members=self.user)

    group = forms.ModelChoiceField(
        queryset=None, initial='Choose group to post in'
    )

    class Meta:
        model = Post
        fields = ['title', 'message', 'group']


class PostImageForm(forms.ModelForm):
    image = forms.ImageField(
        label='Image',
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )

    class Meta:
        model = PostImage
        fields = ['image']

