from django.urls import path, include, re_path
# import routers
from rest_framework import routers
from rest_framework.authtoken import views as auth_views
from .views import (
    AllDataAPIView,
    ResearchAPIView,
    ProductionAPIView,
    ProtectAPIView,
    PHenologyAPIView,
    PhotoUpdateAPIView,
    ExperimentUpdateAPIView,
    NoteUpdateAPIView,
    UserPasswordChangeAPIView,
    WokrekResult,
    Quarantine,
    PlantsAPIviews,
    CountriesAPIviews,
    ProductTypesviews,
    MonthAPIviews

)

# define the router
router = routers.DefaultRouter()

# define the router path and viewset to be used

app_name = 'research'

urlpatterns = [
    path('', include(router.urls)),
    path("product",PlantsAPIviews.as_view()),# excellent
    path("product/type",ProductTypesviews.as_view()),# excellent
    path("country",CountriesAPIviews.as_view()),# excellent
    path("months",MonthAPIviews.as_view()),# excellent
    path("research/<int:pk>/",ResearchAPIView.as_view()),# excellent
    path("product/<int:pk>/",ProductionAPIView.as_view()),# excellent
    path("protect/<int:pk>/",ProtectAPIView.as_view()),# excellent
    path("phenology/<int:pk>/",PHenologyAPIView.as_view()),# excellent
    path("experiment/<int:pk>/",ExperimentUpdateAPIView.as_view()),# excellent
    path("photo/<int:pk>/",PhotoUpdateAPIView.as_view()),# excellent
    path("note/<int:pk>/",NoteUpdateAPIView.as_view()),# excellent
    path("user/change/password",UserPasswordChangeAPIView.as_view()),# excellent
    path('worker/resalt',WokrekResult.as_view()),# excellent
    path('quarantine/resalt/',Quarantine.as_view()),# excellent
    re_path(r"^alldata$",AllDataAPIView.as_view()),# excellent
    re_path(r'^auth/$', auth_views.obtain_auth_token),
   
   
]
