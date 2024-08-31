from django.urls import path
from .views import SignUpView, LoginView, LoadDataView, SummaryReportView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('load-data/', LoadDataView.as_view(), name='load_data'),
    path('summary-report/', SummaryReportView.as_view(), name='summary_report'),
]
