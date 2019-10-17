from django.http import Http404
from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text

from dapricot.blog.tokens import account_activation_token
from dapricot.blog.models import Post, Category, Tag, Comment, Commenter
from dapricot.blog.forms import CommentCommenterForm

def sendMail(request, commenter):
    subject = 'Verificar correo'
    current_site = get_current_site(request)
    message = render_to_string('dapricot/emails/account_activation_email.html',
                {
                    'user': commenter.nickname,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(commenter.pk)),
                    'token': account_activation_token.make_token(commenter),
                })
    
    if settings.EMAIL_HOST_USER:
        send_mail(subject, message,
                  settings.EMAIL_HOST_USER,
                  [commenter.email])
        
    else:
        send_mail(subject, message, None, [commenter.email])

def post(request, day, month, year, slug, demo=0):
    if demo is 1:
        post = Post.objects.get(last_edition_date__year=year,
                    last_edition_date__month=month,
                    last_edition_date__day=day,
                    slug=slug)
        
    else:
        post = Post.objects.get(publication_date__year=year,
                    publication_date__month=month,
                    publication_date__day=day,
                    slug=slug)

    comments = Comment.objects.filter(post=post)
    
    if (post.author==request.user and post.status=='d') or post.status=='p':
        if request.method == "POST":
            form = CommentCommenterForm(request.POST)
            
            if form.is_valid():
                commenter, created = form.get_or_create_comment_commenter(post)
                
                if created:
                    commenter.save()
                    sendMail(request, commenter)
                    form = CommentCommenterForm()
                
        else:
            form = CommentCommenterForm()
            
        return render(request, 'dapricot/blog/post.html', {
            'post': post,
            'comments': comments,
            'form': form
            })
    
    raise Http404("Post does not exist")

def filterList(request, filter_name):
    filter_list = None
    if filter_name=='category':
        filter_list = Category.objects.all()

    elif filter_name=='tag':
        filter_list = Tag.objects.all()

    elif filter_name=='author':
        #TODO
        filter_list = None

    if filter_list and filter_list.count()>0:
        return render(request, 'dapricot/blog/filter_list.html', {
            'filter_list':filter_list,
            'filter_name': filter_name
        })
    
    raise Http404("Poll does not exist")

def datePostList(request, year, month=None, day=None, page=1):

    data = {'date': [year, month, day, page]}

    template = 'dapricot/blog/post_list.html'

    return render(request, template, data)

def postList(request, filter_name=None, value=None, page=1):
    template = 'dapricot/blog/main_site.html'
    filter_value = None
        
    if filter_name:
        template = 'dapricot/blog/post_list.html'
        
        if filter_name=='category':
            filter_value = Category.objects.filter(slug=value).last()
    
        elif filter_name=='tag':
            filter_value = Tag.objects.filter(slug=value).last()
        
    data = {'filter': [filter_name, filter_value]}

    return render(request, template, data)
    
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        commenter = Commenter.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Commenter.DoesNotExist):
        commenter = None

    if (commenter is not None and
        account_activation_token.check_token(commenter, token)):
        commenter.status = 'v'
        commenter.save()
        Comment.objects.filter(author=commenter).update(status='a')
        
        return render(request, 'account_activation_valid.html')
    else:
        return render(request, 'account_activation_invalid.html')
    
    raise Http404("Poll does not exist")
