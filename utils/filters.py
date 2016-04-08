from django.shortcuts import render


def require_superuser(func):
    def check(request, *args, **kwargs):
        if request.user.is_superuser:
            return func(request, *args, **kwargs)

        return render(request, "403.html")

    return check