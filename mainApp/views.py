from django.shortcuts import render, redirect, get_object_or_404 #redering html pages to display or pointing to other view
from django.http import HttpResponse, HttpResponseRedirect # pure http HttpResponse
from mainApp.models import Influencer, Events, Tags, List # Custom models
from django.contrib.auth import login, authenticate #for login, registration view
from django.contrib.auth.forms import UserCreationForm #Django Forms
from .forms import InfluencerCreateForm, TagFormCSV, EventFormCSV, TagForm, EventForm, ListCreateForm, InfluencerCSVForm #custom forms
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required #login_required view decorator
from django.views.generic.edit import CreateView, DeleteView, UpdateView #Django Class based generic views
from django.utils.html import strip_tags #strip html from user input


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

# create a new Influencer instance
@login_required
def InfluencerCreate(request):
    if request.method == 'POST':
        form = InfluencerCreateForm( request.user, request.POST, )
        if form.is_valid():
            influencer = form.save(commit=False)
            influencer.user = request.user
            influencer.save()
            return redirect('index')
    else:
        form = InfluencerCreateForm(request.user)
    return render(request, 'mainApp/influencer_form.html', {'form': form})

# edit an Influencer instance
@login_required
def InfluencerUpdate(request, pk):
    object = Influencer.objects.get(id = pk)
    if request.method == 'POST':
        form = InfluencerCreateForm( request.user, request.POST, instance = object, )
        if form.is_valid():
            influencer = form.save(commit=True)
            return redirect('index')
    else:
        form = InfluencerCreateForm(request.user, instance = object, )
    edit = form['influencer_handle'].value()
    print('e',edit)
    context = {
        'form':form,
        'edit':edit,
        'pk':pk
    }
    return render(request, 'mainApp/influencer_form.html', context)

# Delete Influencer instance
class InfluencerDelete(DeleteView):
    template_name = 'delete.html'
    model = Influencer
    success_url = reverse_lazy('index')

#Create multiple influencer instances from csv data
@login_required
def InfluencerCreateCSV(request):
    if request.method == 'POST':
        form = InfluencerCSVForm(request.POST)
        if form.is_valid():
            username = request.user
            # userid = request.user.id
            fields = form['seperate_fields_with_commas'].value()
            print('fields', fields)
            stripped_fields = strip_tags(fields).strip()
            print('stripped_fields',stripped_fields)
            field_array = stripped_fields.split(",")
            field_array = list(map(str.strip, field_array))
            print('field_array',field_array)
            data = form['paste_CSV']
            stripped_data = strip_tags(data).strip()
            data_array = stripped_data.split(",")
            print('data_array',data_array)
            passed = []
            failed = []
            test_against = ['influencer_handle','legal_name','email','phone','twitter','youtube','twitch','mixer','shirt','country']
            for element in field_array:
                if element in test_against:
                    passed.append(element)
                    print(element, "Is a field catagory!!!!!!!!!")
                else:
                    print(element, "Is not a field catagory")
            for element in test_against:
                if element not in field_array:
                    failed.append(element)
                    print(element, "Field is not being populated")
            print('passed', passed)
            print('failed', failed)
            Handle=[]
            Name=[]
            Email=[]
            Twitch=[]
            Twitter=[]
            Youtube=[]
            Mixer=[]
            Country=[]
            Shirt=[]
            Phone=[]
            pointer = 0
            for item in data_array:
                print('passed item', item)
                catagory = passed[pointer]
                if catagory == 'influencer_handle':
                    Handle.append(item)
                elif catagory == 'legal_name':
                    Name.append(item)
                elif catagory == 'email':
                    Email.append(item)
                elif catagory == 'phone':
                    Phone.append(item)
                elif catagory == 'twitter':
                    Twitter.append(item)
                elif catagory == 'youtube':
                    Youtube.append(item)
                elif catagory == 'twitch':
                    Twitch.append(item)
                elif catagory == 'mixer':
                    Mixer.append(item)
                elif catagory == 'shirt':
                    Shirt.append(item)
                elif catagory == 'country':
                    Country.append(item)
                pointer += 1
                print('p',pointer)
                if pointer >= len(passed):
                    pointer -= len(passed)
            for item in range(len(Handle)):
                print('Failed item', item)
                if 'influencer_handle' in failed:
                    Handle.append("")
                if 'legal_name' in failed:
                    Name.append("")
                if 'email' in failed:
                    Email.append("")
                if 'phone' in failed:
                    Phone.append("")
                if 'twitter' in failed:
                    Twitter.append("")
                if 'youtube' in failed:
                    Youtube.append("")
                if 'twitch' in failed:
                    Twitch.append("")
                if 'mixer' in failed:
                    Mixer.append("")
                if 'shirt' in failed:
                    Shirt.append("")
                if 'country' in failed:
                    Country.append("")
            print('Handle',Handle, len(Handle))
            print('Email',Email, len(Email))
            for item in range(len(Handle)):
                print('item no #', item)
                try:
                    new_influencer = Influencer(user=username, influencer_handle=Handle[item], legal_name=Name[item], email=Email[item], phone=Phone[item], twitter=Twitter[item], youtube=Youtube[item],twitch=Twitch[item],mixer=Mixer[item],shirt=Shirt[item],country=Country[item])
                    new_influencer.save()
                except Exception as inst:
                    print("Failed to create influencer: ",Handle[item])
                    print(type(inst))
                    print(inst.args)
                    print(inst)
            return redirect('index')
    form = InfluencerCSVForm()
    return render(request, 'mainApp/influencer_csv_form.html', {'form':form})
