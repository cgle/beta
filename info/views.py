# Create your views here.
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from info.forms import *
from info.models import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required


def home(request):
    variables = {
        'head_title':'Koinbox | An app by Gosuninjas',
        'page_title':'Welcome to Koinbox | An app by Gosuninjas',
        'page_body':'KOINBOX (C) 2012 GosuNinjas. All rights reserved.',
        'user':request.user
    }
    return render_to_response('home.html',variables)

def about(request):
    variables = {'user':request.user}
    return render_to_response('about.html',variables)

def user_page(request,username):
    try:
        user_info = User.objects.get(username=username)
        user = request.user
    except:
        raise Http404('Requested user not found')
    user_interest = user_info.interest_set.all()
    template = get_template('user_page.html')
    variables = Context({
        'user':request.user,
        'user_info':user_info,
        'username':username,
        'interests':user_interest,
        'show_edit': username == request.user.username,
    })
    output = template.render(variables)
    return HttpResponse(output)


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

def register_page(request):
    if request.method=='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )

            user.save()
            userprofile = UserProfile(
                user=user,
                name=form.cleaned_data['name'],
                age=form.cleaned_data['age'],
                university=form.cleaned_data['university'],
                home_city=form.cleaned_data['home_city'],
                away_city=form.cleaned_data['away_city']
            )
            userprofile.save()
            return HttpResponseRedirect('/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
        'form': form
    })
    return render_to_response('registration/register.html',variables)

@login_required
def edit_profile(request):

    if request.method=='POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            profile = request.user.get_profile()
            profile.name=form.cleaned_data['name']
            profile.age=form.cleaned_data['age']
            profile.university=form.cleaned_data['university']
            profile.home_city=form.cleaned_data['home_city']
            profile.away_city=form.cleaned_data['away_city']
            profile.save()
            return HttpResponseRedirect('/user/%s' %request.user.username)

    elif request.method=='GET':
        profile = request.user.get_profile()
        form = EditProfileForm(
            {
                'name':profile.name,
                'age':profile.age,
                'university':profile.university,
                'home_city':profile.home_city,
                'away_city':profile.away_city
            }
        )
    else:
        form = EditProfileForm()
    variables = RequestContext(request, {
        'user':request.user,
        'form': form
    })
    return render_to_response('edit_profile.html', variables)



@login_required
def interest_save_page(request):
    if request.method=='POST':
        form = InterestSaveForm(request.POST)
        if form.is_valid():
            interest=_save_interest(request,form)
            return HttpResponseRedirect(
                '/user/%s/' % request.user.username
            )
    elif request.GET.has_key('description'):
        description = request.GET['description']
        type_interest = request.GET['type_interest']
        tags = ''
        try:
            interest = Interest.objects.get(
                user=request.user,
                type_interest=type_interest,
                description=description
            )
            tags = ' '.join(
                tag.name for tag in interest.interest_tag_set.all()
            )
        except ObjectDoesNotExist:
            pass
        form = InterestSaveForm({
            'type_interest':type_interest,
            'description': description,
            'tags': tags
        })
    else:
        form = InterestSaveForm()
    variables = RequestContext(request, {
                'form': form
        })
    return render_to_response('interest_save.html', variables)

def _save_interest(request,form):
    interest, created = Interest.objects.get_or_create(
        user=request.user,
        type_interest=form.cleaned_data['type_interest'],
        description = form.cleaned_data['description']
    )


    if not created:
        interest.interest_tag_set.clear()

    tag_names = form.cleaned_data['tags'].split()
    for tag_name in tag_names:
        tag, dummy = Interest_Tag.objects.get_or_create(name=tag_name)
        interest.interest_tag_set.add(tag)

    interest.save()
    return interest

def delete_interest(request):
    if request.method=='GET':
        interest=Interest.objects.get(user=request.user,description=request.GET['description'],type_interest = request.GET['type_interest'])
        interest.delete()
    return HttpResponseRedirect(
        '/user/%s/' % request.user.username)

def koinbox(request):
    user_list=User.objects.all()
    user_list=list(user_list)
    final_list=[]
    user_list.remove(request.user)
    for user in user_list:
        count=0.0
        my_destination=request.user.get_profile().away_city
        their_location=user.get_profile().home_city
        if my_destination.lower()==their_location.lower():
            my_interest=list(request.user.interest_set.all())
            their_interest=list(user.interest_set.all())

            for item in my_interest:
                for item1 in their_interest:
                    if item.description.lower()==item1.description.lower():
                        their_interest.remove(item1)
                        count+=1.0

        if count/(len(request.user.interest_set.all())+0.0000001)>0.8:
            final_list.append(user)
    variables = Context({
        'user':request.user,
        'final_list':final_list,

    })
    template=get_template('koinbox.html')
    output=template.render(variables)
    return HttpResponse(output)


