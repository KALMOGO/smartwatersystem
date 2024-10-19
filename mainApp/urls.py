from django.urls import path
from .views import *
app_name = 'mainApp'
urlpatterns = [
    # Water quality detection
    path("iot/parameters/list/",list_create_WaterParametersIoTIVIEW, name="list_water_parameters_iot"),
    path("iot/parameters/add/",list_create_WaterParametersIoTIVIEW, name="add_water_parameters_iot"),
    path("supervisor/parameters/add/",list_create_WaterParametersIoTIVIEW, name="add_water_parameters_iot"),

    path("user/parameters/list/",list_create_WaterParametersPersonIVIEW, name="list_water_parameters_user"),
    path("user/parameters/add/",list_create_WaterParametersPersonIVIEW, name="add_water_parameters_user"),

    # Water parameters prediction
    path("param/prediction/" ,list_create_WaterParameterPredVIEW, name="prediction_water_parameters"),
    path("predict/quality/"  ,WaterQualityPredictionAPIView,       name="prediction_water_quality"),
	path("param-water-list/" , list_create_WaterParametersAVIEW,  name="param_water_site_url"),    
	path("water-quality-csv/", some_streaming_csv_view, name="water_quality_csv_url"), # retourne les pred à l'utilisat sous forme de fichier csv pour un site   
	path("water-quality-correction/",update_retrieve_destroyVIEW , name="water_quality_correction_url"),    
	path("water-quality-pred-csv/",make_prediction_for_file_VIEW , name="water_quality_pred_with_file_url"), # Prediction pour fichier    

    # User info
    path("info/user/",GetUserInfoAPIView, name="info_conneted_user"),

]
