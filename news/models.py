from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save
from django.utils.text import slugify
from django.db import models
from django.urls import reverse
from PIL import Image

user = get_user_model()

def upload_post_image(instance, filename):
    file_path = 'news/{}/{}-{}'.format(instance.user.id, instance.slug, filename)
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


class News(models.Model):
    # del user, blog will be deleted
    user = models.ForeignKey(user, verbose_name='Author', on_delete=models.CASCADE)
    # del category, the blog will be saved
    category = models.ForeignKey(Category, null=True, verbose_name='Category', on_delete=models.SET_NULL)
    title = models.CharField(max_length=50, verbose_name='Title')
    description = models.TextField(max_length=350, verbose_name='Description')
    text = models.TextField(max_length=5000, verbose_name='Text')
    tags = models.ManyToManyField(Tag, verbose_name='Tags', null=True)
    created = models.DateTimeField(verbose_name='Date created', auto_now_add=True)
    keywords = models.CharField(verbose_name='Keywords', max_length=50)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to=upload_post_image)

    class Meta:
        verbose_name = 'Blog'
        # verbose_name_plural = 'Blogs'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:news_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(News, self).save(*args, **kwargs)

@receiver(post_delete, sender=News)
def delete_news(sender, instance, **kwargs):
    instance.image.delete(False)

@receiver(pre_save, sender=News)
def save_img(sender, instance, **kwargs):
    img = Image.open(instance.image)
    (width, height) = img.size
    "Max width and height 800"
    if (1200 / width < 1200 / height):
        factor = 1200 / height
    else:
        factor = 1200 / width

    size = (int(width // factor), int(height // factor))
    img.resize(size, Image.ANTIALIAS)
    img.save(instance.image.path)




