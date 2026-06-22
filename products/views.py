from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from products.models import *

# Create your views here.

#---Authentication---
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        password = request.POST.get('password')
        passwordc = request.POST.get('passwordc')
        
        user_exist = UserModel.objects.filter(username = username).exists()
        if user_exist:
            messages.warning(request, "You are a fool to use same username!")
            return redirect('register')
        
        if password == passwordc:
            UserModel.objects.create_user(
                username = username,
                email = email,
                full_name = full_name,
                password = password
            )
            messages.success(request, "You Entered The Dorm")
            return redirect('log_in')
        else:
            messages.warning(request, "Are you Blind!?")
            return redirect('register')
    return render(request,'auth/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user_id = authenticate(username = username, password = password)
        if user_id:
            login(request, user_id)
            messages.success(request, "Congratulation")
            return redirect('dash_board')
        else:
            messages.warning(request, "You Don't Exist")
            return redirect('log_in')
    return render(request,'auth/log-in.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You escaped successfully")
    return redirect('log_in')

@login_required
def dash_board(request):
    return render(request, 'dashboard.html')

#---CRUD
def read_view(request):
    product = ProductModel.objects.all()
    search = request.GET.get('search')
    filter_data = request.GET.get('filter_data')
    
    if search:
        product = ProductModel.objects.filter(
            Q(name__icontains = search)
        )
        messages.success(request, "Data Found")
    
    if filter_data:
        product = ProductModel.objects.filter(
            Q(status__icontains = filter_data)
        )
        messages.success(request, "Data Filtered Successfully")
    
    context ={
        'pro' : product
    }
    return render(request, 'CRUD/read.html', context)

def create_view(request):
    current_user = request.user
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        product_image = request.FILES.get('product_image')
        production_date = request.POST.get('production_date')
        filter_data = request.POST.get('filter_data')
        
        ProductModel.objects.create(
            name = name,
            description = description,
            price = price,
            product_image = product_image,
            production_date = production_date,
            status = filter_data,
            created_by = current_user
        )
        messages.success(request, "Data Added")
        return redirect('read_view')
        
    return render(request, 'CRUD/create.html')

def update_view(request, tiger):
    pod_cast = ProductModel.objects.get(id=tiger)
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        product_image = request.FILES.get('product_image')
        production_date = request.POST.get('production_date')
        
        pod_cast.name = name
        pod_cast.description = description
        pod_cast.price = price
        if product_image:
            pod_cast.product_image = product_image
        pod_cast.production_date = production_date
        pod_cast.save()
        messages.success(request, "Data Updated Successfully")
        return redirect('read_view')
            
    context = {
        'pro':pod_cast
    }
    return render(request, 'CRUD/update.html', context)

def delete_view(request, tiger):
    ProductModel.objects.get(id=tiger).delete()
    messages.success(request, "Data Deleted")
    return redirect('read_view')
