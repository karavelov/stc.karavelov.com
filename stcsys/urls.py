
from django.contrib import admin
from django.urls import path
from cmsapp.views import get_categories, get_subcategories
from django.conf import settings
from django.conf.urls.static import static
from .import views, adminviews, userviews
from . import adminviews
from django.views.decorators.csrf import csrf_exempt



urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.BASE, name='base'),
    path('', views.LOGIN, name='login'),
    path('doLogin', views.doLogin, name='doLogin'),
    path('doLogout', views.doLogout, name='logout'),

     # This is admin panel
    path('Admin/AdminHome', adminviews.ADMINHOME, name='admin_home'),
    path('Admin/AddCategory', adminviews.ADD_CATEGORY, name='add_category'),
    
    
    #path('Admin/ManageCategory', adminviews.MANAGE_CATEGORY, name='manage_category'),
    #path('Admin/DeleteCategory/<str:id>', adminviews.DELETE_CATEGORY, name='delete_category'),
    #path('UpdateCategory/<str:id>', adminviews.UPDATE_CATEGORY, name='update_category'),
    #path('UpdateCategoryDetails', adminviews.UPDATE_CATEGORY_DETAILS, name='update_category_details'),
    #path('SearchCategoriesAjax/', adminviews.SEARCH_CATEGORIES_AJAX, name='search_categories_ajax'),
    

    path('AddCategory', adminviews.ADD_CATEGORY, name='add_category'),
    path('ManageCategory', adminviews.MANAGE_CATEGORY, name='manage_category'),
    path('SearchCategoriesAjax/', adminviews.SEARCH_CATEGORIES_AJAX, name='search_categories_ajax'),
    path('DeleteCategory/<str:id>', adminviews.DELETE_CATEGORY, name='delete_category'),
    path('UpdateCategory/<str:id>', adminviews.UPDATE_CATEGORY, name='update_category'),
    path('UpdateCategoryDetails', adminviews.UPDATE_CATEGORY_DETAILS, name='update_category_details'),



    path('AddSubcategory', adminviews.ADD_SUBCATEGORY, name='add_subcategory'),
    path('ManageSubcategory', adminviews.MANAGE_SUBCATEGORY, name='manage_subcategory'),
    path('SearchSubcategoriesAjax/', adminviews.SEARCH_SUBCATEGORIES_AJAX, name='search_subcategories_ajax'),
    path('DeleteSubcategory/<str:id>', adminviews.DELETE_SUBCATEGORY, name='delete_subcategory'),
    path('UpdateSubcategory/<str:id>', adminviews.UPDATE_SUBCATEGORY, name='update_subcategory'),
    path('UpdateSubcategoryDetails', adminviews.UPDATE_SUBCATEGORY_DETAILS, name='update_subcategory_details'),








    path('AddRegion', adminviews.ADD_REGION, name='add_region'),
    path('ManageRegion', adminviews.MANAGE_REGION, name='manage_region'),
    path('SearchRegionsAjax/', adminviews.SEARCH_REGIONS_AJAX, name='search_regions_ajax'),
    path('DeleteRegion/<str:id>', adminviews.DELETE_REGION, name='delete_region'),
    path('UpdateRegion/<str:id>', adminviews.UPDATE_REGION, name='update_region'),
    path('UpdateRegionDetails', adminviews.UPDATE_REGION_DETAILS, name='update_region_details'),



    path('AddCity', adminviews.ADD_CITY, name='add_city'),
    path('ManageCity', adminviews.MANAGE_CITY, name='manage_city'),
    path('SearchCityAjax/', adminviews.SEARCH_CITY_AJAX, name='search_citys_ajax'),
    path('DeleteCity/<str:id>', adminviews.DELETE_CITY, name='delete_city'),
    path('UpdateCity/<str:id>', adminviews.UPDATE_CITY, name='update_city'),
    path('UpdateCityDetails', adminviews.UPDATE_CITY_DETAILS, name='update_city_details'),

    path('AddStreet', adminviews.ADD_STREET, name='add_street'),
    path('ManageStreet', adminviews.MANAGE_STREET, name='manage_street'),
    path('SearchStreetAjax/', adminviews.SEARCH_STREET_AJAX, name='search_streets_ajax'),
    path('DeleteStreet/<str:id>', adminviews.DELETE_STREET, name='delete_street'),
    path('UpdateStreet/<str:id>', adminviews.UPDATE_STREET, name='update_street'),
    path('UpdateStreetDetails', adminviews.UPDATE_STREET_DETAILS, name='update_street_details'),


    path('AddType_Traffic_Lights', adminviews.ADD_TYPE_TRAFFIC_LIGHTS, name='add_type_traffic_lights'),
    path('ManageType_Traffic_Lights', adminviews.MANAGE_TYPE_TRAFFIC_LIGHTS, name='manage_type_traffic_lights'),
    path('SearchType_Traffic_LightsAjax/', adminviews.SEARCH_TYPE_TRAFFIC_LIGHTS_AJAX, name='search_type_traffic_lights_ajax'),
    path('DeleteType_Traffic_Lights/<str:id>', adminviews.DELETE_TYPE_TRAFFIC_LIGHTS, name='delete_type_traffic_lights'),
    path('UpdateType_Traffic_Lights/<int:id>', adminviews.UPDATE_TYPE_TRAFFIC_LIGHTS, name='update_type_traffic_lights'),
    path('UpdateType_Traffic_LightsDetails', adminviews.UPDATE_TYPE_TRAFFIC_LIGHTS_DETAILS, name='update_type_traffic_lights_details'),

    path('AddTraffic_Lights', adminviews.ADD_TRAFFIC_LIGHTS, name='add_traffic_lights'),
    path('ManageTraffic_Lights', adminviews.MANAGE_TRAFFIC_LIGHTS, name='manage_traffic_lights'),
    path('SearchTraffic_LightsAjax/', adminviews.SEARCH_TRAFFIC_LIGHTS_AJAX, name='search_traffic_lights_ajax'),
    path('DeleteTraffic_Lights/<str:id>', adminviews.DELETE_TRAFFIC_LIGHTS, name='delete_traffic_lights'),
    path('UpdateTraffic_Lights/<int:id>', adminviews.UPDATE_TRAFFIC_LIGHTS, name='update_traffic_lights'),
    path('UpdateTraffic_LightsDetails', adminviews.UPDATE_TRAFFIC_LIGHTS_DETAILS, name='update_traffic_lights_details'),

    path('ajax/search-traffic-lights-cities/', adminviews.search_traffic_lights_cities, name="ajax_search_traffic_lights_cities"),
    path('ajax/search-traffic-lights-streets/', adminviews.search_traffic_lights_streets, name="ajax_search_traffic_lights_streets"),
    path('ajax/search-traffic-lights-regions/', adminviews.search_traffic_lights_regions, name="ajax_search_traffic_lights_regions"),
 
    path('AddODMVR', adminviews.ADD_ODMVR, name='add_odmvr'),
    path('ManageODMVR', adminviews.MANAGE_ODMVR, name='manage_odmvr'),
    path('SearchODMVR_Ajax/', adminviews.SEARCH_ODMVR_AJAX, name='search_odmvr_ajax'),
    path('DeleteODMVR/<str:id>', adminviews.DELETE_ODMVR, name='delete_odmvr'),
    path('UpdateODMVR/<int:id>', adminviews.UPDATE_ODMVR, name='update_odmvr'),


    path('AddPositionOccupied', adminviews.ADD_POSITION_OCCUPIED, name='add_position_occupied'),
    path('ManagePositionOccupied', adminviews.MANAGE_POSITION_OCCUPIED, name='manage_position_occupied'),
    path('SearchPositionOccupiedAjax/', adminviews.SEARCH_POSITION_OCCUPIED_AJAX, name='search_position_occupied_ajax'),
    path('DeletePositionOccupied/<int:id>', adminviews.DELETE_POSITION_OCCUPIED, name='delete_position_occupied'),
    path('UpdatePositionOccupied/<int:id>', adminviews.UPDATE_POSITION_OCCUPIED, name='update_position_occupied'),

    path('AddVehicleType', adminviews.ADD_VEHICLE_TYPE, name='add_vehicle_type'),
    path('ManageVehicleType', adminviews.MANAGE_VEHICLE_TYPE, name='manage_vehicle_type'),
    path('SearchVehicleTypeAjax/', adminviews.SEARCH_VEHICLE_TYPE_AJAX, name='search_vehicle_type_ajax'),
    path('DeleteVehicleType/<str:id>', adminviews.DELETE_VEHICLE_TYPE, name='delete_vehicle_type'),
    path('UpdateVehicleType/<int:id>', adminviews.UPDATE_VEHICLE_TYPE, name='update_vehicle_type'),


    path('AddVehiclesOwner', adminviews.ADD_VEHICLES_OWNER, name='add_vehicles_owner'),
    path('ManageVehiclesOwners', adminviews.MANAGE_VEHICLES_OWNERS, name='manage_vehicles_owners'),
    path('UpdateVehiclesOwner/<int:id>', adminviews.UPDATE_VEHICLES_OWNER, name='update_vehicles_owner'),
    path('DeleteVehiclesOwner/<int:id>', adminviews.DELETE_VEHICLES_OWNER, name='delete_vehicles_owner'),
    path('SearchVehiclesOwnersAjax/', adminviews.SEARCH_VEHICLES_OWNERS_AJAX, name='search_vehicles_owners_ajax'),


    path('AddVehicle', adminviews.ADD_VEHICLE, name='add_vehicle'),
    path('ManageVehicles', adminviews.MANAGE_VEHICLES, name='manage_vehicles'),
    path('UpdateVehicle/<int:id>', adminviews.UPDATE_VEHICLE, name='update_vehicle'),
    path('DeleteVehicle/<int:id>', adminviews.DELETE_VEHICLE, name='delete_vehicle'),
    path('SearchVehicleAjax/', adminviews.SEARCH_VEHICLES_AJAX, name='search_vehicle_ajax'),


    # Винетки
    path('AddVignette', adminviews.ADD_VIGNETTE, name='add_vignette'),
    path('ManageVignettes', adminviews.MANAGE_VIGNETTES, name='manage_vignettes'),
    path('UpdateVignette/<int:id>', adminviews.UPDATE_VIGNETTE, name='update_vignette'),
    path('DeleteVignette/<int:id>', adminviews.DELETE_VIGNETTE, name='delete_vignette'),
    path('SearchVignetteAjax/', adminviews.SEARCH_VIGNETTES_AJAX, name='search_vignette_ajax'),
    path('SearchVehiclesForVignetteAjax/', adminviews.SEARCH_VEHICLES_FOR_VIGNETTE_AJAX, name='search_vehicles_for_vignette_ajax'),



path('AddInsurance', adminviews.ADD_INSURANCE, name='add_insurance'),
path('ManageInsurances', adminviews.MANAGE_INSURANCES, name='manage_insurances'),
path('UpdateInsurance/<int:id>', adminviews.UPDATE_INSURANCE, name='update_insurance'),
path('DeleteInsurance/<int:id>', adminviews.DELETE_INSURANCE, name='delete_insurance'),
path('SearchInsuranceAjax/', adminviews.SEARCH_INSURANCES_AJAX, name='search_insurance_ajax'),
path('SearchVehiclesForInsuranceAjax/', adminviews.SEARCH_VEHICLES_FOR_INSURANCE_AJAX, name='search_vehicles_for_insurance_ajax'),


path('AddTrafficFine', adminviews.ADD_TRAFFIC_FINE, name='add_traffic_fine'),
path('ManageTrafficFines', adminviews.MANAGE_TRAFFIC_FINES, name='manage_traffic_fines'),
path('UpdateTrafficFine/<int:id>', adminviews.UPDATE_TRAFFIC_FINE, name='update_traffic_fine'),
path('DeleteTrafficFine/<int:id>', adminviews.DELETE_TRAFFIC_FINE, name='delete_traffic_fine'),
path('SearchTrafficFineAjax/', adminviews.SEARCH_TRAFFIC_FINE_AJAX, name='search_traffic_fine_ajax'),
path('SearchVehiclesForTrafficFineAjax/', adminviews.SEARCH_VEHICLES_FOR_TRAFFIC_FINE_AJAX, name='search_vehicles_for_traffic_fine_ajax'),
path('SearchCitiesAjax/', adminviews.SEARCH_CITIES_AJAX, name='search_cities_ajax'),
path('SearchStreetsAjax/', adminviews.SEARCH_STREETS_AJAX, name='search_streets_ajax'),




    path('AddVehicles_License', adminviews.ADD_VEHICLES_LICENSE, name='add_vehicles_license'),
    path('ManageVehicles_Licenses', adminviews.MANAGE_VEHICLES_LICENSES, name='manage_vehicles_licenses'),
    path('SearchVehicles_LicensesAjax/', adminviews.SEARCH_VEHICLES_LICENSES_AJAX, name='search_vehicles_licenses_ajax'),

    path('UpdateVehicles_License/<int:id>', adminviews.UPDATE_VEHICLES_LICENSE, name='update_vehicles_license'),
    path('DeleteVehicles_License/<int:id>', adminviews.DELETE_VEHICLES_LICENSE, name='delete_vehicles_license'),

    path('LodgedComplaint', adminviews.LODGEDCOMPLAINTS, name='lodgedcomplaint'),

    path('ViewLodgedComplaint/<int:id>', adminviews.VIEWLODGEDCOMPLAINTS, name='viewlodgedcomplaint'),

    path('LodgedComplaintRemark', adminviews.LODGEDCOMPLAINTSREMARK, name='lodgedcomplaintremark'),
    path('ManageUser', adminviews.MANAGEUSERS, name='manageusers'),
    path('ViewUser/<str:id>',adminviews.VIEWUSERS, name='viewusers'),
    path('Admin/DeleteUser/<str:id>', adminviews.DELETEUSERS, name='delete_user'),
    path('Admin/UserComplaints/<str:id>', adminviews.USERSCOMPLAINTS, name='view_complaints'),
    path('NewComplaints', adminviews.NEWCOMPLAINTS, name='newcomplaints'),
    path('InprocessComplaints', adminviews.INPROCESSCOMPLAINTS, name='inprocesscomplaints'),
    path('ClosedComplaints', adminviews.CLOSEDCOMPLAINTS, name='closedcomplaints'),
    path('ComplaintsBetweenDateReport', adminviews.COMPLAINTSREPORT, name='complaintsreports'),
    path('UserBetweenDateReport', adminviews.USERBDREPORT, name='userbdreports'),
    path('SearchComplaints', adminviews.Search_Complaints, name='searchcomplaints'),
    path('SearchUsers', adminviews.Search_Users, name='searchusers'),
    path('EditUser/<int:id>', adminviews.EDIT_USER, name='edit_user'),
    path('AddUser/', adminviews.ADD_USER, name='add_user'),
    path('search_users_ajax/', adminviews.SEARCH_USERS_AJAX, name="search_users_ajax"),


     # This is user panel
    path('user/home', userviews.USERHOME, name='user_home'),
    path('user/usersignup/', userviews.USERSIGNUP, name='usersignup'),
    path('user/registercomplaint', userviews.REGCOMPLAINT, name='regcomplaint'),
    path('user/get_subcat/', userviews.get_subcat, name='get_subcat'),
    path('user/complainthistory', userviews.COMPLAINTHISTORY, name='complainthistory'),
    path('user/complainthistorydetails/<str:id>', userviews.COMPLAINTHISTORYDETAILS, name='complainthistorydetails'),



    path("user/get_streets/", userviews.get_streets, name="get_streets"),
    path("user/get_subcat/", userviews.get_subcategories, name="get_subcat"),


    #profile path
    path('user/profile', views.PROFILE, name='profile'),
    path('user/profile/update', views.PROFILE_UPDATE, name='profile_update'),
    path('user/password', views.CHANGE_PASSWORD, name='change_password'),
    path('user/notifications/', views.notifications, name='notifications'),


    path('police/home/', userviews.POLICEHOME, name="police_home"), 
    path('police/search/', userviews.police_search, name='police_search'),



#Поддръжка
path('support/er-diagram/', adminviews.generate_er_diagram, name='generate_er_diagram'),
path('support/backup-database/', adminviews.backup_database, name='backup_database'),



#Анализи
    path('geographic-analysis/', adminviews.geographic_analysis, name='geographic_analysis'),


]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

