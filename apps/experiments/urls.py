from django.urls import path, include

from apps.experiments import views

single_choice_patterns = [
    path('', views.SingleChoiceExperimentView.as_view(), name='single-choice-experiment'),
    path('result/', views.SingleChoiceResultView.as_view(), name='single-choice-result'),
]

multiple_choice_patterns = [
    path('', views.MultipleChoiceExperimentView.as_view(), name='multiple-choice-experiment'),
    path('result/', views.SingleChoiceResultView.as_view(), name='multiple-choice-result'),
]

urlpatterns = [
    path('single_choice/', include(single_choice_patterns)),
    path('multiple_choice/', include(multiple_choice_patterns)),
]
