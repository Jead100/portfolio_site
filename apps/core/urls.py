from django.urls import path
from .views import PortfolioView, download_resume

urlpatterns = [
    path('', PortfolioView.as_view(), name='portfolio'),
    path("resume/download/", download_resume, name="resume_download"),
]
