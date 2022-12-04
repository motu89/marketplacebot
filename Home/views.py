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

# Create your views here.
from Scraper.models import Product
from authentication.models import Profile

@login_required(login_url='Login')
def dashboard(request):
    

        users = Profile.objects.get(owner__email=request.user.email)
        product_data=Product.objects.filter(owner=request.user)



        context = {'user_profile': users,'product_data':product_data}


        return render(request, 'dashboard.html', context)



def add_product(request):
    users = User.objects.get(username=request.user)

    user_profile = Profile.objects.get(owner=users)
    context = {'user_profile': users}
    if request.method == 'POST':
        myfile = request.FILES['myfile']
        print('Line no 40',myfile.content_type)
        if myfile.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)

            uploaded_file_url = fs.url(filename)


            empexceldata = pd.read_excel(os.path.join(settings.BASE_DIR, 'static', 'media',filename))

            dbframe = empexceldata
            for dbframe in dbframe.itertuples():

                obj = Product.objects.create(owner=request.user,title=dbframe.Title, price=dbframe.Price,
                                             location=dbframe.Locations,
                                             desc=dbframe.Description, tag1=dbframe.Tag1, tag2=dbframe.Tag2,
                                             tag3=dbframe.Tag3,
                                             tag4=dbframe.Tag4, tag5=dbframe.Tag5)
                obj.save()
            messages.info(request, 'File data successfully import.')
            return redirect('dashboard')
        else:
            messages.info(request,'Only excel type file is accpeted.')
            return redirect('dashboard')
    return redirect('dashboard')


@login_required(login_url='Login')
def Setting(request):
    users = User.objects.get(username=request.user)

    user_profile = Profile.objects.get(owner=users)







    context = {'user_profile': user_profile, 'users': users}
    if request.method == 'POST':
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        email = request.POST.get('Email')
        phone = request.POST.get('phone')
        print(fname, lname, email)

        if len(fname) != 0:
            users.first_name = fname
        if len(lname) != 0:
            users.last_name = lname
        if len(email) != 0:
            users.email = email
        # if len(phone) != 0:
        #     user_profile.phone = phone

        if len(request.FILES) != 0:
            my_file = request.FILES['upload']

            if my_file.content_type == 'image/jpg' or my_file.content_type == 'image/jpeg' or my_file.content_type == 'image/png':
                user_profile.picture = request.FILES['upload']

                users.save()
                user_profile.save()

                messages.success(request, 'Data updated successfully')
                return redirect('Settings')

            messages.success(request, 'Only JPG, PNG & JPEG image type is allowed')
            return redirect('Settings')
        users.save()
        messages.success(request, 'Data updated successfully')
        return redirect('Settings')

    return render(request, 'settings.html', context)


@login_required(login_url='Login')
def setting_security(request):
    user_profile = Profile.objects.get(owner=request.user)



    context = {'user_profile': user_profile}
    if request.method == 'POST':
        users = User.objects.get(email=request.user.email)
        current_password = request.POST.get('current_password')
        phone = request.POST.get('phone')

        new_password = request.POST.get('new_password')

        if len(new_password) != 0:
            users.set_password(new_password)
            users.save()
            # if len(phone) != 0:
            user_profile.changed_default_password = 'Yes'
            user_profile.save()
            user = auth.authenticate(username=request.user.username, password=new_password)
            if user is not None:
                login(request, user)
                messages.info(request, 'Password updated successfully.')
                return redirect('dashboard')






    else:

        return render(request, 'settings-security.html', context)




@login_required(login_url='Login')
def delete_product(request):
    if request.method == 'POST':

            ids = request.POST.getlist('id[]')



            for id in ids:

                x = Product.objects.get(pk=id)
                x.delete()

            print('Product deleted by:', request.user.username)



            return JsonResponse(
                'Product removed', safe=False
            )

@login_required(login_url='Login')
def add_image(request):
    if request.method == 'POST':
        product_pk = request.POST.get('product_pk')
        product_data=Product.objects.get(pk=product_pk)
        if len(request.FILES) != 0:
            my_file = request.FILES['product_image']
            if my_file.content_type == 'image/jpg' or my_file.content_type == 'image/jpeg' or my_file.content_type == 'image/png':
                product_data.image = request.FILES['product_image']
                product_data.save()
                messages.success(request, 'Image uploaded successfully')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid image type. Only JPG,JPEG OR PNG type accpeted.')
                return redirect('dashboard')
        else:
            messages.error(request, 'Select image first please')
            return redirect('dashboard')







