from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions
from rest_framework import exceptions
from .models import *
from .serializers import *
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from .qualityDetection import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from datetime import datetime
from .qualityDetection import *
from .paramsPredictionTemperature import *

User = get_user_model()
desired_format = "%m/%d/%Y %H:%M"  # Formatage de la date
class WaterParametersIoTAPIView(generics.ListCreateAPIView):
    '''
        View: get, post
        List Water Parameters by the user and non-user
    '''
    queryset = waterParameters.objects.all()
    serializer_class = WaterParametersIoT2Serializer
    paginator = None
    permission_classes = [HasAPIKey]
    
    def create(self, request, *args, **kwargs):
        """Modify to return only the quality predicted by the model"""
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = self.perform_create(serializer)
        
        # Use current time if harvesting_time is not provided
        current_time = datetime.now()
        time = current_time.strftime(desired_format)
        
        reelTimeData = {
            "time": time,
            "ph": request.data.get("ph", "0"),
            "temperature": request.data.get("temperature", "0"),
            "od": request.data.get("od", "0"),
            "turbidity": request.data.get("turbidity", "0")
        }
        
        # Send WebSocket message
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "data_updates",
            {
                "type": "data_update",
                "message": {"data": reelTimeData},
            }
        )
        # Response
        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        """ Returns the water quality value """
        
        api_key = self.request.headers.get('Authorization')
        if not api_key:
            return Response({"error": "API key not provided in the request headers."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            api_key = api_key.split(' ')[1]
        except IndexError:
            return Response({"error": "Invalid format for Authorization header."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user_iot = UserIoT.objects.get(api_key=api_key)
            user = user_iot.user
            site = user_iot.located_at
        except UserIoT.DoesNotExist:
            return Response({"error": "Invalid API key."}, status=status.HTTP_403_FORBIDDEN)
        water_parameter = serializer.save(user=user, site=site)
        quality = water_parameter.get_quality
        response_data = {"quality": quality}
        print(response_data)
        return response_data

list_create_WaterParametersIoTIVIEW = WaterParametersIoTAPIView.as_view()

@api_view(['GET', 'POST'])
@permission_classes([AllowAny]) 
def WaterQualityPredictionAPIView(request):
    if request.method == 'GET':
        temperature = request.query_params.get('temperature', None)
        if not temperature:
            return Response(data={"message": "temperature is required"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            quality = mainQualityDetection(temperature)
            response = {"quality": quality}
            return Response(data=response, status=status.HTTP_200_OK)
    return Response(data={"message": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class WaterParametersPersonAPIView(generics.ListCreateAPIView):
    '''
        View: get, post
        List and create Water Parameters per user
    '''
    serializer_class = WaterParametersPersonSerializer
    permission_classes = [IsAuthenticated]
    paginator = None

    def get_queryset(self):
        site = self.request.query_params.get('site', None)
        result = {}
        
        user = UserIoT.objects.filter(located_at=site)
        if user.exists():
            parameter = self.request.query_params.get('parameter', None)
            queryset = waterParameters.objects.filter(site=site,user =user[0].user )[:30] 
            if  queryset.exists():
                labels =  []
                data   =  []
                for dt in queryset:
                    # formatage de la date de recolte
                    harvesting_time = dt.harvesting_time.strftime(desired_format)
                    labels.append(harvesting_time)
                    if parameter == "temperature":
                        data.append(dt.temperature)
                    if parameter == "ph":
                        data.append(dt.ph)
                    if parameter == "od":
                        data.append(dt.oxygen)
                    if parameter == "turbidity":
                        data.append(dt.turbidity)
                result["labels"] = labels
                result["data"]   = data
            return result
        return result

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return Response(queryset)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
list_create_WaterParametersPersonIVIEW = WaterParametersPersonAPIView.as_view()

class CorrectionQualityAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WaterQualityPred.objects.all()
    serializer_class = WaterQualityPredSerializer
    permission_classes = [IsAuthenticated]
    paginator = None
    
    def update(self, request, *args, **kwargs):
        id_ = request.data.get("id")
        quality = True if request.data.get("quality", "false") == "true" else False
        
        if id_ is None or quality is None:
            return Response({"detail": "ID and quality are required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            instance = WaterQualityPred.objects.get(pk=id_)
        except WaterQualityPred.DoesNotExist:
            return Response({"detail": "Object not found."}, status=status.HTTP_404_NOT_FOUND)
        # Update the instance with the provided data
        instance.quality = quality
        instance.save()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
update_retrieve_destroyVIEW = CorrectionQualityAPIView.as_view()

#############################################################
class WaterParameterPredAPIView(generics.ListCreateAPIView):
    '''
        View: get, post
        liste Water Parameters par l'utilisateur et non par l'utilisateur
    '''
    queryset = WaterParameterPred.objects.all()
    serializer_class = WaterParameterPredSerializer
    paginator = None
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        
        if data["data_source"] != "Bama" or data["parameter"]!= "temperature":
            return StreamingHttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition":f'attachment; filename="prediction_{site}_parametres_model_inexistant.csv"'},
            )
        
        # Parsing date strings to datetime objects
        data['upper_border'] = datetime.strptime(data['upper_border'], '%Y-%m-%dT%H:%M')
        data['lower_border'] = datetime.strptime(data['lower_border'], '%Y-%m-%dT%H:%M')
        data['user'] = request.user.id  # Add user to the data
        
        # Seriaisation 
        serializer = self.get_serializer(data=data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return StreamingHttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="error.csv"'},
            )
            
        self.perform_create(serializer)
        start_datetime = data['lower_border']
        end_datetime   = data['upper_border']
        site           =  request.data.get("data_source", None)

        # Prediction de la temperature
        predictedTemperature  = mainParamsPrediction(start_datetime=start_datetime, end_datetime=end_datetime)
        
        # Creation du fichier de retoure 
        head_row = ["date","temperature"]
        result = [[param['datetime'],param["temperature"]] for param in predictedTemperature]
        result.insert(0, head_row)
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)

        return StreamingHttpResponse(
            (writer.writerow(row) for row in result),
            content_type="text/csv",
            headers={"Content-Disposition": f'attachment; filename="parametres_{site}_predit.csv"'},
        )
        
    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)
        
list_create_WaterParameterPredVIEW = WaterParameterPredAPIView.as_view()


# Retourne l'information sur l'utilisateur
@api_view(['POST'])
@permission_classes([AllowAny]) 
def GetUserInfoAPIView(request):
    if request.method == 'POST':
        email = request.data.get("email")
        
        if not email:
            return Response(data={"message": "email is required"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.filter(email = email)
        if not user.exists():
            return Response(data={"message": "pas d'utilisateur"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        response = {"email": email, "name":f"{ user[0].first_name} { user[0].last_name}", "photo":user[0].photo}
        return Response(data=response, status=status.HTTP_200_OK)
    return Response(data={"message": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GetWaterParametersAPIView(generics.ListCreateAPIView):
    '''
        View: get, post
        List and create Water Parameters per user
    '''
    serializer_class = WaterParametersPersonSerializer
    permission_classes = [IsAuthenticated]
    paginator = None

    def get_queryset(self):
        user = self.request.user
        site = self.request.query_params.get('site', None)
        #parameter = self.request.query_params.get('parameter', None)
        queryset = waterParameters.objects.filter(site=site)[:1] 
        # result = {}
        return queryset


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
list_create_WaterParametersAVIEW = GetWaterParametersAPIView.as_view()

## Prediction de la qualité avec un fichier
class MakePredictionWithFileAPIWIEW(generics.ListCreateAPIView):
    queryset = waterParameters.objects.all()
    serializer_class = WaterParametersPersonSerializer
    permission_classes = [IsAuthenticated]
    paginator = None
    
    def create(self, request, *args, **kwargs):
        if not isinstance(request.data, list):
            return StreamingHttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="error.csv"'},
            )
        # Seriaisation 
        serializer = self.get_serializer(data=request.data, many=True)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return StreamingHttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="error.csv"'},
            )
        self.perform_create(serializer)
        
        # Creation du fichier de retoure 
        #print(serializer.data[0])
        head_row = ["ph","temperature", "turbidite", "oxygene", "site", "prediction"]
        result = [[param['ph'],param["temperature"], param["turbidity"], param["oxygen"], param["site"],mainQualityDetection(param["temperature"]) ] for param in serializer.data]
        result.insert(0, head_row)
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)

        return StreamingHttpResponse(
            (writer.writerow(row) for row in result),
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="qualite_predicte_resultat.csv"'},
        )
    
    def perform_create(self, serializer):
        # Ajout de l'utilisateur
        instances = serializer.save(user=self.request.user)
        #print(instances)
        return instances
    
make_prediction_for_file_VIEW = MakePredictionWithFileAPIWIEW.as_view()

### Generer fichier CSV de detection de la qualité de l'eau
import csv
from django.http import HttpResponse
from django.http import StreamingHttpResponse

from django.http import StreamingHttpResponse
import csv

class Echo:
    def write(self, value):
        return value

def some_streaming_csv_view(request):
    if request.method == 'GET':
        site = request.GET.get('site', None)
        if not site:
            return StreamingHttpResponse(
                content_type="text/csv",
                headers={"Content-Disposition": 'attachment; filename="error.csv"'},
            )
        
        head_row = ["id","harvesting_time", "temperature", "ph", "site", "quality"]
        quailiy_pred = WaterQualityPred.objects.filter(parameter__site=site)[:65536]
        result = [[param.id,param.parameter.harvesting_time, param.parameter.temperature, param.parameter.ph, site, param.quality] for param in quailiy_pred]
        result.insert(0, head_row)
        
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)

        return StreamingHttpResponse(
            (writer.writerow(row) for row in result),
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="qualite_predicte.csv"'},
        )
    else:
        return StreamingHttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="error.csv"'},
        )

def some_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="somefilename.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(["First row", "Foo", "Bar", "Baz"])
    writer.writerow(["Second row", "A", "B", "C", '"Testing"', "Here's a quote"])

    return response