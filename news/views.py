from django.contrib.messages.views import SuccessMessageMixin

from django.http import HttpResponseNotFound, Http404
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, DetailView, View, UpdateView, CreateView, DeleteView

from .forms import CommentForm, EditPostForm, AddPostForm, FilterForm
from .models import Post, Category, Comment, Tag


class PostList(ListView):
    model = Post
    paginate_by = 4  # if pagination is desired

    def get_queryset(self):
        return self.model.objects.filter(is_approved=True, is_editing_approved=True)


class ArticlesList(ListView):
    model = Post
    template_name = 'news/home.html'

    def get_queryset(self):
        return self.model.objects.filter(user__is_staff=True, is_approved=True)[:6]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all().order_by('title')
        context['categories'] = categories
        return context


class PostDetail(DetailView):
    model = Post
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page')
        comments = Paginator(self.object.comments.filter(parent=None).order_by('-created'), 15)
        context['page_obj'] = comments.get_page(page)
        form = CommentForm()
        context['form'] = form
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.user != self.request.user and (not obj.is_approved and not obj.is_editing_approved):
            raise Http404('This post is on moderation, but it will be shown soon')
        return obj


class EditPost(SuccessMessageMixin, UpdateView):
    model = Post
    slug_field = 'slug'
    form_class = EditPostForm
    success_message = 'Thank you! The post was updated and will be shown after moderation.'

    def get_success_url(self):
        return reverse('user:profile', kwargs={'pk': self.request.user.pk})


class AddPost(SuccessMessageMixin, CreateView):
    model = Post
    template_name = 'news/post_create.html'
    form_class = AddPostForm
    success_message = 'Thank you! The post will be shown after moderation'

    def get_success_url(self):
        return reverse('user:profile', kwargs={'pk': self.request.user.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DeletePost(DeleteView):
    model = Post
    slug_field = 'slug'

    def get_success_url(self):
        return reverse('user:profile', kwargs={'pk': self.request.user.pk})


class AddComment(View):
    def post(self, request, slug, parent=None):
        instance = get_object_or_404(Post, slug=slug)
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.post = instance
            form.user = request.user
            if parent:
                form.parent = Comment.objects.get(id=parent)
            form.save()
        return redirect(instance.get_absolute_url())

    def get(self, request, slug, parent=None):
        instance = Post.objects.get(slug=slug)
        form = CommentForm()
        return render(request, 'news/add_comment.html', {'form': form, 'instance': instance})

class EditComment(SuccessMessageMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    pk_url_kwarg = 'pk'
    success_message = 'The comment was updated'
    template_name = 'news/add_comment.html'

    def get_success_url(self):
        return reverse('news:post_detail', kwargs={'slug': self.object.post.slug})

    # def get_form(self, form_class=None):
    #     form = self.form_class
    #     form.fields['text'].widget.attrs['rows'] = 5
    #     form.fields['text'].widget.attrs['placeholder'] = None
    #     return form


class DeleteComment(DeleteView):
    model = Comment
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object.post
        return context

    def get_success_url(self):
        return reverse('news:post_detail', kwargs={'slug': self.object.post.slug})


class PostFilterView(ListView):
    model = Post
    paginate_by = 4
    template_name = 'news/filter.html'

    def get_queryset(self, *args, **kwargs):
        queryset = Post.objects.filter(Q(category__title__in=self.request.GET.getlist('category')) |
                                       Q(tags__tag__in=self.request.GET.getlist('tag'))).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context['categories'] = Category.objects.all().order_by('title')
        context['tags'] = Tag.objects.all().order_by('tag')
        context["tag"] = ''.join([f"tags={x}&" for x in self.request.GET.getlist("tag")])
        context["category"] = ''.join([f"category={x}&" for x in self.request.GET.getlist("category")])
        return context


class Search(ListView):
    paginate_by = 4

    def get_queryset(self):
        q = self.request.GET.get('q').lower()
        return Post.objects.filter(Q(title__icontains=q) |
                                   Q(keywords__icontains=q)
                                   ).distinct()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = f'{self.request.GET.get("q")}&'
        return context
