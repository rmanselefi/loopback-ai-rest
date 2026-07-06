from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    InterviewFeedbackSerializer,
    InterviewMessageSerializer,
    InterviewSessionSerializer,
    StartInterviewSessionSerializer,
    SubmitAnswerSerializer,
)
from .services import InterviewSessionService

# Create your views here.

class StartInterviewView(APIView):

    @extend_schema(request=StartInterviewSessionSerializer, responses=InterviewSessionSerializer)
    def post(self, request):
        serializer = StartInterviewSessionSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        session = InterviewSessionService.start_session(user=request.user, validated_data=serializer.validated_data)

        return Response(
            InterviewSessionSerializer(session).data,
            status=status.HTTP_201_CREATED
        )


class ListInterviewsView(APIView):

    @extend_schema(responses=InterviewSessionSerializer(many=True))
    def get(self, request):
        sessions = InterviewSessionService.list_sessions(user=request.user)
        return Response(InterviewSessionSerializer(sessions, many=True).data)


class InterviewDetailView(APIView):

    @extend_schema(responses=InterviewSessionSerializer)
    def get(self, request, session_id):
        session = InterviewSessionService.get_owned_session(request.user, session_id)
        return Response(InterviewSessionSerializer(session).data)


class SubmitAnswerView(APIView):

    @extend_schema(
        request=SubmitAnswerSerializer,
        responses=inline_serializer(
            name="SubmitAnswerResponse",
            fields={
                "user_message": InterviewMessageSerializer(),
                "ai_message": InterviewMessageSerializer(),
            },
        ),
    )
    def post(self, request, session_id):
        session = InterviewSessionService.get_owned_session(request.user, session_id)

        serializer = SubmitAnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_message, ai_message = InterviewSessionService.submit_answer(
            session=session, content=serializer.validated_data["content"]
        )

        return Response(
            {
                "user_message": InterviewMessageSerializer(user_message).data,
                "ai_message": InterviewMessageSerializer(ai_message).data,
            },
            status=status.HTTP_201_CREATED,
        )


class EndInterviewView(APIView):

    @extend_schema(request=None, responses=InterviewSessionSerializer)
    def post(self, request, session_id):
        session = InterviewSessionService.get_owned_session(request.user, session_id)
        session = InterviewSessionService.end_session(session)
        return Response(InterviewSessionSerializer(session).data)


class InterviewFeedbackView(APIView):

    @extend_schema(responses=InterviewFeedbackSerializer)
    def get(self, request, session_id):
        session = InterviewSessionService.get_owned_session(request.user, session_id)

        if not hasattr(session, "feedback"):
            return Response(
                {"detail": "Feedback not available for this session yet."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(InterviewFeedbackSerializer(session.feedback).data)
