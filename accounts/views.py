from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
import requests.utils
from .forms import RegistrationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Account
from carts.models import Cart,CartItem
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import requests

# verification email

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from carts.views import _cart_id

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Extracting cleaned data from the form
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            phone_number = form.cleaned_data["phone_number"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            username = email.split("@")[0]

            # Creating a new user
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
            )
            user.phone_number = phone_number
            user.save()
            # user Activation
            current_site ="http://127.0.0.1:8000"
            mail_subject = 'please activate your account'
            message = render_to_string('accounts/account_verification_email.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
                
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            
            # messages.success(request, 'we have send a verification link to your mail id')
            return redirect('/accounts/login/?command=verification&email='+email)  # Redirect to login page after successful registration
    else:
        form = RegistrationForm()

    context = {
        "form": form,
    }
    return render(request, "accounts/register.html", context)


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email,password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists :
                    cart_item = CartItem.objects.filter(cart=cart)
                    # getting the pproduct_variations
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    # get cart items from the user to access his product variations
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list =[]
                    id = []
                    for cart_item in cart_item:  # Iterate over each CartItem object
                        existing_variations = cart_item.variations.all()  # Access variations for the current CartItem
                        ex_var_list.append(list(existing_variations))
                        id.append(cart_item.id)

                    # product_variation =[1,2,3,4,6]
                    # ex_var_list=[4,6,3,5]

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            cart_item_id=id[index]
                            cart_item = CartItem.objects.get(id=cart_item_id)
                            cart_item.quantity += 1
                            cart_item.user = user
                            cart_item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)

                            for cart_item in cart_item:
                                cart_item.user = user
                                cart_item.save()
            except:
                pass
            auth.login(request,user)
            messages.success(request,'you are now logged in')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query

                # next/cart/checkout/
                params= dict(x.split('=')for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)

            except:
                return redirect("dashboard")
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request,'accounts/login.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request,'you are logged out')
    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None
        
    if user is not None and  default_token_generator.check_token(user, token):
        user.is_active =True
        user.save()
        messages.success(request,'congratz, your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'invalid activation link')
        return redirect('register')
    
    
    return HttpResponse('ok')


@login_required(login_url = 'login')        
def dashboard(request):
    return render(request, 'accounts/dashboard.html')


def forgotpassword(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password mail
            current_site = "http://127.0.0.1:8000"
            mail_subject = "Reset your Password"
            message = render_to_string(
                "accounts/reset_password_email.html",
                {
                    "user": user,
                    "domain": current_site,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )

            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(
                request, "Password reset email has been sent to your email address"
            )
            return redirect("login")
        else:
            messages.error(request, "Account does not exist")
            return redirect("forgotpassword")
    return render(request, "accounts/forgotpassword.html")


def resetpassword_validate(request,uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user =Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'please reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')
def resetpassword(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password == confirm_password:
            uid = request.session.get('uid')
            if uid:
                try:
                    user = Account.objects.get(pk=uid)
                    user.set_password(password)
                    user.save()
                    messages.success(request, 'Password reset successful')
                    # Clear the session data after password reset
                    del request.session['uid']
                    return redirect('login')  # Redirect to login page after successful password reset
                except Account.DoesNotExist:
                    messages.error(request, 'User does not exist')
                    return redirect('resetpassword')
            else:
                messages.error(request, 'Invalid reset link')
                return redirect('resetpassword')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('resetpassword')
    else:
        return render(request, 'accounts/resetpassword.html')


# def resetpassword_validate(request, uidb64, token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = Account._default_manager.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
#         user = None

#     if user is not None and  default_token_generator.check_token(user, token):
#         request.session['uid'] = uid
#         messages.success(request, 'please reset your password')
#         return redirect('resetpassword')
#     else:
#         messages.error(request, 'This link has been expired!' )
#         return redirect('login')
