from django import forms
from .models import Comment, Post, Category, Tag



category_choices = [(values['title'].lower(), values['title']) for values in Category.objects.all().order_by('title').values('title')]
tag_choices = [(value['tag'], value['tag']) for value in Tag.objects.all().order_by('tag').values('tag')]
category_choices_multiple = [('category', values['title']) for values in Category.objects.all().order_by('title').values('title')]


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text', )
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-control", 'cols': 12, 'rows': 1, 'placeholder': 'What do you think?'})
        }
        labels = {
            'text': '',
        }


class EditPostForm(forms.ModelForm):
    category = forms.ChoiceField(choices=category_choices, widget=forms.RadioSelect(
                attrs={
                    'class': 'form-control',
                    'id': 'CategoryId',
                }
            ))
    tags = forms.MultipleChoiceField(choices=tag_choices, widget=forms.CheckboxSelectMultiple(
                {'class': "form-control",
                         'id': "TagsId",
                 }
            ))


    class Meta:
        model = Post
        fields = ('title', 'description', 'text', 'keywords', 'image',)
        labels = {
            'category': 'Category',
            'title': 'Title',
            'description': 'Short text',
            'text': 'Text',
            'tags': 'Tags',
            'keywords': 'Keywords',            #
            'image': 'Image',
        }
        widgets = {

            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'TitleId',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'id': 'DescriptionTextId',
                }
            ),
            'text': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'id': 'TextId',
                }
            ),

            'keywords': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'KeywordsId',
                }
            ),
            'image': forms.FileInput(
                attrs={
                    'type': "file",
                    'class': "form-control-file",
                    'id': "FileId",
                })
        }

    def save(self, commit=True):

        super().save(commit=False)

        category = ' '.join([t.capitalize() for t in self.cleaned_data['category'].split()])

        category = Category.objects.get(title=category)
        self.instance.category = category
        tags = [Tag.objects.get(tag=tag) for tag in self.cleaned_data['tags']]

        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            # This is where we actually link the pizza with toppings
            self.instance.tags.clear()
            for tag in tags:
                self.instance.tags.add(tag)

        self.save_m2m = save_m2m
        # Do we need to save all changes now?
        # Just like this
        # if commit:
        self.instance.is_editing_approved = False
        self.instance.save()
        self.save_m2m()
        return self.instance

class AddPostForm(forms.ModelForm):
    category = forms.ChoiceField(choices=category_choices, widget=forms.RadioSelect(
                attrs={
                    'class': 'form-control',
                    'id': 'CategoryId',
                }
            ))
    tags = forms.MultipleChoiceField(choices=tag_choices, widget=forms.CheckboxSelectMultiple(
                {'class': "form-control",
                         'id': "TagsId",}
            ))


    class Meta:
        model = Post
        fields = ('title', 'description', 'text', 'keywords', 'image',)
        labels = {
            'category': 'Category',
            'title': 'Title',
            'description': 'Short text',
            'text': 'Text',
            'tags': 'Tags',
            'keywords': 'Keywords',            #
            'image': 'Image',
        }
        widgets = {

            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'TitleId',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'id': 'DescriptionTextId',
                }
            ),
            'text': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'id': 'TextId',
                }
            ),

            'keywords': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'id': 'KeywordsId',
                }
            ),
            'image': forms.FileInput(
                attrs={
                    'type': "file",
                    'class': "form-control-file",
                    'id': "FileId",
                })
        }

    def save(self, commit=True):

        super().save(commit=False)
        print(self.instance)
        category = ' '.join([t.capitalize() for t in self.cleaned_data['category'].split()])

        category = Category.objects.get(title=category)
        self.instance.category = category
        tags = [Tag.objects.get(tag=tag) for tag in self.cleaned_data['tags']]

        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            # This is where we actually link the pizza with toppings
            self.instance.tags.clear()
            for tag in tags:
                self.instance.tags.add(tag)

        self.save_m2m = save_m2m
        # Do we need to save all changes now?
        # Just like this
        # if commit:
        self.instance.save()
        self.save_m2m()
        return self.instance

class FilterForm(forms.Form):
    category = forms.MultipleChoiceField(choices=category_choices_multiple, widget=forms.CheckboxSelectMultiple(
        attrs={
            'class': 'form-control',
            'id': 'CategoryId',
        }
    ))
    tags = forms.MultipleChoiceField(choices=tag_choices, widget=forms.CheckboxSelectMultiple(
        {'class': "form-control",
         'id': "TagsId", }
    ))

    class Meta:
        model = Post
        labels = {
            'category': 'Category',
            'tags': 'Tags',
        }


