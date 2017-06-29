
from __future__ import unicode_literals
import bcrypt
from django.shortcuts import render, redirect, HttpResponse, reverse
from .models import *
from django.contrib import messages
# messages.success(request, "Sucessful Registation")
# messages.error(request, "User is not in the Database")

# function to print error messages for registration to display on Registration page


def error_flash(request, errors):
    for error in errors:
        messages.error(request, error)


def index(request):
    # print inside the terminal to check anything happening here
    print 'Inside the the index method'
    return render(request, 'exam/index.html')

#
#  Creat new user  function
#


def create(request):
    print 'Inside the the CREATE method'
    if request.method == "POST":
        form_data = request.POST
        check = User.objects.validate(form_data)

        if check != []:
            error_flash(request, check)
            return redirect('/')
        # valid form data
        password = str(form_data['password'])  # convert password to string
        hashed_pw = bcrypt.hashpw(
            password, bcrypt.gensalt())  # hash the password

        user = User.objects.create(
            name=form_data['name'],
            username=form_data['alias'],
            email=form_data['email'],
            password=hashed_pw,
            dob=form_data['dob'],

        )  # saving feilds to the database including hashed password.

        request.session['user_id'] = user.id
        messages.success(request, "Sucessful Registration")
        return redirect('/')

#
#  login and validate function
#


def login(request):
    print "Inside the login method."

    if request.method == "POST":
        form_data = request.POST

        check = User.objects.validate_login(form_data)

        if check:
            print check
            error_flash(request, check)

            return redirect('/')

        User.objects.login(form_data)
        return redirect('/pokes')

    return redirect('/')

#
#  logout function
#


def logout(request):
    request.session.pop('user_id')  # pop the value in the session variable

    return redirect('/')  # send you back to the index page

#
#  ADD function
#


# def add(request):
#     print 'Inside the the ADD method'
#     if request.method == "POST":
#         form_data = request.POST

    #     check = ADD.objects.validate_login(
    #         form_data)  # calls vaidate method
    #
    #     if check != []:
    #         error_flash(request, check)
    #         return redirect('/')
    #
    #         ADD = User.objects.create(
    #             # name=form_data['name'],
    #             # username=form_data['username'],
    #             # email=form_data['email'],
    #             # password=hashed_pw
    #
    #         )  # saving feilds to the database including hashed password.
    # messages.success(request, "Sucessfully added record")
    # return render(request, 'exam/add.html')

#
#  Query results of the website
#


def pokes(request):
    if "user_id" in request.session:
        print '*' * 25
        print request.session['user_id']
        user_id = request.session['user_id']
        current_user = User.objects.get(id=user_id)

        print current_user.poked.all()

        poked_you = len(current_user.poke_by.all())
        pokes = len(current_user.poke_by.all())
        pokees = User.objects.exclude(id=user_id)
        poke_table = Poke.objects.filter()
        poke_history = len(Poke.poker.filter(poker_table=poker_table))

        # print '*' * 25
        # print poke_table
        # print '*' * 25

        print '*' * 25
        print poke_history
        print '*' * 25

        context = {
            "user": current_user,
            "pokees": pokees,
            "pokes": pokes,
            "poked_you": poked_you
            # "poker_history": poker_history
        }
    return render(request, 'exam/pokes.html', context)  # add context here


def get_current_user(request):
    user_id = request.session['user_id']
    return User.objects.get(id=user_id)


def poker(request, id):

    print '*' * 25
    print"inside the Poke method"
    print '*' * 25

    if request.method == "POST":
        user_id = request.session['user_id']
        current_user = User.objects.get(id=user_id)
        user = User.objects.get(id=id)
        poke = Poke.objects.create(poker=current_user,  pokee=user)

        return redirect('/pokes')
