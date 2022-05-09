from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .forms import CommentForm, PostForm
from .models import Post, User, Comment

class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 2
    
    
def postdetail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(active=True).order_by("-created_on")[0:5]
    new_comment = None
    
    posts = Post.objects.all()
    paginator = Paginator(posts, 2) # Show 2 blogs per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    post_comments = [] #list for post comments

    for p in posts:
        for comment in comments:
            if comment.post == post:
                post_comments.append(comment)
        break
    #number of comments for post
    num_of_comments = len(post_comments)

    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST or None)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    context = {
        'post':post,
        'comments':comments,
        'post_comments': post_comments,
        'num_of_comments' : num_of_comments,
        'comment_form':comment_form,
        'page_obj':page_obj,
        'new_comment':new_comment,
    }
    
    return render(request, 'post_detail.html', context)

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
        
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content"]
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False  
    
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    context_object_name = "post"
    success_url = "/"
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
def about(request):
    return render(request, "blog/about.html", {"title" : "About"})