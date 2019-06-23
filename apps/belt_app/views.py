from django.shortcuts import render, redirect
from .models import User, Trips
import bcrypt
from django.contrib import messages


def index(request):
    return render(request, 'belt_app/page1.html')

#Register
def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        print(errors.items())
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ('/') #NO INDENTATION GDI
    else:
        password = request.POST['password']
        confirm_pw = request.POST['confirm_password']
        hashed_pw = bcrypt.hashpw(confirm_pw.encode(), bcrypt.gensalt())
        if bcrypt.checkpw(password.encode(), hashed_pw):
            new_user = User.objects.create(first_name=request.POST['fname'], last_name=request.POST['lname'], email=request.POST['email'], password=hashed_pw)
            request.session['user_id'] = new_user.id #Puts this person in session and it remembers them 
            return redirect('/dashboard')
        else:
            return redirect('/')

#Login
def login(request):
    errors = User.objects.log_validator(request.POST)
    if len(errors) > 0:
        print(errors.items())
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ('/') #NO INDENTATION GDI
    else:
        # get the post from the log form
        email = request.POST['email']
        password = request.POST['password']

        # set user to matching email is in database
        if User.objects.filter(email = email):
            user = User.objects.get(email = email)
            if bcrypt.checkpw(password.encode(), user.password.encode()): #first perameter is the clients password input 
                request.session['user_id'] = user.id #Puts this person in session and it remembers the id of this person
                return redirect('/dashboard')
            else:
                return redirect('/')
        else:
            return redirect('/')

#Success
def success(request):
    if not "user_id" in request.session:
        return redirect('/')

    context = {
        'user' : User.objects.get(id = request.session["user_id"]),
        'trips' : User.objects.get(id = request.session["user_id"]).trips.all().order_by("-id"),
        # 'trip' : Trips.objects.get(),
        'trip_without_user' : Trips.objects.all().exclude(user=request.session['user_id']),
      }
    # when you need to reference something  from a database in the rendered page, add context
    return render(request, 'belt_app/page2.html', context)

#page3 
def create(request):
    context = {
        'user' : User.objects.get(id = request.session['user_id'])
    }
    return render(request, 'belt_app/page3.html', context)

def make(request):
    errors = Trips.objects.create_validator(request.POST)
    if len(errors) > 0:
        print(errors.items())
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ('/trips/new') #NO INDENTATION GDI
    else:
        user = User.objects.get(id = request.session['user_id'])
        user_id= user.id
        User.objects.get(id=user_id).trips.create(destination = request.POST['destination'], start_date = request.POST['start_date'] , end_date= request.POST['end_date'], plan= request.POST['plan'])
        # request.session['trips_id'] = User.objects.get(id=user_id).trips.create(destination = request.POST['destination'], start_date = request.POST['start_date'] , end_date= request.POST['end_date'], plan= request.POST['plan']).id #Puts this person in session and it remembers them 
        return redirect('/dashboard')

def delete(request, one_trip_id):
    destroy = Trips.objects.get(id=one_trip_id)
    destroy.delete()
    return redirect('/dashboard')

def edit(request, one_trip_id):
    # int_id = int(one_trip_id)
    # print(type(int_id))
    
    context = {
        'user' : User.objects.get(id = request.session['user_id']),
        'trip_id' : one_trip_id,
        'trips' : Trips.objects.get(id=one_trip_id)
        # 'start_date' : Trips.objects.get(id = int_id).start_date
    }
    # print(type('start_date'))
    return render(request, 'belt_app/page4.html', context)


def update(request, trip_id):
    errors = Trips.objects.create_validator(request.POST)
    if len(errors) > 0:
        print(errors.items())
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ('/trips/edit/' + str(trip_id)) #NO INDENTATION GDI
    else:
        update=Trips.objects.get(id=trip_id)
        update.destination = request.POST['destination']
        update.start_date = request.POST['start_date']
        update.end_date = request.POST['end_date']
        update.plan = request.POST['plan']
        update.save()
        return redirect('/dashboard')

def read(request, one_trip_id):
    context = {
        'user' : User.objects.get(id = request.session['user_id']),
        'trip_id' : one_trip_id,
        'trip' : Trips.objects.filter(id = one_trip_id),
    }
    return render(request,'belt_app/page5.html', context)