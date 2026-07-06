from django.urls import path
from .views import (
    EndInterviewView,
    InterviewDetailView,
    InterviewFeedbackView,
    ListInterviewsView,
    StartInterviewView,
    SubmitAnswerView,
)

urlpatterns = [
    path("start/", StartInterviewView.as_view(), name="start_interview"),
    path("", ListInterviewsView.as_view(), name="list_interviews"),
    path("<int:session_id>/", InterviewDetailView.as_view(), name="interview_detail"),
    path("<int:session_id>/answer/", SubmitAnswerView.as_view(), name="submit_answer"),
    path("<int:session_id>/end/", EndInterviewView.as_view(), name="end_interview"),
    path("<int:session_id>/feedback/", InterviewFeedbackView.as_view(), name="interview_feedback"),
]
