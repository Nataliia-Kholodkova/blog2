from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from django.utils.text import slugify
from django.db import models
from django.urls import reverse
from PIL import Image
import os
import datetime

user = get_user_model()

def upload_post_image(instance, filename):

    file_path = os.path.join('posts', str(instance.user.id), filename)
    return file_path


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='Name')
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)


class Tag(models.Model):
    tag = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Tag'
        # verbose_name_plural = 'Tags'

    def __str__(self):
        return self.tag



class Post(models.Model):
    # del user, blog will be deleted
    user = models.ForeignKey(user, verbose_name='Author', on_delete=models.CASCADE)
    # del category, the blog will be saved
    category = models.ForeignKey(Category, null=True, verbose_name='Category', on_delete=models.SET_NULL)
    title = models.CharField(max_length=50, verbose_name='Title')
    description = models.TextField(max_length=400, verbose_name='Description')
    text = models.TextField(max_length=30000, verbose_name='Text')
    tags = models.ManyToManyField(Tag, verbose_name='Tags', null=True)
    created = models.DateTimeField(verbose_name='Date created', auto_now_add=True)
    keywords = models.CharField(verbose_name='Keywords', max_length=50)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to=upload_post_image)
    is_approved = models.BooleanField(default=False)
    is_editing_approved = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Post'
        ordering=('-created',)
        # verbose_name_plural = 'Blogs'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        try:
            super(Post, self).save(*args, **kwargs)
        except:
            print(datetime.datetime.now())
            self.slug = slugify(self.title + '-' + str(self.id))
            super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    text = models.TextField(max_length=1000, verbose_name='Comment')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Date')
    post = models.ForeignKey(Post, verbose_name='Post', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(user, verbose_name='Author', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Comment'

    def __str__(self):
        return self.text
    @property
    def is_parent(self):
        print(self.replies.all())
        print(self.replies.count())
        if self.replies.count() > 0:
            return True
        return False

@receiver(post_delete, sender=Post)
def delete_news(sender, instance, **kwargs):
    instance.image.delete(False)

@receiver(post_save, sender=Post)
def save_img(sender, instance, **kwargs):
    if not instance.image:
        return
    img = Image.open(instance.image)

    (width, height) = img.size
    "Max width and height 800"
    if (800 / width < 800 / height):
        factor = 800 / height
    else:
        factor = 800 / width

    size = (int(width // factor), int(height // factor))
    img.resize(size, Image.ANTIALIAS)
    img.save(instance.image.path)




