# -*- coding: utf-8 -*-

import logging

from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

from keymanager.settings import PAGE_SIZE

from .forms import LoginForm
from .forms import UserCreateForm, UserEditForm
from utils.filters import require_superuser


LOG = logging.getLogger(__name__)


def require_superuser_or_self(func):
    def check(request, user_id):
        if request.user.is_superuser or \
                        user_id.encode("utf-8") == str(request.user.id):
            return func(request, user_id)

        return render(request, "403.html")
    return check


@require_superuser
def index(request):
    template_name = "users/index.html"
    msg = ""

    try:
        users = User.objects.exclude(id=request.user.id)
    except:
        msg = _("Unable to list users.")
        LOG.error(msg)
        users = []

    paginator = Paginator(users, PAGE_SIZE)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, template_name, {"users": users, "message": msg})


@require_superuser
def create(request):
    template_name = "users/create_user.html"
    msg = ""
    user_form = UserCreateForm()

    if request.method == "POST":
        user_form = UserCreateForm(request.POST)
        if user_form.is_valid():
            try:
                new_user = User.objects.create_user(
                    request.POST['username'],
                    request.POST['email'],
                    request.POST['password'])
                new_user.save()
                msg = _('Success create user "%s"') % \
                      user_form.cleaned_data['username'].encode("utf-8")
                LOG.info(msg)
            except IntegrityError:
                msg = _("User already exist, please try another username.")
                LOG.error(msg)
            except:
                msg = _('Unable to create user "%s"') % \
                      user_form.cleaned_data['username'].encode("utf-8")
                LOG.error(msg)

    return render(request, template_name, {"user_form": user_form,
                                           "message": msg})


@require_superuser
def delete(request, user_id):
    try:
        User.objects.get(id=user_id).delete()
    except Exception:
        msg = _("Unable to delete user(%s)") % user_id
        LOG.error(msg)

    if user_id == request.user.id:
        logout(request)

    return redirect(reverse('users:index'))


@require_superuser
def deactivate(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_active = False
        user.save()
    except:
        msg = _("Unable to deactivate user(%s)") % user_id
        LOG.error(msg)

    if user_id == request.user.id:
        logout(request)

    return redirect(reverse('users:index'))


@require_superuser
def activate(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_active = True
        user.save()
    except:
        msg = _("Unable to activate user(%s)") % user_id
        LOG.error(msg)

    if user_id == request.user.id:
        logout(request)

    return redirect(reverse('users:index'))


@require_superuser_or_self
def edit(request, user_id):
    template_name = "users/update_user.html"
    msg = ""
    user = User.objects.get(id=user_id)
    user_form = UserEditForm(initial={"username": user.username,
                                      "email": user.email})

    if request.method == "POST":
        user_form = UserEditForm(request.POST)
        if user_form.is_valid():
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            if username:
                user.username = username
            if email:
                user.email = email
            if password:
                user.set_password(password)
            user.save()
            msg = _('Success updated user "%s"') % username.encode("utf-8")
            LOG.info(msg)
    return render(request, template_name, {"user_id": user_id,
                                           "user_form": user_form,
                                           "message": msg})


def login(request):
    template_name = 'auth/login.html'
    msg = ""
    if request.user.is_authenticated():
        return redirect(reverse("keys:index"))

    form = LoginForm

    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    django_login(request, user)
                    msg = _("%s logged in successfully.") % \
                          username.encode('utf-8')
                    LOG.info(msg)
                    return redirect(reverse('keys:index'))
            msg = _("Invalid username or password.")
            LOG.error(msg)

    return render(request, template_name, {"user_form": form,
                                           "message": msg})


def logout(request):
    django_logout(request)
    return redirect(reverse("index"))