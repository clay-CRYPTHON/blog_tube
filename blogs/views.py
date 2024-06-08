from django.shortcuts import get_object_or_404, redirect, render
from admintion.views import global_info
from blogs.forms import BlogForm
from blogs.models import Blog, Category, Comments, Tag
from home.models import DayImages, Social
from users.models import CustomUser
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from hitcount.views import HitCountDetailView

ct = Category.objects.all()
authors = CustomUser.objects.filter(is_author=True).all()
blogs__ = Blog.objects.filter(active=True, is_remove=False).all()


def blog_category(request, slug):
    blogs_ = blogs__.filter(category__slug=slug).all()
    paginator = Paginator(blogs_, 6)
    page_number = request.GET.get('page')
    blogs = paginator.get_page(page_number)
    context = {
        'c': Category.objects.get(slug=slug),
        'day_image': DayImages.objects.filter(is_active=True).first(),
        'blogs': blogs,
        'ct': ct,
        'authors': authors,
        'tags': Tag.objects.all(),
        'top_blogs': Blog.objects.filter(top=True).all().order_by('-create_date')[::5],
    }
    return render(request, 'blog_category.html', context)


def author(request, uuid):
    author = CustomUser.objects.get(uuid=uuid)
    blogs_ = blogs__.filter(user__uuid=uuid).all()
    paginator = Paginator(blogs_, 6)
    page_number = request.GET.get('page')
    blogs = paginator.get_page(page_number)
    context = {
        'author': author,
        'day_image': DayImages.objects.filter(is_active=True).first(),
        'blogs': blogs,
        'ct': ct,
        'authors': authors,
        'tags': Tag.objects.all(),
        'top_blogs': Blog.objects.filter(top=True).all().order_by('-create_date')[::5],
    }
    return render(request, 'author.html', context)


def blog_detail(request, slug):
    global_info(request)
    b = Blog.objects.get(slug=slug)
    b.views_num += 1
    b.save()
    context = {
        'b': b,
        'ct': ct,
        'day_image': DayImages.objects.filter(is_active=True).first(),
        'social': Social.objects.all(),
        'authors': authors,
        'tags': Tag.objects.all(),
        'blogs': Blog.objects.filter(category=b.category).exclude(slug=slug).all()[::5],
    }
    print(context['ct'])
    if request.method == "POST":
        comment = request.POST.get('comment', False)
        if comment:
            c = Comments.objects.create(blog=b, comment=comment, user=request.user)
            c.save()
            # request.session['stored_data'] = form.cleaned_data
            return render(request, 'blog_detail.html', context)
    return render(request, 'blog_detail.html', context)


# except:
#     return redirect('home')

class BlogDetailView(HitCountDetailView):
    model = Blog
    count_hit = True
    template_name = 'blog_detail.html'
    context_object_name = 'b'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Boshqa kontekst ma'lumotlarini qo'shishingiz mumkin
        context['day_image'] = DayImages.objects.filter(is_active=True).first()
        context['social'] = Social.objects.all()
        context['authors'] = authors  # Buni o'zgartiring, agar bu yerda o'zgaruvchi mavjud bo'lmasa
        context['tags'] = Tag.objects.all()
        context['ct'] = ct
        context['authors'] = authors
        context['blogs'] = Blog.objects.filter(category=context['b'].category).exclude(slug=context['b'].slug).all()[
                           ::5]
        return context

    def post(self, request, *args, **kwargs):
        # POST so'rovi keldi, shuning uchun foydalanuvchi izoh qoldirgan
        b = self.get_object()
        comment = request.POST.get('comment', False)

        if comment:
            c = Comments.objects.create(blog=b, comment=comment, user=request.user)
            c.save()

        return self.get(request, *args, **kwargs)


def blogs(request):
    global_info(request)
    blogs_ = blogs__
    paginator = Paginator(blogs_, 6)
    page_number = request.GET.get('page')
    blogs = paginator.get_page(page_number)
    context = {
        'ct': ct,
        'day_image': DayImages.objects.filter(is_active=True).first(),
        'social': Social.objects.all(),
        'authors': authors,
        'blogs': blogs,
        'tags': Tag.objects.all(),
        'top_blogs': Blog.objects.filter(top=True).all().order_by('-create_date')[::5],
    }
    return render(request, 'blogs.html', context)


def search(request):
    global_info(request)
    search = request.GET.get('search')
    blogs_ = blogs__.filter(
        Q(category__name__icontains=search) | Q(title__icontains=search) | Q(sub_title__icontains=search) | Q(
            content__icontains=search) | Q(slug__icontains=search) | Q(user__username__icontains=search) | Q(
            user__first_name__icontains=search) | Q(user__last_name__icontains=search) | Q(
            hash_tags__icontains=search)).all()
    paginator = Paginator(blogs_, 6)
    page_number = request.GET.get('page')
    blogs = paginator.get_page(page_number)
    context = {
        'ct': ct,
        'day_image': DayImages.objects.filter(is_active=True).first(),
        'social': Social.objects.all(),
        'authors': authors,
        'blogs': blogs,
        'tags': Tag.objects.all(),
        'top_blogs': Blog.objects.filter(top=True).all().order_by('-create_date')[::5],
        'search': search
    }

    return render(request, 'blogs.html', context)


@login_required
def add_post(request):
    global_info(request)
    context = {
        'ct': ct,
        'day_image': DayImages.objects.filter(is_active=True).first(),
        'social': Social.objects.all(),
        'authors': authors,
    }
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            return redirect('blog_detail', slug=blog.slug)
    else:
        form = BlogForm()
    context['form'] = form
    return render(request, 'add_post.html', context)


def edit_blog(request, slug):
    global_info(request)
    blog = get_object_or_404(Blog, slug=slug)
    if blog.user == request.user:
        if request.method == 'POST':
            form = BlogForm(request.POST, instance=blog)
            if form.is_valid():
                form.save()
                return redirect('blog_detail',
                                slug=blog.slug)  # Replace 'blog_detail' with your actual view name for displaying blog details
        else:
            form = BlogForm(instance=blog)

        return render(request, 'add_post.html', {'blog': blog, 'form': form})
    else:
        return redirect('home')


def remove_blog(request, slug):
    global_info(request)
    blog = get_object_or_404(Blog, slug=slug)
    if blog.user == request.user:
        blog.is_remove = True
        blog.save()
        return redirect('blogs')
    else:
        return redirect('home')