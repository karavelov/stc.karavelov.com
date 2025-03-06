from django.http import JsonResponse
from .models import Category, Subcategory
from django.shortcuts import render, redirect
from cmsapp.models import CustomUser


from .models import Category, Subcategory


def get_categories(request):
    categories = list(Category.objects.values('id', 'catname'))
    return JsonResponse({'categories': categories})

def get_subcategories(request, category_id):
    subcategories = list(Subcategory.objects.filter(cat_id=category_id).values('id', 'subcatname'))
    return JsonResponse({'subcategories': subcategories})




def load_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(cat_id_id=category_id)
    return render(request, 'cmsapp/subcategory_dropdown_list_options.html', {'subcategories': subcategories})




def manage_users(request):
    # Зареждаме CustomUser + UserReg за да имаме достъп до мобилен номер и дата на регистрация
    userlist = CustomUser.objects.select_related("userreg").all()

    return render(request, 'admin/manage_users.html', {'userlist': userlist})