from django.http import HttpResponseRedirect
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

# def user_login_required(view_func):
#     def wrap(request, *args, **kwargs):
#         user_login = request.session.get("user_login", False)
#         if user_login is True:
#             return HttpResponseRedirect('/')
#         else:
#             return HttpResponseRedirect('/login')
#     return wrap


def admin_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    Decorator for views that checks that the logged in user is an admin,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_admin,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

