from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post,Comment
from .forms import PostForm
from django.db.models import Q

def home(request):
    print(request.META)
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'posts': posts})

@login_required
def profile_view(request):
    posts = Post.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'profile.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')  # Redirect to homepage after posting
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = PostForm(instance=post)

    return render(request, 'edit_post.html', {'form': form, 'post': post})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    
    if request.method == "POST":
        post.delete()
        return redirect('profile')

    return render(request, 'delete_post.html', {'post': post})
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)  # Unlike if already liked
    else:
        post.likes.add(request.user)  # Like if not liked
    return redirect('home')

@login_required
def comment_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        text = request.POST.get('comment')
        if text:
            Comment.objects.create(user=request.user, post=post, text=text)
    return redirect('home')

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    
    if request.method == "POST":
        new_text = request.POST.get("comment_text")
        if new_text:
            comment.text = new_text
            comment.save()
        return redirect('home')
    
    return redirect('home')
@login_required
def search_view(request):
    query = request.GET.get('q', '').strip()
    filter_user = request.GET.get('user', '').strip()
    filter_media = request.GET.get('media', '').strip()
    sort_by = request.GET.get('sort', 'newest')  

    user_results = []  
    post_results = Post.objects.all()

    if query:
        # Find users matching the query
        users = User.objects.filter(Q(username__icontains=query) | Q(email__icontains=query))
        
        for user in users:
            user_profile = getattr(user, "userprofile", None)
            profile_picture = user_profile.profile_picture.url if user_profile and user_profile.profile_picture else "/media/profile_images/default.jpg"
            posts = Post.objects.filter(user=user).order_by('-created_at')
            
            user_results.append({
                "user": user,
                "profile_picture": profile_picture,
                "posts": posts,
            })
        
        # Search for posts containing the query in content
        post_results = post_results.filter(text__icontains=query)

    # Apply user filter
    if filter_user:
        post_results = post_results.filter(user__username__icontains=filter_user)

    # Apply media type filter
    if filter_media == "with_images":
        post_results = post_results.exclude(image__isnull=True).exclude(image__exact='')
    elif filter_media == "without_images":
        post_results = post_results.filter(Q(image__isnull=True) | Q(image__exact=''))

    # Apply sorting (debugging date issue)
    if sort_by == "oldest":
        post_results = post_results.order_by("created_at")
    else:
        post_results = post_results.order_by("-created_at")

    return render(request, "search_results.html", {
        "query": query,
        "user_results": user_results,
        "post_results": post_results,
    })