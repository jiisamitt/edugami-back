"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from interview.views import StudentCreateView, StudentCreateManyView, TestCreateView, TestAssignView, TestAnswerView, StudentRecommendationView, ResetView

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('test', TestCreateView.as_view(), name='test-create'),
    path('student', StudentCreateView.as_view(), name='student-create'),
    path('load-students', StudentCreateManyView.as_view(), name='load-students'),
    path('test/<int:test_id>/assign', TestAssignView.as_view(), name='test-assign'),
    path('test/<int:test_id>/answers', TestAnswerView.as_view(), name='test-answers'), # GET and POST
    path('recommendations/<int:student_id>', StudentRecommendationView.as_view(), name='student-recommendations'),
    path('reset', ResetView.as_view(), name='reset'),
]
