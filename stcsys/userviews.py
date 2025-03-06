from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required

from cmsapp.models import CustomUser,UserReg,Category,Subcategory,Region,Type_Traffic_Lights,Complaints,ComplaintRemark,City,Street
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
from django.core.files.images import get_image_dimensions
from django.conf import settings





@login_required(login_url='/')

def USERHOME(request):
    user_admin = request.user
    user_reg = UserReg.objects.get(admin=user_admin)
    complaints_count = Complaints.objects.filter(userregid=user_reg).count
    newcom_count = Complaints.objects.filter(status='0',userregid=user_reg).count()
    ipcom_count = Complaints.objects.filter(status='Inprocess',userregid=user_reg).count()
    closed_count = Complaints.objects.filter(status='Closed',userregid=user_reg).count()
    context = {
    'complaints_count':complaints_count,
    'newcom_count':newcom_count,
    'ipcom_count':ipcom_count,
    'closed_count':closed_count,        
    }
    return render(request,'user/userdashboard.html',context)







def USERSIGNUP(request):
    if request.method == "POST":
        #print("🔹 Форма е изпратена!")  # Дебъгване

        pic = request.FILES.get('pic', None)  # НЕ е задължително
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')  # Скрито поле
        email = request.POST.get('email')
        mobno = request.POST.get('mobno')
        password = request.POST.get('password')

        # Проверка за дублиране на имейл
        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Този имейл вече е зает!')
            return redirect('usersignup')

        # Проверка за дублиране на потребителско име
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Това потребителско име вече съществува!')
            return redirect('usersignup')

        # Създаване на нов потребител
        user = CustomUser(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            user_type=2,
            profile_pic=pic if pic else None,  # Ако няма снимка, остава празно
        )
        user.set_password(password)
        user.save()

        # Свързване на UserReg модела
        comuser = UserReg(admin=user, mobilenumber=mobno)
        comuser.save()

        messages.success(request, 'Регистрацията е успешна! Моля, влезте в профила си.')
        return redirect('login')

    return render(request, 'user/user_reg.html')











@login_required(login_url='/')
def get_subcat(request):
    if request.method == 'GET':
        c_id = request.GET.get('c_id')
        # print(f"🔍 Получено cat_id: {c_id}")  # Логваме за дебъгване
        # Филтрираме подкатегориите по избраната категория
        subcat = Subcategory.objects.filter(cat_id=c_id)
        subcat_options = '<option value="">Изберете подкатегория</option>'
        for subcategory in subcat:
            subcat_options += f'<option value="{subcategory.id}">{subcategory.subcatname}</option>'
        
        return JsonResponse({'subcat_options': subcat_options})



@login_required(login_url='/')
def COMPLAINTHISTORY(request):
    userreg = request.user.userreg
    complaint_list = Complaints.objects.filter(userregid=userreg)
    paginator = Paginator(complaint_list, 10)  # Show 10 complaints per page

    page_number = request.GET.get('page')
    try:
        complaints = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        complaints = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        complaints = paginator.page(paginator.num_pages)

    context = {'complaints': complaints}
    return render(request, 'user/complaint-history.html', context)

@login_required(login_url='/')
def COMPLAINTHISTORYDETAILS(request,id):
    complaints = Complaints.objects.get(id=id)
    complaintsremarks = ComplaintRemark.objects.filter(comp_id_id=id)

    context = {
         'complaints':complaints,
         'complaintsremarks':complaintsremarks,
    }
    return render(request,'user/complaint-details.html',context)





@login_required(login_url='/')
def REGCOMPLAINT(request):
    """Регистрация на сигнал"""
    if request.method == "POST":
        cat_id = request.POST.get("cat_id")
        subcategory_id = request.POST.get("subcategory_id")
        city_id = request.POST.get("city_id")
        street_id = request.POST.get("street_id")
        complaindetails = request.POST.get("complaindetails")
        compfile = request.FILES.get("compfile")

        # Проверка дали всички полета са попълнени
        if not cat_id or not subcategory_id or not city_id or not street_id:
            messages.error(request, "Всички полета са задължителни!")
            return redirect("regcomplaint")

        # Проверка дали избраният град и улица съществуват в базата данни
        try:
            city = City.objects.get(id=city_id)
            street = Street.objects.get(id=street_id, city_id=city)  # 👈 Проверка дали улицата принадлежи на града
        except City.DoesNotExist:
            messages.error(request, "Невалиден град!")
            return redirect("regcomplaint")
        except Street.DoesNotExist:
            messages.error(request, "Невалидна улица за този град!")
            return redirect("regcomplaint")

        # Записване на сигнала в базата данни
        complaint = Complaints(
            userregid=request.user.userreg,
            cat_id_id=cat_id,
            subcategory_id_id=subcategory_id,
 city=City.objects.get(id=city_id),  # ✅ Правилно подаване на град
    street=Street.objects.get(id=street_id),  # ✅ Правилно подаване на улица
            complaindetails=complaindetails,
            compfile=compfile,
        )
        complaint.save()

        messages.success(request, "Сигналът е изпратен успешно!")
        return redirect("user_home")

    # Извличане на категории и градове за зареждане във формата
    categories = Category.objects.all()
    cities = City.objects.all()
    return render(request, "user/register-complaint.html", {"categories": categories, "cities": cities})


def get_streets(request):
    """Зарежда улиците за избрания град"""
    city_id = request.GET.get("city_id")
    if city_id:
        streets = Street.objects.filter(city_id=city_id).values("id", "street_name")
        return JsonResponse({"streets": list(streets)})
    return JsonResponse({"streets": []})


def get_subcategories(request):
    """Зарежда подкатегории за избраната категория"""
    cat_id = request.GET.get("cat_id")
    if cat_id:
        subcategories = Subcategory.objects.filter(cat_id=cat_id).values("id", "subcatname")
        return JsonResponse({"subcategories": list(subcategories)})
    return JsonResponse({"subcategories": []})







@login_required(login_url='/')
def POLICEHOME(request):
    user_admin = request.user
    user_reg = UserReg.objects.get(admin=user_admin)
    
    complaints_count = Complaints.objects.filter(userregid=user_reg).count
    newcom_count = Complaints.objects.filter(status='0', userregid=user_reg).count()
    ipcom_count = Complaints.objects.filter(status='Inprocess', userregid=user_reg).count()
    closed_count = Complaints.objects.filter(status='Closed', userregid=user_reg).count()

    context = {
        'complaints_count': complaints_count,
        'newcom_count': newcom_count,
        'ipcom_count': ipcom_count,
        'closed_count': closed_count,        
    }
    return render(request, 'police/policedashboard.html', context)





from cmsapp.models import CustomUser  # ако използваш персонализиран модел
from django.db.models import Q

@login_required(login_url='/')
def police_search(request):
    query = request.GET.get('query', '')
    search_results = []

    if query:
        # Търсим по регистрационен номер или ЕГН
        search_results = CustomUser.objects.filter(
            Q(registration_number__icontains=query) | Q(egn__icontains=query)
        )
        
    return render(request, 'admin/police_search.html', {
        'query': query,
        'search_results': search_results
    })
