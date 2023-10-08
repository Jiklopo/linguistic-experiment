from django.urls import path

from apps.experiments import views

urlpatterns = [
    path('single_choice/', views.SingleChoiceExperimentView.as_view(), name='single-choice-experiment')
]
