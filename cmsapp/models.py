from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import update_session_auth_hash
import bcrypt


import bcrypt
from django.contrib.auth.models import AbstractUser
from django.db import models





class City(models.Model):
    city_name = models.CharField(max_length=200)
    post_code = models.IntegerField(default=0, blank=True, null=True)  # Добавен default
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.city_name
    


class Street(models.Model):
    street_name = models.CharField(max_length=200)
    city_id = models.ForeignKey(City, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.street_name




class Region(models.Model):
    regionname = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.regionname







class ODMVR(models.Model):
    id = models.BigAutoField(primary_key=True)
    odmvr_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.odmvr_name


class PositionOccupied(models.Model):
    position_occupied_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cmsapp_position_occupied"  #Променяме името на таблицата

    def __str__(self):
        return self.position_occupied_name
    





class CustomUser(AbstractUser):
    USER_TYPES = [
        (1, 'admin'),
        (2, 'user'),
        (3, 'police'),
    ]

    user_type = models.IntegerField(choices=USER_TYPES, default=2)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True, default='default.jpg')

    odmvr = models.ForeignKey('cmsapp.ODMVR', on_delete=models.SET_NULL, null=True, blank=True)
    position = models.ForeignKey('cmsapp.PositionOccupied', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.password.startswith("bcrypt$$"):
            self.password = self.password.replace("bcrypt$", "")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username








class UserReg(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="userreg")
    mobilenumber = models.CharField(max_length=11)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)  # 🔥 Важно!
    regdate_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.admin.first_name} {self.admin.last_name} - {self.mobilenumber}"





class Category(models.Model):
    catname = models.CharField(max_length=200)
    catdes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.catname

class Subcategory(models.Model):
    cat_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcatname = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subcatname




class Type_Traffic_Lights(models.Model):
    # полета на модела
    type_traffic_lights_name = models.CharField(max_length=100, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)






class Traffic_Lights(models.Model):
    # полета на модела
    type_traffic_light = models.ForeignKey(Type_Traffic_Lights, on_delete=models.CASCADE) 
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    street = models.ForeignKey(Street, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE) 
    topic = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




class Complaints(models.Model):
    userregid = models.ForeignKey(UserReg, on_delete=models.CASCADE, null=True, blank=True)
    cat_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory_id = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    complaint_number = models.BigIntegerField(unique=True, editable=False)
    complaindetails = models.TextField(blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)  # ✅ Добавяме град
    street = models.ForeignKey(Street, on_delete=models.CASCADE)  # ✅ Добавяме улица
    compfile = models.ImageField(upload_to='media/doc_file', blank=True, null=True)  # Не е задължително
    complaintdate_at = models.DateTimeField(auto_now_add=True)
    remark = models.TextField(blank=True)
    status = models.CharField(max_length=250, default="0")
    updated_at = models.DateTimeField(auto_now=True)
    # Нови полета за географски координати
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    def save(self, *args, **kwargs):

        """Автоматично създаване на уникален complaint_number"""
        if not self.complaint_number:
            last_complaint = Complaints.objects.order_by("-complaint_number").first()
            if last_complaint:
                self.complaint_number = last_complaint.complaint_number + 1
            else:
                self.complaint_number = 100000  # ✅ Започва от голямо число
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Сигнал № {self.complaint_number}"


class ComplaintRemark(models.Model):
    comp_id_id = models.ForeignKey(Complaints, on_delete=models.CASCADE)
    remark = models.TextField(blank=True)
    status = models.CharField(max_length=250,default=0)
    remarkdate = models.DateTimeField(auto_now_add=True)







class VehicleType(models.Model):
    vehicle_type_name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "cmsapp_vehicle_type"  #Променяме името на таблицата

    def __str__(self):
        return self.vehicle_type_name




class VehiclesOwners(models.Model):
    name = models.CharField(max_length=100)
    fathers_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    personal_no = models.CharField(max_length=10, unique=True)
    nationality = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    date_of_expiry = models.DateField()
    document_number = models.CharField(max_length=100)
    place_of_birth = models.CharField(max_length=100)
    residence = models.CharField(max_length=255)  # 🔥 Проверете дали тук пише `residence`, а не `residance`
    height = models.IntegerField()
    color_of_eyes = models.CharField(max_length=50)
    authority = models.CharField(max_length=100)
    date_of_issue = models.DateField()

    class Meta:
        db_table = "cmsapp_vehicles_owners"  #Променяме името на таблицата

    def __str__(self):
        return f"{self.name} {self.surname}"





class VehiclesLicenses(models.Model):
    document_number = models.CharField(max_length=100, unique=True)
    date_of_issue = models.DateField()
    date_of_expiry = models.DateField()
    authority = models.CharField(max_length=255)

    AM_DATE = models.DateField(null=True, blank=True)
    A1_DATE = models.DateField(null=True, blank=True)
    A2_DATE = models.DateField(null=True, blank=True)
    A_DATE = models.DateField(null=True, blank=True)
    B1_DATE = models.DateField(null=True, blank=True)
    B_DATE = models.DateField(null=True, blank=True)
    C1_DATE = models.DateField(null=True, blank=True)
    C_DATE = models.DateField(null=True, blank=True)
    D1_DATE = models.DateField(null=True, blank=True)
    D_DATE = models.DateField(null=True, blank=True)
    BE_DATE = models.DateField(null=True, blank=True)
    C1E_DATE = models.DateField(null=True, blank=True)
    CE_DATE = models.DateField(null=True, blank=True)
    D1E_DATE = models.DateField(null=True, blank=True)
    DE_DATE = models.DateField(null=True, blank=True)
    TTM_DATE = models.DateField(null=True, blank=True)
    TKT_DATE = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cmsapp_vehicles_licenses"

    def __str__(self):
        return f"License {self.document_number}"





class InsuranceTable(models.Model):
    id = models.BigAutoField(primary_key=True)
    mps = models.OneToOneField(
        "cmsapp.Vehicles",
        on_delete=models.CASCADE,
        unique=True
    )
    insurance_policy = models.CharField(max_length=50, unique=True)
    sticker_number = models.CharField(max_length=50, unique=True)
    issue_date = models.DateField()
    valid_from = models.DateField()
    valid_to = models.DateField()
    issue_place = models.CharField(max_length=255)
    insurer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cmsapp_insurance"

    def __str__(self):
        return f"Застраховка {self.insurance_policy} за {self.mps.A}"






class VignetteTable(models.Model):
    id = models.BigAutoField(primary_key=True)
    mps = models.OneToOneField(
        "cmsapp.Vehicles",
        on_delete=models.CASCADE
    )
    issue_date = models.DateField()
    valid_from = models.DateField()
    valid_to = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cmsapp_vignette"

    def __str__(self):
        return f"Винетка за {self.mps.A} (валидна до {self.valid_to})"






class Vehicles(models.Model):
    A = models.CharField(max_length=50, null=True, blank=True)  # Рег. номер
    # Референция към `cmsapp_vehicle_type`
    D = models.ForeignKey(VehicleType, on_delete=models.CASCADE)  # Вид на превозното средство
    K = models.CharField(max_length=50, blank=True, null=True)
    

    D2 = models.CharField(max_length=100, blank=True, null=True)
    R = models.CharField(max_length=50, blank=True, null=True)
    F1 = models.IntegerField(blank=True, null=True)
    F2 = models.IntegerField(blank=True, null=True)
    N1 = models.IntegerField(blank=True, null=True)
    P1 = models.IntegerField(blank=True, null=True)
    S1 = models.CharField(max_length=10, blank=True, null=True)
    T = models.IntegerField(blank=True, null=True)
    V1 = models.CharField(max_length=50, blank=True, null=True)
    V5 = models.CharField(max_length=50, blank=True, null=True)
    E = models.CharField(max_length=50, unique=True)  # Уникален номер
    P5 = models.CharField(max_length=50, blank=True, null=True)
    D1 = models.CharField(max_length=100, blank=True, null=True)
    F3 = models.IntegerField(blank=True, null=True)
    N3 = models.CharField(max_length=50, blank=True, null=True)
    P4 = models.IntegerField(blank=True, null=True)
    O1 = models.IntegerField(blank=True, null=True)
    U2 = models.IntegerField(blank=True, null=True)
    V3 = models.CharField(max_length=50, blank=True, null=True)
    V7 = models.IntegerField(blank=True, null=True)
    B = models.DateField(blank=True, null=True)  # Дата на производство
    P3 = models.CharField(max_length=50, blank=True, null=True)
    D3 = models.CharField(max_length=50, blank=True, null=True)
    G = models.IntegerField(blank=True, null=True)
    N4 = models.CharField(max_length=50, blank=True, null=True)
    Q = models.CharField(max_length=50, blank=True, null=True)
    O2 = models.IntegerField(blank=True, null=True)
    U3 = models.IntegerField(blank=True, null=True)
    V4 = models.CharField(max_length=50, blank=True, null=True)
    V8 = models.CharField(max_length=50, blank=True, null=True)
    J = models.CharField(max_length=50, blank=True, null=True)
    N5 = models.CharField(max_length=50, blank=True, null=True)
    L = models.IntegerField(blank=True, null=True)
    M = models.CharField(max_length=50, blank=True, null=True)
    W = models.CharField(max_length=50, blank=True, null=True)
    V9 = models.CharField(max_length=50, blank=True, null=True)

    # Референция към `cmsapp_vehicles_owners`
    owner = models.ForeignKey("cmsapp.VehiclesOwners", on_delete=models.SET_NULL, null=True, related_name="vehicles")

    valid_insurance = models.BooleanField(default=False)
    valid_vignette = models.BooleanField(default=False)

    # Тези таблици все още липсват в базата, така че могат да се добавят по-късно
    insurance = models.ForeignKey("cmsapp.InsuranceTable", on_delete=models.SET_NULL, null=True, blank=True)
    vignette = models.ForeignKey("cmsapp.VignetteTable", on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.A



class TrafficFine(models.Model):
    mps = models.ForeignKey(Vehicles, on_delete=models.CASCADE)
    officer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    violation_datetime = models.DateTimeField()
    violation_text = models.TextField()
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    street = models.ForeignKey(Street, on_delete=models.SET_NULL, null=True, blank=True)
    type_id = models.PositiveSmallIntegerField(choices=((1, 'Фиш'), (2, 'Акт')), default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cmsapp_traffic_fines"

    def __str__(self):
        return f"{self.get_type_id_display()} - {self.mps.A} - {self.violation_datetime.strftime('%d.%m.%Y')}"
