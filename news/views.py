from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, View

from .models import News

class NewsList(ListView):
    model = News
    paginate_by = 10  # if pagination is desired

class NewsDetail(DetailView):
    model = News
    slug_field = 'slug'
