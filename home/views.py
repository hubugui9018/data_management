from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.models import User

# @login_required()
# def index(request):
#     if request.user.username and request.session.get('usermame',None) != None:
#         username = request.session['usermame']
#         return render(request,'app/home.html',{'username':username})
#     else:
#         return render(request,'app/login.html',{})
#
# def gentella_html(request):
#     context = {}
#     load_template = request.path.split('/')[-1]
#     template = loader.get_template('app/' + load_template)
#     return HttpResponse(template.render(context, request))

# @csrf_protect
# def login_action(request):
#     username = request.POST.get('username')
#     password = request.POST.get('password')
#     if username!=None:
#         user = auth.authenticate(request,username=username,password=password)
#         if user is not None:
#             auth.login(request,user)
#             request.session['usermame']=''.join([user.first_name,user.last_name])
#         else:
#             return render(request,'app/login.html',{'message':'用户名和密码不正确'})
#         return redirect('/')
#     else:
#         return render(request, 'app/login.html', {})
@login_required
def index(request):
    if request.user.is_authenticated and request.session.get('username', None):
        username = request.session['username']
        return render(request, 'app/home.html', {'username': username})
    else:
        return render(request, 'app/login.html', {})


def gentella_html(request):
    context = {}
    load_template = request.path.split('/')[-1]
    template = loader.get_template('app/' + load_template)
    return HttpResponse(template.render(context, request))


@csrf_protect
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            # 自动创建或获取一个匿名用户
            user, created = User.objects.get_or_create(username='anonymous')
            if created:
                user.set_password('anonymous_password')
                user.is_active = True
                user.save()

            user = auth.authenticate(request, username='anonymous', password='anonymous_password')
            auth.login(request, user)
            request.session['username'] = 'anonymous'

            return redirect('index')
        else:
            return render(request, 'app/login.html', {'message': '请输入用户名和密码'})

    return render(request, 'app/login.html', {})

def logout(request):
    auth.logout(request)
    return redirect('/')

