from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from .models import Post,BlogComment
from django.contrib import messages  # Import the messages module

# Create your views here.
def blogHome(request):
    allposts = Post.objects.all()
    context={'allposts':allposts}
    return render(request,'blog/blogHome.html',context)
def blogPost(request, slug):
    post = get_object_or_404(Post, slug=slug)
    user = request.user

    # Retrieve top-level comments (parent=None) and replies (not parent=None)
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)

    # Create a dictionary mapping parent comment's `sno` to its replies
    reply_dict = {}
    for reply in replies:
        if reply.parent.sno not in reply_dict:
            reply_dict[reply.parent.sno] = [reply]
        else:
            reply_dict[reply.parent.sno].append(reply)

    context = {
        'post': post,
        'comments': comments,
        'replies': reply_dict,  # Make sure this is passed correctly
        'user': user
    }

    return render(request, 'blog/blogPost.html', context)

def postComment(request):
    if request.method == 'POST':
        post_id = request.POST.get('postId')
        comment_text = request.POST.get('comment')
        user = request.user
        commentId = request.POST.get('commentId')  # For reply to a comment

        # Fetch the post using post_id
        post = get_object_or_404(Post, id=post_id)
        post=Post.objects.get(id=post_id)

        if commentId:  # If commentId exists, it's a reply to an existing comment
            parent_comment = get_object_or_404(BlogComment, sno=commentId)  # Use sno instead of id
            comment = BlogComment(comment=comment_text, user=user, post=post, parent=parent_comment)
            messages.success(request, 'Reply posted successfully!')
        else:
            comment = BlogComment(comment=comment_text, user=user, post=post)
            messages.success(request, 'Comment posted successfully!')

        comment.save()

    # Redirect to the correct blog post
    return redirect('blogDetail', slug=post.slug)


    # return redirect(f'/blog/{post.slug}')

