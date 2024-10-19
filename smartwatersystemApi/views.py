from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


class IndexView(APIView):
	def get(self, request, *args, **kwargs):
		context = {}
		context['is_dashbord_link_clicked']     = True
		context["is_waterPred_link_clicked"]    = False
		context['is_waterQuality_link_clicked'] =  False
		context['is_profil_link_clicked']       = False

		return render(request, "theme/login.html", {})

	def post(self, request, *args, **kwargs):

		return Response({'status': 200})