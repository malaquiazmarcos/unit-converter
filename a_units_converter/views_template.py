from django.shortcuts import render
from django.views.generic import TemplateView

class APIDocumentationView(TemplateView):
    """
    Render template to documentation API.
    """
    template_name = 'docs_api.html'