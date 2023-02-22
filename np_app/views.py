from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.mail import send_mail, EmailMultiAlternatives

from .models import Post, Appointment, User, PostCategory
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


@login_required
def subscribe(request, pk):
    user = User.objects.get(pk=request.user.id)
    post = Post.objects.get(pk=pk)
    category = post.category.all()
    for cat in category:
        if user not in cat.subscribers.all():
            cat.subscribers.add(user)
    return redirect('/news/')


@login_required
def unsubscribe(request, pk):
    user = User.objects.get(pk=request.user.id)
    post = Post.objects.get(pk=pk)
    category = post.category.all()
    for cat in category:
        if user in cat.subscribers.all():
            cat.subscribers.remove(user)
    return redirect('/news/')


class AppointmentView(View):
    template_name = 'appointment_created.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'appointment_created.html', {})

    @receiver(m2m_changed, sender=PostCategory)
    def post(self, request, action, *args, **kwargs):
        appointment = Appointment(
        date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
        user_name=request.POST['user_name'],
        message=request.POST['message'],
        )
        appointment.save()
        if action == 'post_add':
            send_mail(
                subject=f'{appointment.user_name}',
                message=appointment.message,
                from_email='rudeigos1995@yandex.ru',
                recipient_list=['elizacat250795@gmail.com']
                )

            return redirect('appointments:make_appointment')


#@receiver(m2m_changed, sender=PostCategory)
#def post(request, instance, action, **kwargs):
#    if action == 'post_add':
#        send_mail(
#            subject=f'Здравствуй, {request.user}. Новая статья в твоем любимом разделе!',
#            message=f'{instance.text_post}',
#            from_email='rudeigos1995@yandex.ru',
#            recipient_list=['elizacat250795@gmail.com']
#        )