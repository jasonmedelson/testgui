from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from mainApp.models import Influencer, Events, Tags, List
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def index(request):
    username = None
    if request.user.is_authenticated:
        username = request.user
        userid = request.user.id
        all_influencers = Influencer.objects.filter(user = userid)
    else:
        all_influencers= []

    Handle=[]
    Name=[]
    Email=[]
    Twitch=[]
    Twitter=[]
    Youtube=[]
    Mixer=[]
    Country=[]
    Shirt=[]
    Edit=[]
    Last_Updated=[]
    Mailing_Address=[]
    Phone=[]
    tags=[]
    events=[]
    influencer=[]
    lists=[]
    if len(all_influencers):
        try:
            for number in range(len(all_influencers)):
                Handle.append(all_influencers[number].influencer_handle)
                Name.append(all_influencers[number].legal_name)
                Email.append(all_influencers[number].email)
                Phone.append(all_influencers[number].phone)
                Twitch.append(all_influencers[number].twitch)
                Twitter.append(all_influencers[number].twitter)
                Youtube.append(all_influencers[number].youtube)
                Mixer.append(all_influencers[number].mixer)
                Country.append(all_influencers[number].country)
                Shirt.append(all_influencers[number].shirt)
                influencer.append(all_influencers[number])
                timestamp = all_influencers[number].updated_at
                timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                Last_Updated.append(timestamp)
                Mailing_Address.append(all_influencers[number].mailing_address)
                hold = ""
                i_tags = all_influencers[number].tags.all()
                for item in i_tags:
                    hold += item.tag_name + ', '
                hold = hold[:-2]
                tags.append(hold)
                hold = ""
                e_tags = all_influencers[number].events.all()
                for item in e_tags:
                    hold += item.event_name + ', '
                hold = hold[:-2]
                events.append(hold)
                query = List.objects.filter(list_influencers__influencer_handle = all_influencers[number].influencer_handle)
                print('q',query)
                for item in query:
                    hold += item.list_name + ', '
                print('h',hold)
                hold = hold[:-2]
                lists.append(hold)
        except:
            Handle.append('Error')
            Name.append('Error')
            Email.append('Error')
            Twitch.append('Error')
            Twitter.append('Error')
            Youtube.append('Error')
            Mixer.append('Error')
            Country.append('Error')
            Shirt.append('Error')
            Last_Updated.append('Error')
            Mailing_Address.append('Error')
            Phone.append('Error')
            tags.append('Error')
            events.append('Error')
            influencer = 'Error'
            lists.append('Error')

    zipped = zip(
        Handle,
        Name,
        Email,
        Twitch,
        Twitter,
        Country,
        Shirt,
        influencer,
        Last_Updated,
        Mailing_Address,
        Phone,
        Youtube,
        Mixer,
        tags,
        events,
        lists,
        )

    return render(
        request,
        './index.html',
        context={'info':zipped}
    )
