from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


from .models import Post, User, Category
from .filters import PostFilter
from .forms import PostForm


class PostList(ListView):
    model = Post
    ordering = '-time_create_post'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context


class PostSearch(ListView):
    model = Post
    ordering = '-time_create_post'
    template_name = 'post_search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'news_one.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['user_auth'] = self.request.user.is_authenticated
        id = self.kwargs.get('pk')
        post = Post.objects.get(pk=id)
        is_subscribersuser = True
        for cat in post.category.all():
            if self.request.user not in cat.subscribers.all():
                is_subscribersuser = False
        context['is_subscribersuser'] = is_subscribersuser
        return context


class PostCreate(CreateView, PermissionRequiredMixin, LoginRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('post.add_post')

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.method == 'POST':
            path_info = self.request.META['PATH_INFO']
            if path_info == '/news/create/':
                post.choice = 'News'
            elif path_info == '/articles/create/':
                post.choice = 'Arti'
        post.save()
        return super().form_valid(form)


class PostEdit(UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('post.change_post')


class PostDelete(DeleteView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = ('post.delete_post')

class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.genre = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.genre).order_by('-time_create_post')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.genre.subscribers.all()
        context['category'] = self.genre
        return context

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категорий'
    return render(request, 'subscribe.html', {'category': category, 'message': message})

#@login_required
#def subscribe(request, pk):
#    user = User.objects.get(pk=request.user.id)
#    post = Post.objects.get(pk=pk)
#    category = post.category.all()
#    for cat in category:
#        if user not in cat.subscribers.all():
#            cat.subscribers.add(user)
#    return redirect('/news/')
#
#
#@login_required
#def unsubscribe(request, pk):
#    user = User.objects.get(pk=request.user.id)
#    post = Post.objects.get(pk=pk)
#    category = post.category.all()
#    for cat in category:
#        if user in cat.subscribers.all():
#            cat.subscribers.remove(user)
#    return redirect('/news/')