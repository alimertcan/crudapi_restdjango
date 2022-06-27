from django.urls import include, path
from .views import *

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view = get_schema_view(
   openapi.Info(
      title="Crud API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="tekin.mertcan@yahoo.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,

)
urlpatterns = [

    path('', ApiOverview, name='home'),
    path('add_passenger/', add_passenger, name='add_passenger'),
    path('trip_view/', trip_view_get_post, name='trip_view'),
    path('trip_view/<int:pk>', trip_view_update_delete, name='trip_view'),
    path('all_passengers/', view_passengers, name='view_passengers'),
    path('update_passenger/<int:pk>/', update_passenger, name='update_passenger'),
    path('passenger/<int:pk>/delete/', delete_passenger, name='delete_passenger'),
    path('', include('rest_framework.urls', namespace='rest_framework')),
    path('swagger',schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]