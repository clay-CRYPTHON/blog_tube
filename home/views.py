from django.shortcuts import render
from admintion.views import global_info
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from blogs.views import blogs__ as blogs_, authors, ct
from blogs.models import Blog, Category
from home.models import AboutSection, AboutTeam, ContactForm, ContactSection, DayImages, Social
from users.models import CustomUser



week_period = timezone.now() - timedelta(days=7)
week_top_models = Blog.objects.filter(
        hitcounts__hit__created__gte=week_period
    ).annotate(
        counts=Count('hitcounts__hit')
    ).order_by('-counts')[:5]

month_period = timezone.now() - timedelta(days=30)
month_top_models = Blog.objects.filter(
        hitcounts__hit__created__gte=month_period
    ).annotate(
        counts=Count('hitcounts__hit')
    ).order_by('-counts')[::8]

# Create your views here.
def home(request):
    global_info(request)
    context = {
        'ct': ct,
        'authors':authors,
        'day_image': DayImages.objects.filter(is_active=True).first(),
        'main': blogs_.get(is_main=True),
        'top_blogs': blogs_.filter(top=True).all().order_by('-create_date')[::3],
        'recent_blog': blogs_.all().order_by('-create_date').first(),
        'recent_blogs': blogs_.all().order_by('-create_date')[1::4],
        'trending_blogs': blogs_.all().order_by('-hitcounts__hits')[::4],
        'social':Social.objects.all(),
        'week_top_models':week_top_models,
        'month_top_models':month_top_models,


    }
    return render(request,'home.html',context)

def about(request):
    global_info(request)
    context = {
        'ct': ct,
        'day_image': DayImages.objects.filter(is_active=True).first(),
        'social': Social.objects.all(),
        'about': AboutSection.objects.first(),
        'team': AboutTeam.objects.first(),
        'authors': authors,

    }
    return render(request,'about.html',context)

def contact(request):
    global_info(request)
    context = {
        'ct': ct,
        'day_image': DayImages.objects.filter(is_active=True).first(),
        'social':Social.objects.all(),
        'authors':authors,
        'sec': ContactSection.objects.first(),
    }
    if request.method == 'POST':
        post = request.POST
        full_name = post.get('full_name',False)
        email_or_phone = post.get('email_or_phone',False)
        message = post.get('message',False)
        if full_name and email_or_phone and message:
            c = ContactForm.objects.create(full_name=full_name,email_or_phone=email_or_phone,message=message)
            c.save()
            context['msg'] = "Murojaatingiz yuborildi"
            return render(request,'contact.html',context)
    return render(request,'contact.html',context)



def handler404(request, exception):
    global_info(request)
    return render(request, '404.html')