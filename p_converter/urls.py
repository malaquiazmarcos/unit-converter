from django.contrib import admin
from django.urls import path, include
from a_units_converter.views_template import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include('a_units_converter.urls')),
    path('', APIDocumentationView.as_view(), name='docs_api'),
]
