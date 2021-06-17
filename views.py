from django.shortcuts import render


from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from .models import Post
from django.views.generic import DetailView, CreateView, DeleteView, DeleteView
from .forms import RegisterationForm, LoginForm, PostForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from django.urls import reverse_lazy, reverse
from django.db.models import Q 

# Create your views here.
def post_list(request):
    posts = Post.published.all()
    return render(request,'post/list.html', {'posts': posts})

class DetailArticleView(DetailView):
    model= Post
    template_name='post/detail.html'

    def get_context_data(self, *args, **kwargs):
        context=super(DetailArticleView, self).get_context_data(**kwargs)
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = post.total_likes()

        liked=False
        if post.likes.filter(id=self.request.user.id).exists():
            liked=True

        context["total_likes"]= total_likes 
        context["liked"] = liked
        return context
# def post_detail(request, pk):
#     post= get_object_or_404(Post, pk=id)
#     return render(request, 'post/detail.html', {'post': post})


def LikeView(request, pk):
    post = get_object_or_404(Post, id = request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked=False
    else:
        post.likes.add(request.user)
        liked= True
    return HttpResponseRedirect(reverse('blog:post_detail', args=[str(pk)]))


class Add_Post(CreateView):
    model = Post
    form_class= PostForm
    template_name='user/post.html'
    # fields='__all__'

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return HttpResponseRedirect('/')
        else:
            return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render   (request, 'user/login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = RegisterationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
        return HttpResponseRedirect('/login')
    else:
        form =RegisterationForm()
    return render(request, 'user/signup.html', {'form': form})

class Delete(DeleteView):
    model = Post
    template_name='user/delete.html'
    
    def get_success_url(self) :
        return reverse('blog:post_list')

def search(request):
    search_post = request.GET.get('search')
    if search_post:
        post = Post.objects.filter(Q(title__icontains=search_post) & Q(content__icontains=search_post))
    else:
        # If not searched, return default posts
        post = Post.objects.all()
    return render(request, 'post/list.html', {'post':post})

