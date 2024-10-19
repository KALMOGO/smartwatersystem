from django.urls import re_path, path 
from . import views

app_name = "users"


urlpatterns = [
    # Login, Register, Forgot password, Logout
    re_path(r'^login/$', views.LoginView.as_view(), name="login_url"),
    re_path(r'^register/$', views.RegisterView.as_view(), name="register_url"),
    re_path(r'^forgot-password/$', views.ForgotPasswordView.as_view(), name="forgot_password_url"),
    re_path(r'^logout/$', views.LogoutView.as_view(), name="logout_url"),
    # Web pages used
    re_path(r'^home/$', views.IndexView.as_view(), name="index_url_user"),
    re_path(r'^historic-quality/$', views.HistoriqueQualityDetect.as_view(), name="historic_quality_url"),
    re_path(r'^water-quality/$', views.QuatityPrediction.as_view(), name="water_quality_url"), 
	re_path(r'^param-prediction-history/$', views.ParamPredictionHistoryView.as_view(), name="param_pred_history_url"),    
	re_path(r'^list-param/$', views.ListParametres.as_view(), name="param_list"),    
	re_path(r'^param-prediction/$', views.ParametersPrediction.as_view(), name="parame_prediction_url"),    
	re_path(r'^page_not_found/$', views.PageNotFoundView.as_view(), name="page_not_found_url"),    


    # Not used
    re_path(r'^charts/$', views.ChartsView.as_view(), name="charts_url"),
    re_path(r'^tables/$', views.TablesView.as_view(), name="tables_url"),
	re_path(r'^blank/$', views.BlankView.as_view(), name="blank_page_url"),    
	re_path(r'^animations/$', views.AnimationsView.as_view(), name="animations_url"),    
	re_path(r'^dashbord/$', views.DashboardView.as_view(), name="dashbord_url"),    

]