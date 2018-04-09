from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Create your views here.
from testyourbrain.forms import UserForm,NewSession
from testyourbrain.models import GameSession, UserProfile, UserMethods


def index(request):
    if request.user.is_authenticated==False:
        return render(request, 'testyourbrain/login.html', {})
    else:
        sesh_list=GameSession.objects.all()
        return render (request, 'testyourbrain/index.html', {'sessions':sesh_list})


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)


        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            UserProfile.objects.create(user=user)
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render(request,
                  'testyourbrain/register.html',
                  {'form': user_form,

                   'registered': registered})


def user_login(request):
    invalid_login = False
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account is disabled")
        else:  # invalid login details
            invalid_login = True
            return render(request, 'testyourbrain/login.html', {'invalid_login': invalid_login, 'nbar': "login"})
    else:
        return render(request, 'testyourbrain/login.html', {'invalid_login': invalid_login, 'nbar': "login"})

@login_required
def user_logout(request):
    user=UserProfile.objects.get(user=request.user)
    auth_list=GameSession.objects.filter().values_list('author')
    try:
        user_sesh=GameSession.objects.get(author=request.user)
        try:
            user_sesh.author=UserProfile.objects.filter(session=user_sesh)[0]
        except:
            user_sesh.delete()
    except:
        pass
    finally:
        user.session=None
        user.save()
        logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def session(request,id):
    session = GameSession.objects.get(id=id)
    players = [session.author,]
    user=User.objects.get(username=request.user.username)
    user.session=session
    if user!=session.author:
        players.append(user)


    return  render(request, 'testyourbrain/session.html',{'players':players})

@login_required
def profile(request,username):
    user=User.objects.get(username=username)
    return render(request, 'testyourbrain/profile.html', {})


#@user_passes_test(UserMethods.no_game)
@login_required
def add_game(request):
    user=UserProfile.objects.get(user=request.user)
    if user.session:
        return session(request,user.session.id)
    if request.method=='POST':
        game_form=NewSession(data=request.POST)
        game=game_form.save(commit=False)
        game.author=request.user
        game.save()
        user.session=game

        return session(request,game.id)
    else:
        game_form=NewSession()
    return render(request, 'testyourbrain/add_game.html', {'game_form':game_form})