import os

import pandas as pd
from django.conf import settings
from django.contrib import messages, auth
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from Scraper.models import Product, Fb_credentails
from authentication.models import Profile


@login_required(login_url="Login")
def dashboard(request):
    # First try to get the profile by exact user match
    user_profile = Profile.objects.filter(owner=request.user).first()
    
    # If profile not found, try by email
    if not user_profile:
        user_profile = Profile.objects.filter(owner__email=request.user.email).first()
    
    # If still no profile, create one
    if not user_profile:
        user_profile = Profile.objects.create(owner=request.user)
    
    # Get products data
    product_data = Product.objects.filter(owner=request.user)
    
    # Get Facebook accounts
    fb_accounts = Fb_credentails.objects.filter(owner=request.user).order_by('account_number')
    
    # Create a list of 5 accounts (existing or empty placeholders)
    accounts_list = []
    for i in range(1, 6):
        account = fb_accounts.filter(account_number=i).first()
        if not account:
            account = Fb_credentails(owner=request.user, account_number=i)
        accounts_list.append(account)
    
    context = {
        "user_profile": user_profile, 
        "product_data": product_data,
        "fb_accounts": accounts_list
    }
    return render(request, "dashboard.html", context)


def add_product(request):
    users = User.objects.get(username=request.user)
    if request.method == "POST":
        myfile = request.FILES["myfile"]
        if (
            myfile.content_type
            == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ):
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            empexceldata = pd.read_excel(
                os.path.join(settings.BASE_DIR, "static", "media", filename)
            )
            dbframe = empexceldata
            for dbframe in dbframe.itertuples():

                obj = Product.objects.create(
                    owner=request.user,
                    title=dbframe.Title,
                    price=dbframe.Price,
                    location=dbframe.Locations,
                    desc=dbframe.Description,
                    tag1=dbframe.Tag1,
                    tag2=dbframe.Tag2,
                    tag3=dbframe.Tag3,
                    tag4=dbframe.Tag4,
                    tag5=dbframe.Tag5,
                )
                obj.save()
            messages.info(request, "File data successfully import.")
            return redirect("dashboard")
        else:
            messages.info(request, "Only excel type file is accpeted.")
            return redirect("dashboard")
    return redirect("dashboard")


@login_required(login_url="Login")
def Setting(request):
    users = User.objects.get(username=request.user)
    user_profile = Profile.objects.filter(owner=users).first()
    
    # If profile not found, create one
    if not user_profile:
        user_profile = Profile.objects.create(owner=users)
    
    context = {"user_profile": user_profile, "users": users}
    
    if request.method == "POST":
        fname = request.POST.get("firstname")
        lname = request.POST.get("lastname")
        email = request.POST.get("Email")
        phone = request.POST.get("phone")
        
        if len(fname) != 0:
            users.first_name = fname
        if len(lname) != 0:
            users.last_name = lname
        if len(email) != 0:
            users.email = email
        if phone:
            user_profile.phone = phone
            
        # Process image upload if present
        if len(request.FILES) != 0:
            my_file = request.FILES["upload"]
            if (
                my_file.content_type == "image/jpg"
                or my_file.content_type == "image/jpeg"
                or my_file.content_type == "image/png"
            ):
                user_profile.picture = request.FILES["upload"]
                users.save()
                user_profile.save()
                messages.success(request, "Data updated successfully")
                return redirect("Settings")
            messages.success(request, "Only JPG, PNG & JPEG image type is allowed")
            return redirect("Settings")
            
        # Save changes even without image upload
        users.save()
        user_profile.save()
        messages.success(request, "Data updated successfully")
        return redirect("Settings")

    return render(request, "settings.html", context)


@login_required(login_url="Login")
def setting_security(request):
    # Get user profile consistently
    user_profile = Profile.objects.filter(owner=request.user).first()
    
    # If profile not found, create one
    if not user_profile:
        user_profile = Profile.objects.create(owner=request.user)
    
    context = {"user_profile": user_profile}
    
    if request.method == "POST":
        new_password = request.POST.get("new_password")
        if len(new_password) != 0:
            request.user.set_password(new_password)
            request.user.save()
            user = auth.authenticate(
                username=request.user.username, password=new_password
            )
            if user is not None:
                login(request, user)
                messages.info(request, "Password updated successfully.")
                return redirect("dashboard")
        else:
            messages.error(request, "Please enter a new password")
            return redirect("settings-security")

    return render(request, "settings-security.html", context)


@login_required(login_url="Login")
def delete_product(request):
    if request.method == "POST":
        ids = request.POST.getlist("id[]")
        for id in ids:
            try:
                x = Product.objects.get(pk=id)
                x.delete()
            except:
                pass
        return JsonResponse("Product removed", safe=False)


@login_required(login_url="Login")
def add_image(request):
    if request.method == "POST":
        product_pk = request.POST.get("product_pk")
        product_data = Product.objects.get(pk=product_pk)
        if len(request.FILES) != 0:
            my_file = request.FILES["product_image"]
            if (
                my_file.content_type == "image/jpg"
                or my_file.content_type == "image/jpeg"
                or my_file.content_type == "image/png"
            ):
                product_data.image = request.FILES["product_image"]
                product_data.save()
                
                # If it's an AJAX request, return the image URL as JSON
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'message': 'Image uploaded successfully',
                        'image_url': product_data.image.url,
                        'product_id': product_data.id
                    })
                
                messages.success(request, "Image uploaded successfully")
                return redirect("dashboard")
            else:
                error_msg = "Invalid image type. Only JPG, JPEG OR PNG type accepted."
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'message': error_msg
                    })
                
                messages.error(request, error_msg)
                return redirect("dashboard")
        else:
            error_msg = "Select image first please"
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': error_msg
                })
            
            messages.error(request, error_msg)
            return redirect("dashboard")
    
    # If not POST request
    return redirect("dashboard")


@login_required(login_url="Login")
def upload_images(request):
    if request.method == "POST":
        if len(request.FILES) != 0:
            files = request.FILES.getlist("product_images")
            # Only get products for the current user, and limit to the number of files
            products = Product.objects.filter(owner=request.user).order_by('id')
            
            # Process only as many products as we have files for
            count = min(len(files), products.count())
            success_count = 0
            uploaded_images = []
            
            # Directly process each file and product pair
            for i in range(count):
                try:
                    file = files[i]
                    product = products[i]
                    
                    # Validate file type
                    if (file.content_type == "image/jpg" or 
                        file.content_type == "image/jpeg" or 
                        file.content_type == "image/png"):
                        product.image = file
                        product.save()
                        success_count += 1
                        
                        # Add image URL and product ID to response data
                        uploaded_images.append({
                            'product_id': product.id,
                            'image_url': product.image.url
                        })
                except Exception as e:
                    print(f"Error uploading image: {str(e)}")
                    pass
            
            # If AJAX request, return JSON response
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                if success_count > 0:
                    return JsonResponse({
                        'success': True,
                        'message': f"{success_count} image(s) uploaded successfully",
                        'uploaded_images': uploaded_images
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'message': "Failed to upload images"
                    })
            
            # If normal request, use messages and redirect
            if success_count > 0:
                messages.success(request, f"{success_count} image(s) uploaded successfully")
            else:
                messages.error(request, "Failed to upload images")
            return redirect("dashboard")
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': "Please select at least one image"
                })
            
            messages.error(request, "Select image first please")
            return redirect("dashboard")
    
    return redirect("dashboard")


@login_required(login_url="Login")
def facebook_accounts(request):
    # Get existing Facebook accounts for the user
    fb_accounts = Fb_credentails.objects.filter(owner=request.user).order_by('account_number')
    
    # Create a list of 5 accounts (existing or empty placeholders)
    accounts_list = []
    for i in range(1, 6):
        account = fb_accounts.filter(account_number=i).first()
        if not account:
            account = Fb_credentails(owner=request.user, account_number=i)
        accounts_list.append(account)
    
    context = {
        'fb_accounts': accounts_list,
    }
    return render(request, 'facebook_accounts.html', context)


@login_required(login_url="Login")
def save_fb_account(request):
    if request.method == "POST":
        account_number = int(request.POST.get('account_number', 1))
        username = request.POST.get('fb_username')
        password = request.POST.get('fb_password')
        account_name = request.POST.get('account_name', f'Account {account_number}')
        
        if not account_name.strip():
            account_name = f'Account {account_number}'
        
        # Get or create the Facebook account
        fb_account, created = Fb_credentails.objects.get_or_create(
            owner=request.user,
            account_number=account_number,
            defaults={
                'username': username,
                'password': password,
                'account_name': account_name
            }
        )
        
        # If it already exists, update the values
        if not created:
            fb_account.username = username
            fb_account.password = password
            fb_account.account_name = account_name
            fb_account.save()
        
        messages.success(request, f'Facebook Account #{account_number} saved successfully')
        return redirect('facebook_accounts')
    
    return redirect('facebook_accounts')


@login_required(login_url="Login")
def delete_fb_account(request, account_id):
    try:
        account = Fb_credentails.objects.get(id=account_id, owner=request.user)
        account_number = account.account_number
        account.delete()
        messages.success(request, f'Facebook Account #{account_number} deleted successfully')
    except Fb_credentails.DoesNotExist:
        messages.error(request, 'Account not found')
    
    return redirect('facebook_accounts')


@login_required(login_url="Login")
def fb_accounts(request):
    # This is the old function, now just redirects to the new facebook_accounts view
    return redirect('facebook_accounts')


@login_required(login_url="Login")
def publish_with_account(request, account_number):
    # Add loading state feedback
    messages.info(request, f'Starting upload process with Account #{account_number}. This may take a few minutes...')
    # Redirect to scraper view with account number
    return redirect('scraper_with_account', account_number=account_number)
