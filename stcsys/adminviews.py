from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from cmsapp.models import Category,Subcategory,Region,Complaints,ComplaintRemark,UserReg,Type_Traffic_Lights,Traffic_Lights,City,Street,ODMVR,PositionOccupied,VehicleType,VehiclesOwners,VehiclesLicenses,Vehicles,VignetteTable,InsuranceTable
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from cmsapp.models import Region,Type_Traffic_Lights

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from cmsapp.models import CustomUser, UserReg, Region
import os
from django.conf import settings




from django.http import JsonResponse
from django.db.models import Q  # Импортираме за търсене

from cmsapp.models import UserReg, CustomUser  # Увери се, че са правилно импортнати
from django.contrib.auth.hashers import make_password


@login_required(login_url='/')
def ADMINHOME(request):
    complaints = Complaints.objects.all()
    user_count = UserReg.objects.all().count
    category_count = Category.objects.all().count
    subcategory_count = Subcategory.objects.all().count
    region_count = Region.objects.all().count    
    complaints_count = Complaints.objects.all().count
    newcom_count = Complaints.objects.filter(status='0').count()
    ipcom_count = Complaints.objects.filter(status='Inprocess').count()
    closed_count = Complaints.objects.filter(status='Closed').count()
    context = {'user_count':user_count,
    'category_count': category_count,
    'subcategory_count':subcategory_count,
    'region_count':region_count,
    'complaints_count':complaints_count,
    'newcom_count':newcom_count,
    'ipcom_count':ipcom_count,
    'closed_count':closed_count,
    'complaints':complaints        
    }
    return render(request,'admin/admindashboard.html',context)




@login_required(login_url='/')
def ADD_CATEGORY(request):
    if request.method == "POST":
        catname = request.POST.get('catname').strip()  # Премахване на излишни интервали
        if Category.objects.filter(catname__iexact=catname).exists():
            messages.error(request, "Категория с такова име вече съществува!")
            return redirect("add_category")  # Пренасочва обратно към страницата за добавяне
        
        # Ако няма дублиращо се име, създава нова категория
        category = Category(catname=catname)
        category.save()
        messages.success(request, "Категорията е добавена успешно!")
        return redirect("manage_category")  # Пренасочване към списъка с категории

    return render(request, 'admin/add_category.html')


@login_required(login_url='/')
def MANAGE_CATEGORY(request):
    query = request.GET.get('query', '').strip()  # Взимаме въведената стойност от полето за търсене

    # **Търсим във всички категории в базата данни по име на категория**
    if query:
        category_list = Category.objects.filter(catname__icontains=query)  # Търсим в цялата база
    else:
        category_list = Category.objects.all()  # Показваме всички категории

    paginator = Paginator(category_list, 4)  # Пагинация - 10 категории на страница
    page_number = request.GET.get('page')

    try:
        categories = paginator.page(page_number)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)

    context = {
        'categories': categories,
        'query': query,  # Подаваме търсената стойност обратно в шаблона
    }

    return render(request, 'admin/manage_category.html', context)




@login_required(login_url='/')
def UPDATE_CATEGORY(request, id):
    category = Category.objects.get(id=id)

    context = {
         'category': category,
    }

    return render(request, 'admin/update_category.html', context)


@login_required(login_url='/')
def UPDATE_CATEGORY_DETAILS(request):
        if request.method == 'POST':
          cat_id = request.POST.get('cat_id')
          catname = request.POST.get('catname')
          catdes = request.POST.get('catdes')
          category = Category.objects.get(id=cat_id)
          category.catname = catname
          category.catdes = catdes
          category.save()
          messages.success(request,"Категорията е обновена успешно!")
          return redirect('manage_category')
        return render(request, 'admin/update_category.html')






@login_required(login_url='/')
def SEARCH_CATEGORIES_AJAX(request):
    query = request.GET.get('query', '').strip()
    if query:
        categories = Category.objects.filter(catname__icontains=query).values('id', 'catname')[:10]
        return JsonResponse(list(categories), safe=False)
    return JsonResponse([], safe=False)




@login_required(login_url='/')
def DELETE_CATEGORY(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    messages.success(request, 'Категорията е изтрита успешно!')

    return redirect('manage_category')







@login_required(login_url='/')
def ADD_SUBCATEGORY(request):
    if request.method == "POST":
        cat_id = request.POST.get('cat_id')
        subcatname = request.POST.get('subcatname').strip()

        if Subcategory.objects.filter(subcatname__iexact=subcatname, cat_id=cat_id).exists():
            messages.error(request, "Подкатегория с такова име вече съществува!")
            return redirect("add_subcategory")

        category = get_object_or_404(Category, id=cat_id)
        subcategory = Subcategory(cat_id=category, subcatname=subcatname)
        subcategory.save()
        messages.success(request, "Подкатегорията е добавена успешно!")
        return redirect("manage_subcategory")

    categories = Category.objects.all()
    return render(request, 'admin/add_subcategory.html', {'categories': categories})

@login_required(login_url='/')
def MANAGE_SUBCATEGORY(request):
    query = request.GET.get('query', '').strip()

    # Филтриране по име на подкатегория
    if query:
        subcategory_list = Subcategory.objects.filter(subcatname__icontains=query)
    else:
        subcategory_list = Subcategory.objects.all()  # ✅ Извличаме само подкатегории

    paginator = Paginator(subcategory_list, 4)  # Пагинация - 4 подкатегории на страница
    page_number = request.GET.get('page')

    try:
        subcategories = paginator.page(page_number)
    except PageNotAnInteger:
        subcategories = paginator.page(1)
    except EmptyPage:
        subcategories = paginator.page(paginator.num_pages)

    context = {
        'subcategories': subcategories,  # ✅ Уверяваме се, че изпращаме подкатегории, а не категории
        'query': query,
    }
    
    return render(request, 'admin/manage_subcategory.html', context)


@login_required(login_url='/')
def SEARCH_SUBCATEGORIES_AJAX(request):
    query = request.GET.get('query', '').strip()
    if query:
        subcategories = Subcategory.objects.filter(subcatname__icontains=query).values('subcatname')[:10]
        return JsonResponse(list(subcategories), safe=False)
    return JsonResponse([], safe=False)
@login_required(login_url='/')
def UPDATE_SUBCATEGORY(request, id):
    subcategory = get_object_or_404(Subcategory, id=id)
    categories = Category.objects.all()  # Зареждаме всички категории за избор

    context = {
        'subcategory': subcategory,
        'category': categories,
    }

    return render(request, 'admin/update_subcategory.html', context)

@login_required(login_url='/')
def UPDATE_SUBCATEGORY_DETAILS(request):
    if request.method == 'POST':
        subcategory_id = request.POST.get('subcat_id')
        cat_id = request.POST.get('cat_id')
        subcatname = request.POST.get('subcatname').strip()

        try:
            subcategory = Subcategory.objects.get(id=subcategory_id)
            category = get_object_or_404(Category, id=cat_id)
            subcategory.cat_id = category
            subcategory.subcatname = subcatname
            subcategory.save()
            messages.success(request, "Подкатегорията е успешно обновена!")
            return redirect('manage_subcategory')
        except Subcategory.DoesNotExist:
            messages.error(request, "Грешка: Подкатегорията не съществува!")
            return redirect('manage_subcategory')
        except Exception as e:
            messages.error(request, f"Грешка: {e}")
            return redirect('manage_subcategory')

    return redirect('manage_subcategory')



@login_required(login_url='/')
def DELETE_SUBCATEGORY(request, id):
    subcategory = get_object_or_404(Subcategory, id=id)  # ✅ Проверява дали подкатегорията съществува
    subcategory.delete()
    messages.success(request, 'Подкатегорията е изтрита успешно!')
    return redirect('manage_subcategory')















@login_required(login_url='/')
def ADD_REGION(request):
    if request.method == "POST":
        regionname = request.POST.get('regionname').strip()
        city_id = request.POST.get('city')  # Новото поле за град

        if not regionname:
            messages.error(request, "Моля, въведете име на района!")
            return redirect("add_region")

        # Проверяваме дали името на района вече съществува
        if Region.objects.filter(regionname__iexact=regionname).exists():
            messages.error(request, "Район с такова име вече съществува!")
            return redirect("add_region")

        # Проверяваме дали е избран валиден град
        city = None
        if city_id:
            try:
                city = City.objects.get(id=city_id)
            except City.DoesNotExist:
                messages.error(request, "Избраният град не съществува!")
                return redirect("add_region")

        # Създаваме и записваме новия район
        region = Region(regionname=regionname, city=city)
        region.save()

        messages.success(request, "Районът е добавен успешно!")
        return redirect("manage_region")

    return render(request, 'admin/add_region.html')

@login_required(login_url='/')
def MANAGE_REGION(request):
    query = request.GET.get('query', '').strip()  # Взимаме въведената стойност от полето за търсене

    # Филтриране по име на регион, ако има въведена стойност
    if query:
        region_list = Region.objects.filter(regionname__icontains=query)
    else:
        region_list = Region.objects.all()

    paginator = Paginator(region_list, 4)  # Пагинация - 4 региона на страница
    page_number = request.GET.get('page')
    
    try:
        regions = paginator.page(page_number)
    except PageNotAnInteger:
        regions = paginator.page(1)
    except EmptyPage:
        regions = paginator.page(paginator.num_pages)

    context = {
        'regions': regions,
        'query': query,  # Подаваме стойността на заявката обратно в шаблона
    }
    
    return render(request, 'admin/manage_region.html', context)

@login_required(login_url='/')
def SEARCH_REGIONS_AJAX(request):
    query = request.GET.get('query', '').strip()
    if query:
        regions = Region.objects.filter(regionname__icontains=query).values('regionname')[:10]
        return JsonResponse(list(regions), safe=False)
    return JsonResponse([], safe=False)

@login_required(login_url='/')
def UPDATE_REGION(request,id):
    region = Region.objects.get(id=id)

    context = {
         'region':region,
    }

    return render(request,'admin/update_region.html',context)


@login_required(login_url='/')
def UPDATE_REGION(request,id):
    region = Region.objects.get(id=id)

    context = {
         'region':region,
    }

    return render(request,'admin/update_region.html',context)

@login_required(login_url='/')
def UPDATE_REGION_DETAILS(request):
    if request.method == 'POST':
        region_id = request.POST.get('region_id')
        regionname = request.POST.get('regionname')
        city_id = request.POST.get('city')  # Новото поле за град

        try:
            # Проверяваме дали регионът съществува
            region = Region.objects.get(id=region_id)
            region.regionname = regionname

            # Проверяваме дали е избран град и дали съществува
            if city_id:
                try:
                    city = City.objects.get(id=city_id)
                    region.city = city  # Обновяваме града на региона
                except City.DoesNotExist:
                    messages.error(request, "Избраният град не съществува!")
                    return redirect('update_region', id=region_id)

            region.save()
            messages.success(request, "Регионът е обновен успешно!")
            return redirect('manage_region')

        except Region.DoesNotExist:
            messages.error(request, "Грешка: Регионът не съществува!")
            return redirect('manage_region')

    return render(request, 'admin/update_region.html')


@login_required(login_url='/')
def DELETE_REGION(request,id):
    region = Region.objects.get(id=id)
    region.delete()
    messages.success(request,'Регионът е изтрит успешно!')

    return redirect('manage_region')



















@login_required(login_url='/')
def ADD_CITY(request):
    if request.method == "POST":
        city_name = request.POST.get('city_name').strip()  # Премахване на излишни интервали
        post_code = request.POST.get('post_code').strip()  # Прихващане на пощенски код

        if not post_code.isdigit():  # Проверка дали пощенският код съдържа само цифри
            messages.error(request, "Пощенският код трябва да съдържа само цифри!")
            return redirect("add_city")

        if City.objects.filter(city_name__iexact=city_name).exists():
            messages.error(request, "Град с такова име вече съществува!")
            return redirect("add_city")

        # Запис на града и пощенския код
        city = City(city_name=city_name, post_code=int(post_code))
        city.save()

        messages.success(request, "Градът е добавен успешно!")
        return redirect("manage_city")  # Пренасочване към списъка с градове

    return render(request, 'admin/add_city.html')



@login_required(login_url='/')
def MANAGE_CITY(request):
    query = request.GET.get('query', '').strip()  # Взимаме въведената стойност от полето за търсене

    # Филтриране по име на регион, ако има въведена стойност
    if query:
        city_list = City.objects.filter(city_name__icontains=query)
    else:
        city_list = City.objects.all()

    paginator = Paginator(city_list, 50)  # Пагинация - 4 региона на страница
    page_number = request.GET.get('page')
    
    try:
        citys = paginator.page(page_number)
    except PageNotAnInteger:
        citys = paginator.page(1)
    except EmptyPage:
        citys = paginator.page(paginator.num_pages)

    context = {
        'citys': citys,
        'query': query,  # Подаваме стойността на заявката обратно в шаблона
    }
    
    return render(request, 'admin/manage_city.html', context)

@login_required(login_url='/')
def SEARCH_CITY_AJAX(request):
    query = request.GET.get('query', '').strip()
    if query:
        citys = City.objects.filter(city_name__icontains=query).values('city_name')[:10]
        return JsonResponse(list(citys), safe=False)
    return JsonResponse([], safe=False)

@login_required(login_url='/')
def UPDATE_CITY(request,id):
    city = City.objects.get(id=id)

    context = {
         'city':city,
    }

    return render(request,'admin/update_city.html',context)


@login_required(login_url='/')
def UPDATE_CITY(request,id):
    city = City.objects.get(id=id)

    context = {
         'city':city,
    }

    return render(request,'admin/update_city.html',context)


@login_required(login_url='/')
def UPDATE_CITY_DETAILS(request):
    if request.method == 'POST':
        city_id = request.POST.get('city_id')
        city_name = request.POST.get('city_name')
        post_code = request.POST.get('post_code')

        city = City.objects.get(id=city_id)
        city.city_name = city_name
        city.post_code = post_code  # Добавено записване на пощенски код

        city.save()
        messages.success(request, "Градът е обновен успешно!")
        return redirect('manage_city')

    return render(request, 'admin/update_city.html')



@login_required(login_url='/')
def DELETE_CITY(request,id):
    city = City.objects.get(id=id)
    city.delete()
    messages.success(request,'Градът е изтрит успешно!')

    return redirect('manage_city')



@login_required(login_url='/')
def ADD_STREET(request):
    if request.method == "POST":
        street_name = request.POST.get('street_name').strip()
        city_id = request.POST.get('city_id')

        if not city_id:
            messages.error(request, "Моля, изберете град!")
            return redirect("add_street")

        # Проверка дали градът съществува
        try:
            city = City.objects.get(id=city_id)
        except City.DoesNotExist:
            messages.error(request, "Избраният град не съществува!")
            return redirect("add_street")

        # Проверка за дублирана улица в същия град
        if Street.objects.filter(street_name__iexact=street_name, city_id=city).exists():
            messages.error(request, "Улица с такова име вече съществува в този град!")
            return redirect("add_street")

        # Запис на улицата
        street = Street(street_name=street_name, city_id=city)
        street.save()

        messages.success(request, "Улицата е добавена успешно!")
        return redirect("manage_street")

    # Зареждаме всички градове за dropdown менюто
    cities = City.objects.all()
    return render(request, 'admin/add_street.html', {"cities": cities})






@login_required(login_url='/')
def MANAGE_STREET(request):
    query = request.GET.get('query', '').strip()

    if query:
        street_list = Street.objects.filter(street_name__icontains=query).select_related('city_id')
    else:
        street_list = Street.objects.all().select_related('city_id')

    paginator = Paginator(street_list, 50)
    page_number = request.GET.get('page')

    try:
        streets = paginator.page(page_number)
    except PageNotAnInteger:
        streets = paginator.page(1)
    except EmptyPage:
        streets = paginator.page(paginator.num_pages)

    context = {
        'streets': streets,
        'query': query,
    }

    return render(request, 'admin/manage_street.html', context)



@login_required(login_url='/')
def SEARCH_STREET_AJAX(request):
    query = request.GET.get('query', '').strip()
    if query:
        streets = Street.objects.filter(street_name__icontains=query).values('street_name')[:10]
        return JsonResponse(list(streets), safe=False)
    return JsonResponse([], safe=False)

@login_required(login_url='/')
def UPDATE_STREET(request, id):
    try:
        street = Street.objects.get(id=id)
    except Street.DoesNotExist:
        messages.error(request, "Тази улица не съществува!")
        return redirect("manage_street")

    cities = City.objects.all()  # Зареждаме всички градове

    print(f"Cities loaded: {cities}")  # Дебъгване - виж дали има градове в конзолата

    context = {
        "street": street,
        "cities": cities,
    }
    return render(request, "admin/update_street.html", context)


@login_required(login_url='/')
def UPDATE_STREET_DETAILS(request):
    if request.method == "POST":
        street_id = request.POST.get("street_id")
        street_name = request.POST.get("street_name").strip()
        city_id = request.POST.get("city_id")

        try:
            street = Street.objects.get(id=street_id)
        except Street.DoesNotExist:
            messages.error(request, "Тази улица не съществува!")
            return redirect("manage_street")

        if not city_id:
            messages.error(request, "Моля, изберете населено място!")
            return redirect("update_street", id=street.id)

        try:
            city = City.objects.get(id=city_id)
        except City.DoesNotExist:
            messages.error(request, "Избраното населено място не съществува!")
            return redirect("update_street", id=street.id)

        # Проверка за дублиране
        if Street.objects.exclude(id=street.id).filter(street_name__iexact=street_name, city_id=city).exists():
            messages.error(request, "Вече съществува улица с това име в същото населено място!")
            return redirect("update_street", id=street.id)

        # Обновяване на данните
        street.street_name = street_name
        street.city_id = city
        street.save()

        messages.success(request, "Улицата беше успешно обновена!")
        return redirect("manage_street")

    return redirect("manage_street")


@login_required(login_url='/')
def DELETE_STREET(request,id):
    street = Street.objects.get(id=id)
    street.delete()
    messages.success(request,'Улицата е изтрит успешно!')

    return redirect('manage_street')










@login_required(login_url='/')
def ADD_TYPE_TRAFFIC_LIGHTS(request):
    if request.method == "POST":
        type_traffic_lights_name = request.POST.get('type_traffic_lights_name').strip()  # Премахване на излишни интервали
        if Type_Traffic_Lights.objects.filter(type_traffic_lights_name__iexact=type_traffic_lights_name).exists():
            messages.error(request, "Тип светофар с такова име вече съществува!")
            return redirect("add_type_traffic_lights")  # Пренасочва обратно към страницата за добавяне
        
        # Ако няма дублиращо се име, създава нов регион
        type_traffic_lights = Type_Traffic_Lights(type_traffic_lights_name=type_traffic_lights_name)
        type_traffic_lights.save()
        messages.success(request, "Типът светофар е добавен успешно!")
        return redirect("manage_type_traffic_lights")  # Пренасочване към списъка с региони

    return render(request, 'admin/add_type_traffic_lights.html')

@login_required(login_url='/')
def MANAGE_TYPE_TRAFFIC_LIGHTS(request):
    query = request.GET.get('query', '').strip()  # Взимаме въведената стойност от полето за търсене

    # Филтриране по име на регион, ако има въведена стойност
    if query:
        type_traffic_lights_list = Type_Traffic_Lights.objects.filter(type_traffic_lights_name__icontains=query)
    else:
        type_traffic_lights_list = Type_Traffic_Lights.objects.all()

    paginator = Paginator(type_traffic_lights_list, 4)  # Пагинация - 4 региона на страница
    page_number = request.GET.get('page')
    
    try:
        type_traffic_lightss = paginator.page(page_number)
    except PageNotAnInteger:
        type_traffic_lightss = paginator.page(1)
    except EmptyPage:
        type_traffic_lightss = paginator.page(paginator.num_pages)

    context = {
        'type_traffic_lightss': type_traffic_lightss,
        'query': query,  # Подаваме стойността на заявката обратно в шаблона
    }
    
    return render(request, 'admin/manage_type_traffic_lights.html', context)

@login_required(login_url='/')
def SEARCH_TYPE_TRAFFIC_LIGHTS_AJAX(request):
    query = request.GET.get('query', '').strip()
    if query:
        type_traffic_lights = Type_Traffic_Lights.objects.filter(type_traffic_lights_name__icontains=query).values('id', 'type_traffic_lights_name')[:10]
        return JsonResponse(list(type_traffic_lights), safe=False)
    return JsonResponse([], safe=False)

@login_required(login_url='/')
def UPDATE_TYPE_TRAFFIC_LIGHTS(request, id):
    # Вземане на съществуващия запис
    type_traffic_lights = get_object_or_404(Type_Traffic_Lights, id=id)

    if request.method == 'POST':
        type_traffic_lights_name = request.POST.get('type_traffic_lights_name')

        # Запазване на новите данни
        type_traffic_lights.type_traffic_lights_name = type_traffic_lights_name
        type_traffic_lights.save()

        messages.success(request, "Типът светофар е обновен успешно!")
        return redirect('manage_type_traffic_lights')

    # Подаване на данните към шаблона
    context = {
        'type_traffic_lights': type_traffic_lights
    }
    return render(request, 'admin/update_type_traffic_lights.html', context)



@login_required(login_url='/')
def UPDATE_TYPE_TRAFFIC_LIGHTS_DETAILS(request):
        if request.method == 'POST':
          type_traffic_lights_id = request.POST.get('type_traffic_lights_id')
          type_traffic_lights_name = request.POST.get('type_traffic_lights_name')

          type_traffic_lights = Type_Traffic_Lights.objects.get(id=type_traffic_lights_id)
          type_traffic_lights.type_traffic_lights_name = type_traffic_lights_name

          type_traffic_lights.save()
          messages.success(request,"Района е обновен успешно!")
          return redirect('manage_type_traffic_lights')
        return render(request, 'admin/update_type_traffic_lights.html')


@login_required(login_url='/')
def DELETE_TYPE_TRAFFIC_LIGHTS(request,id):
    type_traffic_lights = Type_Traffic_Lights.objects.get(id=id)
    type_traffic_lights.delete()
    messages.success(request,'Типът светофар е изтрит успешно!')

    return redirect('manage_type_traffic_lights')


@login_required(login_url='/')
def ADD_TRAFFIC_LIGHTS(request):
    if request.method == "POST":
        type_traffic_light_id = request.POST.get('type_traffic_light')
        city_id = request.POST.get('city')
        street_id = request.POST.get('street')
        region_id = request.POST.get('region')
        topic = request.POST.get('topic').strip()

        try:
            type_traffic_light = Type_Traffic_Lights.objects.get(id=type_traffic_light_id)
            city = City.objects.get(id=city_id)
            street = Street.objects.get(id=street_id)
            region = Region.objects.get(id=region_id)
        except (Type_Traffic_Lights.DoesNotExist, City.DoesNotExist, Street.DoesNotExist, Region.DoesNotExist):
            messages.error(request, "Невалидни данни! Моля, опитайте отново.")
            return redirect("add_traffic_lights")

        traffic_light = Traffic_Lights(
            type_traffic_light=type_traffic_light,
            city=city,
            street=street,
            region=region,
            topic=topic
        )
        traffic_light.save()

        messages.success(request, "Светофарът е добавен успешно!")
        return redirect("manage_traffic_lights")

    type_traffic_lights = Type_Traffic_Lights.objects.all()
    
    return render(request, 'admin/add_traffic_lights.html', {
        "type_traffic_lights": type_traffic_lights
    })


# AJAX за градове (динамично търсене)
def search_traffic_lights_cities(request):
    query = request.GET.get('q', '').strip()
    if len(query) >= 2:
        cities = City.objects.filter(city_name__icontains=query).values("id", "city_name")[:10]
        return JsonResponse({"results": [{"id": c["id"], "text": c["city_name"]} for c in cities]})
    return JsonResponse({"results": []})


# AJAX за улици (зависи от избран град)
def search_traffic_lights_streets(request):
    city_id = request.GET.get('city_id')
    query = request.GET.get('q', '').strip()
    if city_id and len(query) >= 2:
        streets = Street.objects.filter(city_id_id=city_id, street_name__icontains=query).values("id", "street_name")[:10]
        return JsonResponse({"results": [{"id": s["id"], "text": s["street_name"]} for s in streets]})
    return JsonResponse({"results": []})


# AJAX за региони (зависи от избран град)
def search_traffic_lights_regions(request):
    city_id = request.GET.get('city_id')
    query = request.GET.get('q', '').strip()
    if city_id and len(query) >= 2:
        regions = Region.objects.filter(city_id=city_id, regionname__icontains=query).values("id", "regionname")[:10]
        return JsonResponse({"results": [{"id": r["id"], "text": r["regionname"]} for r in regions]})
    return JsonResponse({"results": []})





@login_required(login_url='/')
def MANAGE_TRAFFIC_LIGHTS(request):
    query = request.GET.get('query', '').strip()

    # Филтриране по тема на светофара или по град
    if query:
        traffic_lights_list = Traffic_Lights.objects.filter(
            Q(topic__icontains=query) |
            Q(city__city_name__icontains=query)
        ).select_related('type_traffic_light', 'city', 'street', 'region')
    else:
        traffic_lights_list = Traffic_Lights.objects.all().select_related('type_traffic_light', 'city', 'street', 'region')

    paginator = Paginator(traffic_lights_list, 10)  # Пагинация - 10 светофара на страница
    page_number = request.GET.get('page')

    try:
        traffic_lights_list = paginator.page(page_number)
    except PageNotAnInteger:
        traffic_lights_list = paginator.page(1)
    except EmptyPage:
        traffic_lights_list = paginator.page(paginator.num_pages)

    context = {
        'traffic_lights_list': traffic_lights_list,
        'query': query,  # Подаваме стойността на заявката обратно в шаблона
    }

    return render(request, 'admin/manage_traffic_lights.html', context)



@login_required(login_url='/')
def SEARCH_TRAFFIC_LIGHTS_AJAX(request):
    query = request.GET.get('query', '').strip()
    if query:
        traffic_lights = Traffic_Lights.objects.filter(traffic_lights_name__icontains=query).values('id', 'traffic_lights_name')[:10]
        return JsonResponse(list(traffic_lights), safe=False)
    return JsonResponse([], safe=False)

@login_required(login_url='/')
def UPDATE_TRAFFIC_LIGHTS(request, id):
    traffic_light = get_object_or_404(Traffic_Lights, id=id)
    type_traffic_lights = Type_Traffic_Lights.objects.all()

    if request.method == "POST":
        type_traffic_light_id = request.POST.get('type_traffic_light')
        city_id = request.POST.get('city')
        street_id = request.POST.get('street')
        region_id = request.POST.get('region')
        topic = request.POST.get('topic').strip()

        try:
            type_traffic_light = Type_Traffic_Lights.objects.get(id=type_traffic_light_id)
            city = City.objects.get(id=city_id)
            street = Street.objects.get(id=street_id)
            region = Region.objects.get(id=region_id)
        except (Type_Traffic_Lights.DoesNotExist, City.DoesNotExist, Street.DoesNotExist, Region.DoesNotExist):
            messages.error(request, "Невалидни данни! Моля, опитайте отново.")
            return redirect("update_traffic_lights", id=id)

        traffic_light.type_traffic_light = type_traffic_light
        traffic_light.city = city
        traffic_light.street = street
        traffic_light.region = region
        traffic_light.topic = topic
        traffic_light.save()

        messages.success(request, "Светофарът е редактиран успешно!")
        return redirect("manage_traffic_lights")

    context = {
        "traffic_light": traffic_light,
        "type_traffic_lights": type_traffic_lights
    }

    return render(request, "admin/update_traffic_lights.html", context)



@login_required(login_url='/')
def UPDATE_TRAFFIC_LIGHTS_DETAILS(request):
        if request.method == 'POST':
          traffic_lights_id = request.POST.get('traffic_lights_id')
          traffic_lights_name = request.POST.get('traffic_lights_name')

          traffic_lights = Traffic_Lights.objects.get(id=traffic_lights_id)
          traffic_lights.traffic_lights_name = traffic_lights_name

          traffic_lights.save()
          messages.success(request,"Района е обновен успешно!")
          return redirect('manage_traffic_lights')
        return render(request, 'admin/update_traffic_lights.html')


@login_required(login_url='/')
def DELETE_TRAFFIC_LIGHTS(request,id):
    traffic_lights = Traffic_Lights.objects.get(id=id)
    traffic_lights.delete()
    messages.success(request,'Типът светофар е изтрит успешно!')

    return redirect('manage_traffic_lights')





















@login_required(login_url='/')
def MANAGEUSERS(request):
    query = request.GET.get('query', '').strip()  # Основно търсене по име, фамилия, телефон, имейл
    user_type = request.GET.get('user_type', '')  # Филтър по потребителски тип

    # Запитване за търсене
    user_list = UserReg.objects.filter(
        Q(admin__first_name__icontains=query) |
        Q(admin__last_name__icontains=query) |
        Q(admin__email__icontains=query) |
        Q(mobilenumber__icontains=query)
    )

    # Прилага филтър по user_type, ако е избран
    if user_type:
        user_list = user_list.filter(admin__user_type=user_type)

    # Пагинация
    paginator = Paginator(user_list, 4)
    page_number = request.GET.get('page')
    try:
        userlist = paginator.page(page_number)
    except PageNotAnInteger:
        userlist = paginator.page(1)
    except EmptyPage:
        userlist = paginator.page(paginator.num_pages)

    context = {
        'userlist': userlist,
        'query': query,
        'selected_user_type': user_type,  # Запазва избора в шаблона
    }
    return render(request, 'admin/manage_userlist.html', context)



login_required(login_url='/')
def VIEWUSERS(request,id):
    listedusers = UserReg.objects.get(id=id)
    
    context = {
         'listedusers':listedusers,
    }

    return render(request,'admin/view_users_details.html',context)

login_required(login_url='/')
def DELETEUSERS(request,id):
    delusers = UserReg.objects.get(id=id)
    delusers.delete()
    messages.success(request,'Record Delete Succeesfully!!!')

    return redirect('manageusers')



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from cmsapp.models import CustomUser, UserReg, Region

@login_required(login_url='/')
def EDIT_USER(request, id):
    user = get_object_or_404(UserReg, id=id)
    admin_user = get_object_or_404(CustomUser, id=user.admin_id)
    regions = Region.objects.all()  # Взимаме всички региони

    if request.method == 'POST':
        admin_user.first_name = request.POST.get('first_name')
        admin_user.last_name = request.POST.get('last_name')
        admin_user.email = request.POST.get('email')
        user.mobilenumber = request.POST.get('mobilenumber')

        # ✅ Запис на потребителски тип (user_type)
        user_type_value = request.POST.get('user_type')
        if user_type_value:
            admin_user.user_type = int(user_type_value)

        # ✅ Ако потребителят е полицай (user_type=3), запазваме региона
        if admin_user.user_type == 3:
            region_id = request.POST.get('region')
            if region_id:
                try:
                    user.region = Region.objects.get(id=region_id)
                except Region.DoesNotExist:
                    messages.error(request, "Избраният регион не съществува!")
                    return redirect('edit_user', id=id)
        else:
            user.region = None  # Изчистваме региона, ако потребителят НЕ е полицай

        # ✅ Запазване на нова парола (ако има въведена)
        new_password = request.POST.get('password')
        if new_password:
            admin_user.password = make_password(new_password)

        # ✅ Запазване на профилна снимка (ако има качена нова)
        if 'profile_pic' in request.FILES:
            admin_user.profile_pic = request.FILES['profile_pic']

        admin_user.save()
        user.save()

        messages.success(request, "Потребителят е успешно редактиран!")
        return redirect('manageusers')

    # ✅ Подаваме user_type и region_id към шаблона
    return render(request, 'admin/edit_user.html', {
        'user': user,
        'admin_user': admin_user,
        'regions': regions
    })



@login_required(login_url='/')
def SEARCH_USERS_AJAX(request):
    query = request.GET.get('query', '').strip()
    
    if query:
        users = UserReg.objects.filter(
            Q(admin__first_name__icontains=query) |
            Q(admin__last_name__icontains=query) |
            Q(admin__email__icontains=query) |
            Q(mobilenumber__icontains=query)
        ).values('admin__first_name', 'admin__last_name', 'admin__email', 'mobilenumber')[:10]

        return JsonResponse(list(users), safe=False)

    return JsonResponse([], safe=False)






@login_required(login_url='/')
def USERSCOMPLAINTS(request, id):
    complaints=Complaints.objects.filter(userregid=id)
    context = {'complaints':complaints}
    return render(request, 'admin/user-lodged-complaints.html', context)





@login_required(login_url='/')
def LODGEDCOMPLAINTS(request):
    complaint_list = Complaints.objects.all().order_by('-complaintdate_at')  # Подреждане по дата
    paginator = Paginator(complaint_list, 10)  # Показва 10 сигнала на страница

    # Вземане на номер на страницата от заявката
    page_number = request.GET.get('page')
    
    try:
        complaints = paginator.get_page(page_number)
    except PageNotAnInteger:
        complaints = paginator.get_page(1)
    except EmptyPage:
        complaints = paginator.get_page(paginator.num_pages)

    context = {'complaints': complaints}
    return render(request, 'admin/lodged-complaints.html', context)




@login_required(login_url='/')
def VIEWLODGEDCOMPLAINTS(request, id):
    print(f"🔍 Проверявам запис с ID={id}")  # ✅ Дебъгване на ID-то

    try:
        # Опитваме се да получим запис от базата
        complaint = Complaints.objects.select_related(
            'userregid__admin', 'cat_id', 'subcategory_id', 'city', 'street'
        ).get(id=id)

        complaintsremarks = ComplaintRemark.objects.filter(comp_id_id=id)

        context = {
            'complaint': complaint,
            'complaintsremarks': complaintsremarks,
        }

        print(f"✅ Намерен запис с ID={id}")  # Потвърждение, че записът съществува
        return render(request, 'admin/view-lodged-complaints.html', context)

    except Complaints.DoesNotExist:
        print(f"❌ Грешка: Няма запис с ID={id} в Django!")  # Дебъгване в терминала

        # Извеждане на всички записи в базата, за да видим дали записът е там
        all_complaints = Complaints.objects.all().values_list('id', flat=True)
        print(f"📌 Списък на всички ID в базата: {list(all_complaints)}")  

        return HttpResponse(f"❌ Грешка: Не е намерен запис с ID={id}", status=404)








def LODGEDCOMPLAINTSREMARK(request):
    if request.method == 'POST':
        complaint_id = request.POST.get('comp_id')
        remark_text = request.POST.get('remark')
        status = request.POST.get('status')
        
        # Update the Complaints model
        lodged_complaint = Complaints.objects.get(id=complaint_id)
        lodged_complaint.remark = remark_text
        lodged_complaint.status = status
        lodged_complaint.save()
        
        # Create a new ComplaintRemark entry
        new_remark = ComplaintRemark.objects.create(
            comp_id_id=lodged_complaint,  # Pass the Complaints instance here
            remark=remark_text,
            status=status,
            remarkdate=timezone.now()
        )
        
        messages.success(request, "Status updated successfully")
        return redirect('lodgedcomplaint')
    else:
        # Handle the GET request if needed
        complaint_id = request.GET.get('comp_id')
        if complaint_id:
            lodged_complaint = get_object_or_404(Complaints, id=complaint_id)
            remarks = ComplaintRemark.objects.filter(comp_id_id=lodged_complaint)
            context = {'complaint': lodged_complaint, 'remarks': remarks}
        else:
            context = {}
             
    return render(request, 'admin/lodged-complaints.html', context)




@login_required(login_url='/')
def NEWCOMPLAINTS(request):
    complaints_list = Complaints.objects.filter(status='0') \
        .select_related('userregid', 'userregid__admin', 'cat_id', 'subcategory_id', 'city', 'street') \
        .values('id', 'complaint_number', 'complaindetails', 'complaintdate_at', 'status', 
                'cat_id__catname', 'subcategory_id__subcatname', 
                'city__city_name', 'street__street_name', 
                'userregid__mobilenumber', 'userregid__admin__first_name', 'userregid__admin__last_name')

    # ✅ Пагинация - 10 сигнала на страница
    paginator = Paginator(complaints_list, 10)
    page = request.GET.get('page')

    try:
        complaints = paginator.page(page)
    except PageNotAnInteger:
        complaints = paginator.page(1)
    except EmptyPage:
        complaints = paginator.page(paginator.num_pages)

    context = {'complaints': complaints}  # 🔥 Коригирано за съвместимост с темплейта
    return render(request, 'admin/new-complaints.html', context)



@login_required(login_url='/')
def INPROCESSCOMPLAINTS(request):
    # Взимаме само нужните колони и правим `JOIN` с важните таблици
    complaints_list = Complaints.objects.filter(status='Inprocess') \
        .select_related('userregid', 'userregid__admin', 'cat_id', 'subcategory_id', 'city', 'street') \
        .only('id', 'complaint_number', 'complaindetails', 'complaintdate_at', 'status', 
              'cat_id__catname', 'subcategory_id__subcatname', 
              'city__city_name', 'street__street_name', 
              'userregid__mobilenumber', 'userregid__admin__first_name', 'userregid__admin__last_name')

    # ✅ Пагинация - 10 сигнала на страница
    paginator = Paginator(complaints_list, 10)
    page = request.GET.get('page')

    try:
        complaints = paginator.page(page)
    except PageNotAnInteger:
        complaints = paginator.page(1)
    except EmptyPage:
        complaints = paginator.page(paginator.num_pages)

    context = {'complaints': complaints}
    return render(request, 'admin/inprocess_complaints.html', context)




@login_required(login_url='/')
def CLOSEDCOMPLAINTS(request):
    # Оптимизирана заявка с select_related и only
    closed_complaints = Complaints.objects.select_related(
        "userregid__admin", "city", "street"
    ).only(
        "id", "complaint_number", "status", "complaindetails", 
        "complaintdate_at", "userregid__admin__first_name", 
        "userregid__admin__last_name", "userregid__mobilenumber",
        "city__city_name", "street__street_name"
    ).filter(status="Closed").order_by("-complaintdate_at")

    # Пагинация (10 записа на страница)
    paginator = Paginator(closed_complaints, 10)
    page_number = request.GET.get("page")
    closed_complaints = paginator.get_page(page_number)

    context = {"closed_complaints": closed_complaints}
    return render(request, "admin/closed_complaints.html", context)



def COMPLAINTSREPORT(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    lodgedcomplaints = []

    if start_date and end_date:
        # Validate the date inputs
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'admin/complaint-between-date-report.html', {'lodgedcomplaints': lodgedcomplaints, 'error_message': 'Invalid date format'})

        # Filter visitors between the given date range
        lodgedcomplaints = Complaints.objects.filter(complaintdate_at__range=(start_date, end_date))

    return render(request, 'admin/complaint-between-date-report.html', {'lodgedcomplaints': lodgedcomplaints,'start_date':start_date,'end_date':end_date})


def USERBDREPORT(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    userdetails = []

    if start_date and end_date:
        # Validate the date inputs
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'admin/user-between-date-report.html', {'userdetails': userdetails, 'error_message': 'Invalid date format'})

        # Filter visitors between the given date range
        userdetails = UserReg.objects.filter(regdate_at__range=(start_date, end_date))

    return render(request, 'admin/user-between-date-report.html', {'userdetails': userdetails,'start_date':start_date,'end_date':end_date})


def Search_Complaints(request):
    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            # Filter records where email or mobilenumber contains the query
            searchcomp = Complaints.objects.filter(complaint_number__icontains=query) | Complaints.objects.filter(userregid__mobilenumber__icontains=query)
            messages.info(request, "Search against " + query)
            return render(request, 'admin/search-complaints.html', {'searchcomp': searchcomp, 'query': query})
        else:
            print("No Record Found")
            return render(request, 'admin/search-complaints.html', {})

def Search_Users(request):
    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            # Filter records where email or mobilenumber contains the query
            searchusers = UserReg.objects.filter(admin__email__icontains=query) |  UserReg.objects.filter(mobilenumber__icontains=query)| UserReg.objects.filter(admin__first_name__icontains=query)| UserReg.objects.filter(admin__last_name__icontains=query)
            
           
            messages.info(request, "Search against " + query)
            return render(request, 'admin/search-users.html', {'searchusers': searchusers, 'query': query})
        else:
            print("No Record Found")
            return render(request, 'admin/search-users.html', {})





@login_required(login_url='/')
def ADD_USER(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        user_type = request.POST.get('user_type')
        password = request.POST.get('password')
        mobilenumber = request.POST.get('mobilenumber')
        profile_pic = request.FILES.get('profile_pic')

        # Създаване на CustomUser
        user = CustomUser.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            user_type=user_type,
            password=make_password(password),  # Записване на паролата хеширана
            profile_pic=profile_pic
        )

        # Създаване на UserReg
        UserReg.objects.create(
            admin=user,
            mobilenumber=mobilenumber
        )

        messages.success(request, "Потребителят е добавен успешно!")
        return redirect('manageusers')

    return render(request, 'admin/add_user.html')








@login_required(login_url='/')
def ADD_ODMVR(request):
    if request.method == "POST":
        odmvr_name = request.POST.get('odmvr_name').strip()

        if ODMVR.objects.filter(odmvr_name__iexact=odmvr_name).exists():
            messages.error(request, "Запис с това име вече съществува!")
            return redirect("add_odmvr")

        odmvr = ODMVR(odmvr_name=odmvr_name)
        odmvr.save()
        messages.success(request, "Записът е добавен успешно!")
        return redirect("manage_odmvr")

    return render(request, 'admin/add_odmvr.html')



@login_required(login_url='/')
def MANAGE_ODMVR(request):
    query = request.GET.get('query', '').strip()
    
    if query:
        odmvr_list = ODMVR.objects.filter(odmvr_name__icontains=query)
    else:
        odmvr_list = ODMVR.objects.all()

    print(f"🔎 Намерени {odmvr_list.count()} записи в ODMVR")  # ✅ ПРОВЕРКА

    paginator = Paginator(odmvr_list, 4)
    page_number = request.GET.get('page')

    try:
        odmvr_items = paginator.page(page_number)
    except PageNotAnInteger:
        odmvr_items = paginator.page(1)
    except EmptyPage:
        odmvr_items = paginator.page(paginator.num_pages)

    print(f"📋 Заредени {len(odmvr_items)} записа за показване!")  # ✅ ПРОВЕРКА

    context = {
        'odmvr_items': odmvr_items,
        'query': query,
    }

    return render(request, 'admin/manage_odmvr.html', context)



@login_required(login_url='/')
def SEARCH_ODMVR_AJAX(request):
    query = request.GET.get('query', '').strip()
    if query:
        odmvr_items = ODMVR.objects.filter(odmvr_name__icontains=query).values('id', 'odmvr_name')[:10]
        return JsonResponse(list(odmvr_items), safe=False)
    return JsonResponse([], safe=False)


@login_required(login_url='/')
def UPDATE_ODMVR(request, id):
    odmvr = get_object_or_404(ODMVR, id=id)

    if request.method == 'POST':
        odmvr_name = request.POST.get('odmvr_name')
        odmvr.odmvr_name = odmvr_name
        odmvr.save()

        messages.success(request, "Записът е обновен успешно!")
        return redirect('manage_odmvr')

    context = {
        'odmvr': odmvr
    }
    return render(request, 'admin/update_odmvr.html', context)


@login_required(login_url='/')
def DELETE_ODMVR(request, id):
    odmvr = ODMVR.objects.get(id=id)
    odmvr.delete()
    messages.success(request, 'Записът е изтрит успешно!')
    return redirect('manage_odmvr')




@login_required(login_url='/')
def ADD_POSITION_OCCUPIED(request):
    if request.method == "POST":
        position_occupied_name = request.POST.get('position_occupied_name').strip()
        
        if PositionOccupied.objects.filter(position_occupied_name__iexact=position_occupied_name).exists():
            messages.error(request, "Тази позиция вече съществува!")
            return redirect("add_position_occupied")

        position_occupied = PositionOccupied(position_occupied_name=position_occupied_name)
        position_occupied.save()
        messages.success(request, "Позицията е добавена успешно!")
        return redirect("manage_position_occupied")

    return render(request, 'admin/add_position_occupied.html')


@login_required(login_url='/')
def MANAGE_POSITION_OCCUPIED(request):
    query = request.GET.get('query', '').strip()

    if query:
        position_list = PositionOccupied.objects.filter(position_occupied_name__icontains=query)
    else:
        position_list = PositionOccupied.objects.all()

    paginator = Paginator(position_list, 4)
    page_number = request.GET.get('page')

    try:
        position_items = paginator.page(page_number)
    except PageNotAnInteger:
        position_items = paginator.page(1)
    except EmptyPage:
        position_items = paginator.page(paginator.num_pages)

    context = {
        'position_items': position_items,
        'query': query,
    }

    return render(request, 'admin/manage_position_occupied.html', context)


@login_required(login_url='/')
def SEARCH_POSITION_OCCUPIED_AJAX(request):
    query = request.GET.get('query', '').strip()
    if query:
        positions = PositionOccupied.objects.filter(position_occupied_name__icontains=query).values('id', 'position_occupied_name')[:10]
        return JsonResponse(list(positions), safe=False)
    return JsonResponse([], safe=False)


@login_required(login_url='/')
def UPDATE_POSITION_OCCUPIED(request, id):
    position_occupied = get_object_or_404(PositionOccupied, id=id)

    if request.method == 'POST':
        position_occupied_name = request.POST.get('position_occupied_name')
        position_occupied.position_occupied_name = position_occupied_name
        position_occupied.save()

        messages.success(request, "Позицията е обновена успешно!")
        return redirect('manage_position_occupied')

    context = {
        'position_occupied': position_occupied
    }
    return render(request, 'admin/update_position_occupied.html', context)


@login_required(login_url='/')
def DELETE_POSITION_OCCUPIED(request, id):
    position_occupied = get_object_or_404(PositionOccupied, id=id)
    position_occupied.delete()
    messages.success(request, "Позицията е изтрита успешно!")
    return redirect('manage_position_occupied')





@login_required(login_url='/')
def ADD_VEHICLE_TYPE(request):
    if request.method == "POST":
        vehicle_type_name = request.POST.get('vehicle_type_name').strip()
        if VehicleType.objects.filter(vehicle_type_name__iexact=vehicle_type_name).exists():
            messages.error(request, "Тип превозно средство с такова име вече съществува!")
            return redirect("add_vehicle_type")
        
        vehicle_type = VehicleType(vehicle_type_name=vehicle_type_name)
        vehicle_type.save()
        messages.success(request, "Типът превозно средство е добавен успешно!")
        return redirect("manage_vehicle_type")

    return render(request, 'admin/add_vehicle_type.html')


@login_required(login_url='/')
def MANAGE_VEHICLE_TYPE(request):
    query = request.GET.get('query', '').strip()

    if query:
        vehicle_type_list = VehicleType.objects.filter(vehicle_type_name__icontains=query)
    else:
        vehicle_type_list = VehicleType.objects.all()

    paginator = Paginator(vehicle_type_list, 10)
    page_number = request.GET.get('page')

    try:
        vehicle_types = paginator.page(page_number)
    except PageNotAnInteger:
        vehicle_types = paginator.page(1)
    except EmptyPage:
        vehicle_types = paginator.page(paginator.num_pages)

    context = {
        'vehicle_types': vehicle_types,
        'query': query,
    }

    return render(request, 'admin/manage_vehicle_type.html', context)


@login_required(login_url='/')
def SEARCH_VEHICLE_TYPE_AJAX(request):
    query = request.GET.get('query', '').strip()
    if query:
        vehicle_types = VehicleType.objects.filter(vehicle_type_name__icontains=query).values('id', 'vehicle_type_name')[:10]
        return JsonResponse(list(vehicle_types), safe=False)
    return JsonResponse([], safe=False)


@login_required(login_url='/')
def UPDATE_VEHICLE_TYPE(request, id):
    vehicle_type = get_object_or_404(VehicleType, id=id)

    if request.method == 'POST':
        vehicle_type_name = request.POST.get('vehicle_type_name').strip()
        vehicle_type.vehicle_type_name = vehicle_type_name
        vehicle_type.save()
        messages.success(request, "Типът превозно средство е обновен успешно!")
        return redirect('manage_vehicle_type')

    context = {
        'vehicle_type': vehicle_type
    }
    return render(request, 'admin/update_vehicle_type.html', context)


@login_required(login_url='/')
def DELETE_VEHICLE_TYPE(request, id):
    vehicle_type = get_object_or_404(VehicleType, id=id)
    vehicle_type.delete()
    messages.success(request, 'Типът превозно средство е изтрит успешно!')
    return redirect('manage_vehicle_type')






@login_required(login_url='/')
def ADD_VEHICLES_OWNER(request):
    if request.method == "POST":
        name = request.POST.get('name').strip()
        fathers_name = request.POST.get('fathers_name').strip()
        surname = request.POST.get('surname').strip()
        personal_no = request.POST.get('personal_no').strip()
        nationality = request.POST.get('nationality').strip()
        date_of_birth = request.POST.get('date_of_birth')
        date_of_expiry = request.POST.get('date_of_expiry')
        document_number = request.POST.get('document_number').strip()
        place_of_birth = request.POST.get('place_of_birth').strip()
        residence = request.POST.get('residence').strip()
        height = request.POST.get('height')
        color_of_eyes = request.POST.get('color_of_eyes').strip()
        authority = request.POST.get('authority').strip()
        date_of_issue = request.POST.get('date_of_issue')

        # Проверка за дублиране на Personal NO или Document Number
        if VehiclesOwners.objects.filter(personal_no=personal_no).exists():
            messages.error(request, "Лице с този Personal NO вече съществува!")
            return redirect("add_vehicles_owner")

        if VehiclesOwners.objects.filter(document_number=document_number).exists():
            messages.error(request, "Лице с този документ вече съществува!")
            return redirect("add_vehicles_owner")

        owner = VehiclesOwners(
            name=name,
            fathers_name=fathers_name,
            surname=surname,
            personal_no=personal_no,
            nationality=nationality,
            date_of_birth=date_of_birth,
            date_of_expiry=date_of_expiry,
            document_number=document_number,
            place_of_birth=place_of_birth,
            residence=residence,
            height=height,
            color_of_eyes=color_of_eyes,
            authority=authority,
            date_of_issue=date_of_issue
        )
        owner.save()
        messages.success(request, "Собственикът на превозно средство е добавен успешно!")
        return redirect("manage_vehicles_owners")

    return render(request, 'admin/add_vehicles_owner.html')

@login_required(login_url='/')
def MANAGE_VEHICLES_OWNERS(request):
    query = request.GET.get('query', '').strip()

    if query:
        owners_list = VehiclesOwners.objects.filter(name__icontains=query) | VehiclesOwners.objects.filter(personal_no__icontains=query)
    else:
        owners_list = VehiclesOwners.objects.all()

    paginator = Paginator(owners_list, 50)
    page_number = request.GET.get('page')

    try:
        owners = paginator.page(page_number)
    except:
        owners = paginator.page(1)

    context = {
        'owners': owners,
        'query': query,
    }

    return render(request, 'admin/manage_vehicles_owners.html', context)

@login_required(login_url='/')
def UPDATE_VEHICLES_OWNER(request, id):
    owner = get_object_or_404(VehiclesOwners, id=id)

    if request.method == 'POST':
        owner.name = request.POST.get('name').strip()
        owner.fathers_name = request.POST.get('fathers_name').strip()
        owner.surname = request.POST.get('surname').strip()
        owner.personal_no = request.POST.get('personal_no').strip()
        owner.nationality = request.POST.get('nationality').strip()
        owner.date_of_birth = request.POST.get('date_of_birth')
        owner.date_of_expiry = request.POST.get('date_of_expiry')
        owner.document_number = request.POST.get('document_number').strip()
        owner.place_of_birth = request.POST.get('place_of_birth').strip()
        owner.residence = request.POST.get('residence').strip()
        owner.height = request.POST.get('height')
        owner.color_of_eyes = request.POST.get('color_of_eyes').strip()
        owner.authority = request.POST.get('authority').strip()
        owner.date_of_issue = request.POST.get('date_of_issue')

        owner.save()
        messages.success(request, "Информацията за собственика е обновена успешно!")
        return redirect('manage_vehicles_owners')

    context = {
        'owner': owner
    }
    return render(request, 'admin/update_vehicles_owners.html', context)

@login_required(login_url='/')
def DELETE_VEHICLES_OWNER(request, id):
    owner = VehiclesOwners.objects.get(id=id)
    owner.delete()
    messages.success(request, "Собственикът на превозно средство е изтрит успешно!")
    return redirect('manage_vehicles_owners')




@login_required(login_url='/')
def SEARCH_VEHICLES_OWNERS_AJAX(request):
    query = request.GET.get('query', '').strip()

    if query:
        owners = VehiclesOwners.objects.filter(
            Q(name__icontains=query) |
            Q(fathers_name__icontains=query) |
            Q(surname__icontains=query) |
            Q(personal_no__icontains=query) |
            Q(nationality__icontains=query) |
            Q(document_number__icontains=query) |
            Q(place_of_birth__icontains=query) |
            Q(residence__icontains=query) |
            Q(color_of_eyes__icontains=query) |
            Q(authority__icontains=query)
        ).values('id', 'name', 'surname', 'personal_no')[:10]

        return JsonResponse(list(owners), safe=False)

    return JsonResponse([], safe=False)




@login_required(login_url='/')
def ADD_VEHICLES_LICENSE(request):
    if request.method == "POST":
        document_number = request.POST.get('document_number')
        date_of_issue = request.POST.get('date_of_issue')
        date_of_expiry = request.POST.get('date_of_expiry')
        authority = request.POST.get('authority')

        # Категории
        category_fields = [
            "AM_DATE", "A1_DATE", "A2_DATE", "A_DATE", "B1_DATE", "B_DATE",
            "C1_DATE", "C_DATE", "D1_DATE", "D_DATE", "BE_DATE", "C1E_DATE",
            "CE_DATE", "D1E_DATE", "DE_DATE", "TTM_DATE", "TKT_DATE"
        ]
        category_data = {field: request.POST.get(field) for field in category_fields}

        if VehiclesLicenses.objects.filter(document_number=document_number).exists():
            messages.error(request, "Свидетелство с този документен номер вече съществува!")
            return redirect("add_vehicles_license")

        license = VehiclesLicenses(
            document_number=document_number,
            date_of_issue=date_of_issue,
            date_of_expiry=date_of_expiry,
            authority=authority,
            **category_data
        )
        license.save()
        messages.success(request, "Свидетелството е добавено успешно!")
        return redirect("manage_vehicles_licenses")

    return render(request, 'admin/add_vehicles_license.html')

@login_required(login_url='/')
def MANAGE_VEHICLES_LICENSES(request):
    query = request.GET.get('query', '').strip()

    if query:
        licenses_list = VehiclesLicenses.objects.filter(document_number__icontains=query)
    else:
        licenses_list = VehiclesLicenses.objects.all()

    paginator = Paginator(licenses_list, 10)
    page_number = request.GET.get('page')

    try:
        licenses = paginator.page(page_number)
    except:
        licenses = paginator.page(1)

    context = {'licenses': licenses, 'query': query}
    return render(request, 'admin/manage_vehicles_licenses.html', context)



@login_required(login_url='/')
def UPDATE_VEHICLES_LICENSE(request, id):
    license = get_object_or_404(VehiclesLicenses, id=id)

    if request.method == 'POST':
        license.document_number = request.POST.get('document_number')
        license.date_of_issue = request.POST.get('date_of_issue')
        license.date_of_expiry = request.POST.get('date_of_expiry')
        license.authority = request.POST.get('authority')

        category_fields = [
            "AM_DATE", "A1_DATE", "A2_DATE", "A_DATE", "B1_DATE", "B_DATE",
            "C1_DATE", "C_DATE", "D1_DATE", "D_DATE", "BE_DATE", "C1E_DATE",
            "CE_DATE", "D1E_DATE", "DE_DATE", "TTM_DATE", "TKT_DATE"
        ]

        for field in category_fields:
            value = request.POST.get(field)
            setattr(license, field, value if value else None)  # Ако е празно, запазва None

        try:
            license.save()
            messages.success(request, "Свидетелството е обновено успешно!")
            return redirect('manage_vehicles_licenses')
        except ValidationError as e:
            messages.error(request, f"Грешка при запис: {e}")
    
    context = {'license': license}
    return render(request, 'admin/update_vehicles_license.html', context)




@login_required(login_url='/')
def DELETE_VEHICLES_LICENSE(request, id):
    license = get_object_or_404(VehiclesLicenses, id=id)
    license.delete()
    messages.success(request, "Свидетелството е изтрито успешно!")
    return redirect('manage_vehicles_licenses')

@login_required(login_url='/')
def SEARCH_VEHICLES_LICENSES_AJAX(request):
    query = request.GET.get('query', '').strip()
    if query:
        licenses = VehiclesLicenses.objects.filter(document_number__icontains=query).values('id', 'document_number')[:10]
        return JsonResponse(list(licenses), safe=False)
    return JsonResponse([], safe=False)
















from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from cmsapp.models import Vehicles, VehicleType, VehiclesOwners, InsuranceTable, VignetteTable

@login_required(login_url='/')
def ADD_VEHICLE(request):
    if request.method == "POST":
        A = request.POST.get('A')
        D = request.POST.get('D')
        owner_id = request.POST.get('owner_id')
        valid_insurance = request.POST.get('valid_insurance', False)
        insurance_id = request.POST.get('insurance_id')
        valid_vignette = request.POST.get('valid_vignette', False)
        vignette_id = request.POST.get('vignette_id')

        if Vehicles.objects.filter(A=A).exists():
            messages.error(request, "Превозно средство с този регистрационен номер вече съществува!")
            return redirect("add_vehicle")

        vehicle = Vehicles(
            A=A,
            D=VehicleType.objects.get(id=D),
            owner=VehiclesOwners.objects.get(id=owner_id),
            valid_insurance=bool(valid_insurance),
            insurance=InsuranceTable.objects.get(id=insurance_id) if insurance_id else None,
            valid_vignette=bool(valid_vignette),
            vignette=VignetteTable.objects.get(id=vignette_id) if vignette_id else None
        )
        vehicle.save()
        messages.success(request, "Превозното средство е добавено успешно!")
        return redirect("manage_vehicles")

    vehicle_types = VehicleType.objects.all()
    owners = VehiclesOwners.objects.all()
    insurances = InsuranceTable.objects.all()
    vignettes = VignetteTable.objects.all()

    return render(request, 'admin/add_vehicle.html', {
        'vehicle_types': vehicle_types,
        'owners': owners,
        'insurances': insurances,
        'vignettes': vignettes
    })


@login_required(login_url='/')
def MANAGE_VEHICLES(request):
    query = request.GET.get('query', '').strip()
    
    vehicles_list = Vehicles.objects.select_related('owner').all()
    
    if query:
        vehicles_list = vehicles_list.filter(
            Q(A__icontains=query) |
            Q(owner__personal_no__icontains=query)
        )
    
    paginator = Paginator(vehicles_list, 10)
    page_number = request.GET.get('page')

    try:
        vehicles = paginator.page(page_number)
    except:
        vehicles = paginator.page(1)

    return render(request, 'admin/manage_vehicles.html', {
        'vehicles': vehicles,
        'query': query
    })



@login_required(login_url='/')
def UPDATE_VEHICLE(request, id):
    vehicle = get_object_or_404(Vehicles, id=id)

    if request.method == 'POST':
        vehicle.A = request.POST.get('A')
        vehicle.D = VehicleType.objects.get(id=request.POST.get('D'))
        vehicle.owner = VehiclesOwners.objects.get(id=request.POST.get('owner_id'))
        vehicle.valid_insurance = bool(request.POST.get('valid_insurance'))
        vehicle.insurance = InsuranceTable.objects.get(id=request.POST.get('insurance_id')) if request.POST.get('insurance_id') else None
        vehicle.valid_vignette = bool(request.POST.get('valid_vignette'))
        vehicle.vignette = VignetteTable.objects.get(id=request.POST.get('vignette_id')) if request.POST.get('vignette_id') else None

        vehicle.save()
        messages.success(request, "Превозното средство е обновено успешно!")
        return redirect('manage_vehicles')

    return render(request, 'admin/update_vehicle.html', {'vehicle': vehicle})


@login_required(login_url='/')
def DELETE_VEHICLE(request, id):
    vehicle = get_object_or_404(Vehicles, id=id)
    vehicle.delete()
    messages.success(request, "Превозното средство е изтрито успешно!")
    return redirect('manage_vehicles')


@login_required(login_url='/')
def SEARCH_VEHICLES_AJAX(request):
    query = request.GET.get('query', '').strip()
    if query:
        vehicles = Vehicles.objects.select_related('owner').filter(
            Q(A__icontains=query) |
            Q(owner__personal_no__icontains=query)
        ).values(
            'id', 
            'A', 
            'owner__personal_no'
        )[:10]

        results = []
        for vehicle in vehicles:
            results.append({
                'registration_number': vehicle['A'],
                'owner_personal_no': vehicle['owner__personal_no']
            })

        return JsonResponse(results, safe=False)
    
    return JsonResponse([], safe=False)




###################################################################
@login_required(login_url='/')
def ADD_VIGNETTE(request):
    if request.method == "POST":
        mps_id = request.POST.get('mps_id')
        issue_date = request.POST.get('issue_date')
        valid_from = request.POST.get('valid_from')
        valid_to = request.POST.get('valid_to')

        if not mps_id or not issue_date or not valid_from or not valid_to:
            messages.error(request, "Моля, попълнете всички полета!")
            return redirect('add_vignette')

        VignetteTable.objects.create(
            mps=Vehicles.objects.get(id=mps_id),
            issue_date=issue_date,
            valid_from=valid_from,
            valid_to=valid_to
        )
        messages.success(request, "Винетката е добавена успешно!")
        return redirect('manage_vignettes')

    return render(request, 'admin/add_vignette.html')


@login_required(login_url='/')
def MANAGE_VIGNETTES(request):
    query = request.GET.get('query', '').strip()
    
    vignettes_list = VignetteTable.objects.select_related('mps').all()
    
    if query:
        vignettes_list = vignettes_list.filter(
            mps__A__icontains=query
        )
    
    paginator = Paginator(vignettes_list, 10)
    page_number = request.GET.get('page')

    try:
        vignettes = paginator.page(page_number)
    except:
        vignettes = paginator.page(1)

    return render(request, 'admin/manage_vignettes.html', {
        'vignettes': vignettes,
        'query': query
    })


@login_required(login_url='/')
def UPDATE_VIGNETTE(request, id):
    vignette = get_object_or_404(VignetteTable, id=id)

    if request.method == "POST":
        mps_id = request.POST.get('mps_id')
        issue_date = request.POST.get('issue_date')
        valid_from = request.POST.get('valid_from')
        valid_to = request.POST.get('valid_to')

        if not mps_id or not issue_date or not valid_from or not valid_to:
            messages.error(request, "Моля, попълнете всички полета!")
            return redirect('update_vignette', id=id)

        vignette.mps = Vehicles.objects.get(id=mps_id)
        vignette.issue_date = issue_date
        vignette.valid_from = valid_from
        vignette.valid_to = valid_to
        vignette.save()

        messages.success(request, "Винетката е обновена успешно!")
        return redirect('manage_vignettes')

    return render(request, 'admin/update_vignette.html', {
        'vignette': vignette
    })



@login_required(login_url='/')
def DELETE_VIGNETTE(request, id):
    vignette = get_object_or_404(VignetteTable, id=id)
    vignette.delete()
    messages.success(request, "Винетката е изтрита успешно!")
    return redirect('manage_vignettes')

@login_required(login_url='/')
def SEARCH_VIGNETTES_AJAX(request):
    query = request.GET.get('query', '').strip()
    if query:
        vignettes = VignetteTable.objects.select_related('mps').filter(
            mps__A__icontains=query
        ).values(
            'id',
            'mps__A',
            'valid_to'
        )[:10]

        results = []
        for vignette in vignettes:
            results.append({
                'id': vignette['id'],
                'registration_number': vignette['mps__A'],
                'valid_to': vignette['valid_to']
            })

        return JsonResponse(results, safe=False)

    return JsonResponse([], safe=False)





@login_required(login_url='/')
def SEARCH_VEHICLES_FOR_VIGNETTE_AJAX(request):
    query = request.GET.get('query', '').strip()
    if query:
        vehicles = Vehicles.objects.select_related('owner').filter(
            A__icontains=query
        ).values(
            'id', 
            'A',
            'owner__name'
        )[:10]

        results = []
        for vehicle in vehicles:
            results.append({
                'id': vehicle['id'],
                'registration_number': vehicle['A'],
                'owner_name': vehicle['owner__name']
            })

        return JsonResponse(results, safe=False)

    return JsonResponse([], safe=False)





##########################################################################################################


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from cmsapp.models import Vehicles, InsuranceTable


@login_required(login_url='/')
def ADD_INSURANCE(request):
    if request.method == "POST":
        mps_id = request.POST.get('mps_id')
        insurance_policy = request.POST.get('insurance_policy')
        sticker_number = request.POST.get('sticker_number')
        issue_date = request.POST.get('issue_date')
        valid_from = request.POST.get('valid_from')
        valid_to = request.POST.get('valid_to')
        issue_place = request.POST.get('issue_place')
        insurer = request.POST.get('insurer')

        if not all([mps_id, insurance_policy, sticker_number, issue_date, valid_from, valid_to, issue_place, insurer]):
            messages.error(request, "Моля, попълнете всички полета!")
            return redirect('add_insurance')

        InsuranceTable.objects.create(
            mps=Vehicles.objects.get(id=mps_id),
            insurance_policy=insurance_policy,
            sticker_number=sticker_number,
            issue_date=issue_date,
            valid_from=valid_from,
            valid_to=valid_to,
            issue_place=issue_place,
            insurer=insurer
        )
        messages.success(request, "Застраховката е добавена успешно!")
        return redirect('manage_insurances')

    return render(request, 'admin/add_insurance.html')



@login_required(login_url='/')
def MANAGE_INSURANCES(request):
    query = request.GET.get('query', '').strip()

    insurances_list = InsuranceTable.objects.select_related('mps').all()

    if query:
        insurances_list = insurances_list.filter(
            mps__A__icontains=query
        )

    paginator = Paginator(insurances_list, 10)
    page_number = request.GET.get('page')

    try:
        insurances = paginator.page(page_number)
    except:
        insurances = paginator.page(1)

    return render(request, 'admin/manage_insurances.html', {
        'insurances': insurances,
        'query': query
    })


@login_required(login_url='/')
def UPDATE_INSURANCE(request, id):
    insurance = get_object_or_404(InsuranceTable, id=id)

    if request.method == "POST":
        mps_id = request.POST.get('mps_id')
        insurance_policy = request.POST.get('insurance_policy')
        sticker_number = request.POST.get('sticker_number')
        issue_date = request.POST.get('issue_date')
        valid_from = request.POST.get('valid_from')
        valid_to = request.POST.get('valid_to')
        issue_place = request.POST.get('issue_place')
        insurer = request.POST.get('insurer')

        if not all([mps_id, insurance_policy, sticker_number, issue_date, valid_from, valid_to, issue_place, insurer]):
            messages.error(request, "Моля, попълнете всички полета!")
            return redirect('update_insurance', id=id)

        insurance.mps = Vehicles.objects.get(id=mps_id)
        insurance.insurance_policy = insurance_policy
        insurance.sticker_number = sticker_number
        insurance.issue_date = issue_date
        insurance.valid_from = valid_from
        insurance.valid_to = valid_to
        insurance.issue_place = issue_place
        insurance.insurer = insurer
        insurance.save()

        messages.success(request, "Застраховката е обновена успешно!")
        return redirect('manage_insurances')

    return render(request, 'admin/update_insurance.html', {
        'insurance': insurance
    })



@login_required(login_url='/')
def DELETE_INSURANCE(request, id):
    insurance = get_object_or_404(InsuranceTable, id=id)
    insurance.delete()
    messages.success(request, "Застраховката е изтрита успешно!")
    return redirect('manage_insurances')


@login_required(login_url='/')
def SEARCH_INSURANCES_AJAX(request):
    query = request.GET.get('query', '').strip()
    if query:
        insurances = InsuranceTable.objects.select_related('mps').filter(
            mps__A__icontains=query
        ).values(
            'id',
            'mps__A',
            'valid_to'
        )[:10]

        results = []
        for insurance in insurances:
            results.append({
                'id': insurance['id'],
                'registration_number': insurance['mps__A'],
                'valid_to': insurance['valid_to']
            })

        return JsonResponse(results, safe=False)

    return JsonResponse([], safe=False)


@login_required(login_url='/')
def SEARCH_VEHICLES_FOR_INSURANCE_AJAX(request):
    query = request.GET.get('query', '').strip()
    if query:
        vehicles = Vehicles.objects.select_related('owner').filter(
            A__icontains=query
        ).values(
            'id',
            'A',
            'owner__name'
        )[:10]

        results = []
        for vehicle in vehicles:
            results.append({
                'id': vehicle['id'],
                'registration_number': vehicle['A'],
                'owner_name': vehicle['owner__name']
            })

        return JsonResponse(results, safe=False)

    return JsonResponse([], safe=False)





################################################################################



from cmsapp.models import CustomUser, City, Street, TrafficFine, Vehicles
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def ADD_TRAFFIC_FINE(request):
    if request.method == "POST":
        mps_id = request.POST.get('mps_id')
        officer_id = request.POST.get('officer_id')
        violation_datetime = request.POST.get('violation_datetime')
        violation_text = request.POST.get('violation_text')
        fine_amount = request.POST.get('fine_amount')
        city_id = request.POST.get('city_id')
        street_id = request.POST.get('street_id')

        TrafficFine.objects.create(
            mps=Vehicles.objects.get(id=mps_id),
            officer=CustomUser.objects.get(id=officer_id),
            violation_datetime=violation_datetime,
            violation_text=violation_text,
            fine_amount=fine_amount,
            city=City.objects.get(id=city_id),
            street=Street.objects.get(id=street_id)
        )
        messages.success(request, "Фишът е добавен успешно!")
        return redirect('manage_traffic_fines')

    officers = CustomUser.objects.filter(user_type='3')
    cities = City.objects.all()
    streets = Street.objects.all()

    return render(request, 'admin/add_traffic_fine.html', {
        'officers': officers,
        'cities': cities,
        'streets': streets
    })


@login_required(login_url='/')
def MANAGE_TRAFFIC_FINES(request):
    query = request.GET.get('query', '').strip()
    fines_list = TrafficFine.objects.select_related('mps').all()
    
    if query:
        fines_list = fines_list.filter(
            mps__A__icontains=query
        )
    
    paginator = Paginator(fines_list, 10)
    page_number = request.GET.get('page')

    fines = paginator.get_page(page_number)

    return render(request, 'admin/manage_traffic_fines.html', {
        'fines': fines,
        'query': query
    })


@login_required(login_url='/')
def UPDATE_TRAFFIC_FINE(request, id):
    fine = get_object_or_404(TrafficFine, id=id)

    if request.method == "POST":
        fine.mps = Vehicles.objects.get(id=request.POST.get('mps_id'))
        fine.officer = CustomUser.objects.get(id=request.POST.get('officer_id'))
        fine.violation_datetime = request.POST.get('violation_datetime')
        fine.violation_text = request.POST.get('violation_text')
        fine.fine_amount = request.POST.get('fine_amount')
        fine.city_id = request.POST.get('city_id')
        fine.street_id = request.POST.get('street_id')
        fine.type_id = request.POST.get('type_id')  # ✅ Добавено за запазване на type_id
        fine.save()

        messages.success(request, "Фишът е обновен успешно!")
        return redirect('manage_traffic_fines')

    officers = CustomUser.objects.filter(user_type='3')

    return render(request, 'admin/update_traffic_fine.html', {
        'fine': fine,
        'officers': officers
    })


@login_required(login_url='/')
def DELETE_TRAFFIC_FINE(request, id):
    fine = get_object_or_404(TrafficFine, id=id)
    fine.delete()
    messages.success(request, "Фишът е изтрит успешно!")
    return redirect('manage_traffic_fines')


@login_required(login_url='/')
def SEARCH_TRAFFIC_FINE_AJAX(request):
    query = request.GET.get('query', '').strip()
    if query:
        fines = TrafficFine.objects.select_related('mps').filter(
            mps__A__icontains=query
        ).values(
            'id',
            'mps__A',
            'fine_amount'
        )[:10]

        results = [{'id': fine['id'], 'registration_number': fine['mps__A'], 'fine_amount': str(fine['fine_amount'])} for fine in fines]
        return JsonResponse(results, safe=False)

    return JsonResponse([], safe=False)


@login_required(login_url='/')
def SEARCH_VEHICLES_FOR_TRAFFIC_FINE_AJAX(request):
    query = request.GET.get('query', '').strip()
    if query:
        vehicles = Vehicles.objects.select_related('owner').filter(
            A__icontains=query
        ).values(
            'id',
            'A',
            'owner__name'
        )[:10]

        results = [{'id': vehicle['id'], 'registration_number': vehicle['A'], 'owner_name': vehicle['owner__name']} for vehicle in vehicles]
        return JsonResponse(results, safe=False)

    return JsonResponse([], safe=False)




from cmsapp.models import City

@login_required(login_url='/')
def SEARCH_CITIES_AJAX(request):
    query = request.GET.get('query', '').strip()
    if query:
        cities = City.objects.filter(
            city_name__icontains=query
        ).values(
            'id', 'city_name'
        )[:10]

        results = [{'id': city['id'], 'city_name': city['city_name']} for city in cities]
        return JsonResponse(results, safe=False)

    return JsonResponse([], safe=False)


from cmsapp.models import Street

@login_required(login_url='/')
def SEARCH_STREETS_AJAX(request):
    city_id = request.GET.get('city_id')
    if city_id:
        streets = Street.objects.filter(city_id_id=city_id).values('id', 'street_name')
        return JsonResponse(list(streets), safe=False)
    return JsonResponse([], safe=False)










#### ПОДДРЪЖКА #####
from django.core.management import call_command

def generate_er_diagram(request):
    diagram_path = os.path.join(settings.MEDIA_ROOT, 'er_diagram.png')

    # Генериране на ER диаграмата в реално време
    try:
        call_command('graph_models', '-a', '-o', diagram_path)
    except Exception as e:
        messages.error(request, f"Грешка при генерирането: {e}")
        return render(request, 'admin/er_diagram.html', {'error': 'Неуспешно генериране на диаграмата.'})

    return render(request, 'admin/er_diagram.html', {
        'diagram_url': settings.MEDIA_URL + 'er_diagram.png'
    })



import os
import subprocess
import datetime
import zipfile
from django.conf import settings
from django.shortcuts import render


def backup_database(request):
    backup_file = None

    if request.method == 'POST':
        now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        sql_filename = f"backup_{now}.sql"
        sql_filepath = os.path.join(settings.MEDIA_ROOT, sql_filename)

        zip_filename = f"backup_{now}.zip"
        zip_filepath = os.path.join(settings.MEDIA_ROOT, zip_filename)

        try:
            # Генериране на SQL бекъп
            command = f"mysqldump -u {settings.DATABASES['default']['USER']} -p'{settings.DATABASES['default']['PASSWORD']}' {settings.DATABASES['default']['NAME']} > {sql_filepath}"
            subprocess.run(command, shell=True, check=True)

            # Архивиране в ZIP
            with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(sql_filepath, arcname=sql_filename)

            # Изтриване на .sql файла след архивиране
            os.remove(sql_filepath)

            backup_file = settings.MEDIA_URL + zip_filename

        except Exception as e:
            return render(request, 'admin/backup.html', {'error': f'Грешка при създаване на бекъп: {e}'})

    return render(request, 'admin/backup.html', {'backup_file': backup_file})







##### АНАЛИЗИ #####

from django.shortcuts import render
from django.db.models import Count
from django.utils.timezone import now, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import io
import urllib, base64
from cmsapp.models import Complaints, City

def geographic_analysis(request):
    # ✅ Четене на GET параметри от заявката
    filter_period = request.GET.get('filter_period', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    # ✅ Изчисляване на датите на база избрания период
    filter_message = "Всички налични данни"  # По подразбиране
    today = now().date()
    
    if filter_period:
        if filter_period == "1d":
            start_date = today - timedelta(days=1)
            end_date = today
            filter_message = "Последните 24 часа"
        elif filter_period == "1w":
            start_date = today - timedelta(weeks=1)
            end_date = today
            filter_message = "Последната седмица"
        elif filter_period == "1m":
            start_date = today - timedelta(weeks=4)
            end_date = today
            filter_message = "Последния месец"
        elif filter_period == "3m":
            start_date = today - timedelta(weeks=12)
            end_date = today
            filter_message = "Последните 3 месеца"
        elif filter_period == "6m":
            start_date = today - timedelta(weeks=24)
            end_date = today
            filter_message = "Последните 6 месеца"
        elif filter_period == "12m":
            start_date = today - timedelta(weeks=52)
            end_date = today
            filter_message = "Последните 12 месеца"
        elif filter_period == "24m":
            start_date = today - timedelta(weeks=104)
            end_date = today
            filter_message = "Последните 24 месеца"
    
    # ✅ Ако потребителят ръчно избере дати
    elif start_date and end_date:
        filter_message = f"Данни от {start_date} до {end_date}"
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

    # ✅ Филтриране на жалбите според избраните дати
    complaints_query = Complaints.objects.values('city_id').annotate(total=Count('id'))
    
    if start_date and end_date:
        complaints_query = complaints_query.filter(complaintdate_at__range=[start_date, end_date])

    # ✅ Проверка дали има резултати
    if not complaints_query.exists():
        return render(request, 'admin/geographic_analysis.html', {'error': "Няма достатъчно данни за анализ."})

    # ✅ Връзка градове -> имена
    city_map = {city.id: city.city_name for city in City.objects.all()}
    city_list = [{'city_name': city_map.get(entry['city_id'], 'Неизвестен град'), 'total': entry['total']} for entry in complaints_query]

    # ✅ Преобразуване в Pandas DataFrame
    df = pd.DataFrame(city_list)

    if df.empty:
        return render(request, 'admin/geographic_analysis.html', {'error': "Няма налични сигнали."})

    # ✅ Генериране на графика
    plt.figure(figsize=(12, 6))
    plt.barh(df['city_name'], df['total'], color='#d8d8d8')  # 🌈 Променен цвят
    plt.xlabel("Брой сигнали")
    plt.ylabel("Град")
    plt.title("Географски анализ на сигналите")
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.gca().invert_yaxis()  # 🔄 Обръщане на реда за по-добра четимост

    # ✅ Запазване на графиката в паметта
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches="tight")  # 📏 bbox_inches предотвратява отрязване на текст
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    # ✅ Конвертиране в base64 формат за HTML
    graphic = base64.b64encode(image_png).decode('utf-8')

    # ✅ Предаване на графиката и съобщението към шаблона
    return render(request, 'admin/geographic_analysis.html', {
        'graphic': graphic,
        'filter_message': filter_message,
        'start_date': request.GET.get('start_date', ''),
        'end_date': request.GET.get('end_date', ''),
        'filter_period': filter_period
    })
