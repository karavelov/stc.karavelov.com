from django.shortcuts import render,redirect,HttpResponse
from cmsapp.EmailBackEnd import EmailBackEnd
from django.contrib.auth import  logout,login
from django.contrib import messages
from cmsapp.models import CustomUser,UserReg,Complaints
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
import bcrypt
from django.contrib.auth import update_session_auth_hash



User = get_user_model()

from django.contrib.auth.decorators import login_required

def BASE(request):
       return render(request,'base.html')




def LOGIN(request):
    return render(request,'login.html')

def notifications(request):
    complaints1 = Complaints.objects.all()
    newcom_count1 = Complaints.objects.filter(status='0').count() 
    context = {
    'newcom_count1':newcom_count1,
    'complaints1':complaints1        
    }
    return render(request, 'includes/header.html', context)



def doLogout(request):
    logout(request)
    request.session.flush()  # Clear the session including CSRF token
    return redirect('login')



def doLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(f"🔍 Опит за логин с: {email}")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            print(f"✅ Успешен логин за: {user.email}, Тип: {user.user_type}")
            user_type = int(user.user_type)

            # Проверка дали user_type е валиден
            if user_type in [1, 2, 3]:
                login(request, user)

                if user_type == 1:
                    return redirect('admin_home')
                elif user_type == 2:
                    return redirect('user_home')
                elif us.user_type == 3:
                    return redirect('police_home')

            # ⚠️ Ако user_type не е валиден, връщаме грешка
            print("❌ Грешка: Непознат user_type! Проверете базата данни.")
            messages.error(request, "Грешка в системата. Свържете се с администратора.")
            return redirect('login')  # ✅ Добавен return тук!

        else:
            print("❌ Грешна парола или несъществуващ потребител!")
            messages.error(request, 'Вашият имейл или парола са грешни')
            return redirect('login')  # ✅ Гарантирано HttpResponse

    messages.error(request, 'Невалиден метод')
    return redirect('login')  # ✅ Връща HttpResponse и за GET заявки







login_required(login_url='/')
def PROFILE(request):
    user = CustomUser.objects.get(id = request.user.id)
    context = {
        "user":user,
    }
    return render(request,'profile.html',context)



@login_required(login_url='/')
def PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name

            if profile_pic:
                customuser.profile_pic = profile_pic

            customuser.save()
            messages.success(request, "Вашият профил беше успешно обновен!")
            return redirect('profile')

        except:
            messages.error(request, "Грешка при обновяване на профила!")
    return render(request, 'profile.html')



def CHANGE_PASSWORD(request):
    context = {}

    try:
        user = User.objects.get(id=request.user.id)
        context["data"] = user
    except User.DoesNotExist:
        messages.error(request, "Грешка: Потребителят не е намерен.")
        return redirect("change_password")

    if request.method == "POST":
        current = request.POST.get("cpwd", "")
        new_pas = request.POST.get("npwd", "")

        print(f"🔍 Опит за смяна на парола от {user.email}")
        print(f"🔑 Въведена текуща парола: {current}")
        print(f"🔑 Запазен хеш: {user.password}")

        # Проверяваме дали старата парола е правилна
        if bcrypt.checkpw(current.encode("utf-8"), user.password.encode("utf-8")):
            print("✅ Старата парола е вярна!")

            # Генерираме bcrypt хеш за новата парола
            hashed_new_password = bcrypt.hashpw(new_pas.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            # Записваме новата парола
            user.password = hashed_new_password
            user.save()

            # Обновяваме сесията, за да не разлогне потребителя
            update_session_auth_hash(request, user)

            print("✅ Паролата е сменена успешно!")
            messages.success(request, "Успешна промяна на парола!")
            return redirect("profile")  # ✅ Пренасочване към профила

        else:
            print("❌ Грешна стара парола!")
            messages.error(request, "Текущата парола е грешна!")
            return redirect("change_password")

    return render(request, "change-password.html", context)


@login_required(login_url='/')
def EDIT_USER(request, id):
    user = get_object_or_404(UserReg.objects.select_related('admin'), id=id)

    if request.method == 'POST':
        user.admin.first_name = request.POST.get('first_name', user.admin.first_name)
        user.admin.last_name = request.POST.get('last_name', user.admin.last_name)
        user.admin.email = request.POST.get('email', user.admin.email)
        user.mobilenumber = request.POST.get('mobilenumber', user.mobilenumber)

        if 'profile_pic' in request.FILES:
            user.admin.profile_pic = request.FILES['profile_pic']

        user.admin.save()
        user.save()

        messages.success(request, "Потребителят е успешно редактиран!")
        return redirect('manageusers')

    context = {
        'user': user
    }
    return render(request, 'admin/edit_user.html', context)




