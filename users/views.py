from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from users.models import CustomUser


def be_author(request):
    if request.user.is_authenticated and request.user.groups != "author":
        user = request.user
        user.is_staff = True
        user.is_author = True
        g = Group.objects.get(name="author")
        user.groups.add(g)
        user.save()

        return redirect('admin:index')
    else:
        return redirect('home')


def log_in(request):
    context = {}
    if request.method == 'POST':
        post = request.POST
        login1 = post.get('login', False)
        register = post.get('register', False)
        if login1:
            username = post.get('username', False)
            password = post.get('password', False)
            if username and CustomUser.objects.filter(username=username).exists() and password:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    context['err'] = 'Parol yoki username xato'
                    context['post'] = post
            else:
                context['err'] = 'Bunday foydalanuvchi mavjud emas'
                context['post'] = post
        else:
            context['err'] = 'Kirishda xatolik'

        if register:
            username = post.get('username', False)
            if not CustomUser.objects.filter(username=username).exists():
                pass1 = post.get('password', False)
                pass2 = post.get('password_again', False)
                first_name = post.get('first_name', False)
                last_name = post.get('last_name', False)
                email = post.get('email', False)
                if pass1 and pass2 and (pass1 == pass2):
                    if username and first_name and email and last_name:
                        r_user = CustomUser.objects.create(username=username, email=email, first_name=first_name,
                                                           last_name=last_name)
                        r_user.set_password(pass1)
                        r_user.save()
                        r_user = authenticate(request, username=username, password=pass1)
                        if r_user is not None:
                            login(request, r_user)
                            return redirect('home')

                    else:
                        context['err'] = "Ma'lumotlar to'liq kiritilmadi"
                        context['post'] = post
                else:
                    context['err1'] = 'Qayta kiritilgan parol xato'
                    context['post'] = post
            else:
                context['err'] = 'Bunday foydalanuvchi mavjud'
                context['post'] = post
        else:
            context['err'] = 'Kirishda xatolik'

    return render(request, 'login.html')
