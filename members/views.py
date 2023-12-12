from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django import forms
from .models import Member, Court, Resevation
from django.contrib.auth.hashers import make_password


def members(request):
    template = loader.get_template("all_members.html")

    minor_members = Member.objects.filter(age__lte=20)
    adult_members = Member.objects.filter(age__gt=20)
    context = {"adult_members": adult_members, "minor_members": minor_members}
    print(minor_members[0].firstname, adult_members)
    return HttpResponse(template.render(context))


def books(request):
    template = loader.get_template("all_book.html")

    book = Resevation.objects.all()
    context = {"book": book}
    return HttpResponse(template.render(context))


def details(request, id):
    member = Member.objects.get(id=id)
    template = loader.get_template("details.html")
    print(member.joined)
    context = {
        "member": member,
    }
    return HttpResponse(template.render(context, request))


def details_court(request, id):
    court = Court.objects.get(name=id)
    template = loader.get_template("details_court.html")
    context = {
        "court": court,
    }
    return HttpResponse(template.render(context, request))


class BookForm(forms.Form):
    # court = forms.ModelChoiceField(queryset=Court.objects.all())
    date = forms.DateTimeField(widget=forms.DateInput(attrs={"type": "date"}))


def book_court(request, id):
    if not request.user.is_authenticated:
        return redirect("/login")
    if request.method != "POST":
        post_form = BookForm()
        return render(
            request=request,
            template_name="book.html",
            context={
                "message": "Please enter booking info",
                "post_form": post_form,
                "court": id,
            },
        )
    post_form = BookForm(request.POST)
    if not post_form.is_valid():
        return render(
            request=request,
            template_name="book.html",
            context={
                "message": "invalid login credentials",
                "post_form": post_form,
                "court": id,
            },
        )
    date = post_form.cleaned_data["date"]
    court = Court.objects.filter(name=id)[0]
    user = Member.objects.filter(user=request.user)[0]
    print("flag", id, date, court, user)
    Resevation.objects.create(court=court, date=date, member=user)
    return redirect("/court/book")


def main(request):
    template = loader.get_template("main.html")
    return HttpResponse(template.render())


def testing(request):
    template = loader.get_template("template.html")
    context = {
        "fruits": ["Apple", "Banana", "Cherry"],
    }
    return HttpResponse(template.render(context, request))


class LoginForm(forms.Form):
    username = forms.CharField(max_length=32)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)


def login(request):
    if request.method != "POST":
        post_form = LoginForm()
        return render(
            request=request,
            template_name="login.html",
            context={
                "message": "Please enter login credentials",
                "post_form": post_form,
            },
        )
    post_form = LoginForm(request.POST)
    if not post_form.is_valid():
        return render(
            request=request,
            template_name="login.html",
            context={
                "message": "invalid login credentials",
                "post_form": post_form,
            },
        )
    username = post_form.cleaned_data["username"]
    password = post_form.cleaned_data["password"]
    user = auth.authenticate(username=username, password=password)
    print(username, (password))
    if user is not None:
        auth.login(request=request, user=user)
        return redirect("/")

    print(user)
    post_form = LoginForm(request.POST)
    return render(
        request=request,
        template_name="login.html",
        context={
            "message": "login failed",
            "post_form": post_form,
        },
    )


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=32)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    firstname = forms.CharField()
    lastname = forms.CharField()
    phone = forms.CharField()
    age = forms.IntegerField()


def register(request):
    if request.method != "POST":
        post_form = RegisterForm()
        return render(
            request=request,
            template_name="register.html",
            context={
                "message": "Please enter new user credentials",
                "post_form": post_form,
            },
        )

    post_form = RegisterForm(request.POST)
    if not post_form.is_valid():
        return render(
            request=request,
            template_name="register.html",
            context={
                "message": "invalid login credentials",
                "post_form": post_form,
            },
        )
    username = post_form.cleaned_data["username"]
    password = post_form.cleaned_data["password"]
    firstname = post_form.cleaned_data["firstname"]
    lastname = post_form.cleaned_data["lastname"]
    phone = post_form.cleaned_data["phone"]
    age = post_form.cleaned_data["age"]
    if User.objects.filter(username=username).exists():
        return render(
            request=request,
            template_name="register.html",
            context={
                "message": "user {} already exists".format(username),
                "post_form": post_form,
            },
        )
    user = User.objects.create_user(username=username, email=None, password=password)
    Member.objects.create(
        user=user, firstname=firstname, lastname=lastname, phone=phone, age=age
    )
    return redirect("/login")


def logout(request):
    auth.logout(request)
    return redirect("/")


class CourtAddForm(forms.Form):
    court_name = forms.CharField()
    ground_type = forms.ChoiceField(
        choices=[
            ("grass", "Grass"),
            ("harder", "Harder"),
            ("carpet", "Carpet"),
            ("mud", "Mud"),
        ],
        widget=forms.Select(),
    )


def add_court(request):
    if request.method != "POST":
        post_form = CourtAddForm()
        return render(
            request=request,
            template_name="add_court.html",
            context={
                "message": "Please enter new court data",
                "post_form": post_form,
            },
        )

    post_form = CourtAddForm(request.POST)
    # print(post_form)
    if not post_form.is_valid():
        return render(
            request=request,
            template_name="add_court.html",
            context={
                "message": "invalid form",
                "post_form": post_form,
            },
        )
    court_name = post_form.cleaned_data["court_name"]
    ground_type = post_form.cleaned_data["ground_type"]

    if Court.objects.filter(name=court_name).exists():
        return render(
            request=request,
            template_name="add_court.html",
            context={
                "message": "court '{}' already exists".format(court_name),
                "post_form": post_form,
            },
        )
    Court.objects.create(name=court_name, ground_type=ground_type)
    return redirect("/court")


def court(request):
    data = Court.objects.all()
    return render(request=request, template_name="court.html", context={"courts": data})
