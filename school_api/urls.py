from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse, HttpRequest, JsonResponse

def home(response):
  return HttpResponse("<h1>Hello Home</>")



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('api/v1/', include("student_app.urls")),
    path('api/v1/', include('student_app.urls')),
]
