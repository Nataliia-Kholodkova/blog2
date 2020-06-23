from allauth.account.views import SignupView
from django.core.paginator import Paginator
from django.shortcuts import reverse
from django.views.generic import DetailView, UpdateView, DeleteView

from news.models import Post
from .forms import UserUpdateForm
from .models import User


class SighUp(SignupView):
    def get_success_url(self):
        self.success_url = reverse('user:profile_update', kwargs={'pk': self.request.user.pk})
        super().get_success_url()


class UserProfile(DetailView):
    model = User
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_list = Post.objects.filter(user=context['user'])
        paginator = Paginator(post_list, 4)
        page = self.request.GET.get('page')
        page_obj = paginator.get_page(page)
        context['page_obj'] = page_obj

        return context


class UserProfileUpdate(UpdateView):
    model = User
    pk_url_kwarg = 'pk'
    form_class = UserUpdateForm

    def get_success_url(self):
        return reverse('user:profile', kwargs={'pk': self.object.pk})


class DeleteUser(DeleteView):
    model = User
    pk_url_kwarg = 'pk'

    def get_success_url(self):
        return reverse('/')

    def delete(self, request, *args, **kwargs):
        self.object.is_active = False
        super().delete(request, *args, **kwargs)
