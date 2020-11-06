from django.http import HttpResponseRedirect

def user_login_required(view_func):
    def wrap(request, *args, **kwargs):
        if not request.session.get('user_login', True):
            return HttpResponseRedirect('/login/')
        return view_func(request, args, *kwargs)
    return wrap




