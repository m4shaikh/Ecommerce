from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from functools import wraps

def seller_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        # Check user_type directly from CustomUser model
        if not hasattr(request.user, 'user_type') or request.user.user_type != 'seller':
            return HttpResponseForbidden(
                "You must be a registered seller to access this page. "
                "Please contact support if you need seller privileges."
            )
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view