from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from mainApp.models import *

class LoginView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/login.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class RegisterView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/register.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class ForgotPasswordView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/forgot-password.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class LogoutView(APIView):
    def get(self, request, *args, **kwargs):
        
        return render(request, "theme/forgot-password.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})

# ==================================================


class IndexView(APIView):
    
    context = {}
    def get(self, request, *args, **kwargs):
        
        self.context['is_dashbord_link_clicked']     = True
        self.context["is_waterPred_link_clicked"]    = False
        self.context['is_waterQuality_link_clicked'] =  False
        self.context['is_profil_link_clicked']       = False
        
        return render(request, "theme/index.html", context=self.context)
    
    def post(self, request, *args, **kwargs):
        #print(request.body)
        return render(request, "theme/index.html", {})

class ChartsView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/charts.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class TablesView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/tables.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class LogoutView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/forgot-password.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class ButtonsView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/buttons.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})

class QuatityPrediction(APIView):
    context = {}
    
    def get(self, request, *args, **kwargs):
        self.context['is_dashbord_link_clicked']     = True
        self.context["is_waterPred_link_clicked"]    = False
        self.context['is_waterQuality_link_clicked'] =  False
        self.context['is_profil_link_clicked']       = False
        
        return render(request, "theme/qualityPrediction.html", context = self.context)

    def post(self, request, *args, **kwargs):
        return Response({'status': 200})
    
class HistoriqueQualityDetect(APIView):
    context = {}
    def get(self, request, *args, **kwargs):
        self.context['is_dashbord_link_clicked']     = True
        self.context["is_waterPred_link_clicked"]    = False
        self.context['is_waterQuality_link_clicked'] =  False
        self.context['is_profil_link_clicked']       = False
        return render(request, "theme/historiqueQualityDetect.html", context=self.context)

    def post(self, request, *args, **kwargs):
        return Response({'status': 200})

class ParametersPrediction(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/parametersPrediction.html", {})

    def post(self, request, *args, **kwargs):
        return Response({'status': 200})
    

class CardsView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/cards.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class PageNotFoundView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/404.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class BlankView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/blank.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class ColorsView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/utilities-color.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class ParamPredictionHistoryView(APIView):
    def get(self, request, *args, **kwargs):
        context = {
            "params" : WaterParameterPred.objects.all()
        }
        
        return render(request, "theme/utilities-border.html", context = context)

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})

class ListParametres(APIView):
    def get(self, request, *args, **kwargs):
        context = {
            "params" : waterParameters.objects.all()
        }
        return render(request, "theme/listParametres.html", context = context)

    def post(self, request, *args, **kwargs):
        return Response({'status': 200})

class AnimationsView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/utilities-animation.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})


class OthersView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "theme/utilities-other.html", {})

    def post(self, request, *args, **kwargs):

        return Response({'status': 200})



class DashboardView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, "users/dashboard.html", {})

    def post(self, request, *args, **kwargs):
        return render(request, "users/dashboard.html", {})
