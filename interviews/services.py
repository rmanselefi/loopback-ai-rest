from django.http import Http404
from django.utils import timezone

from utils.mock_ai import generate_question

from .models import InterviewMessage, InterviewSession


class InterviewSessionService:
    @staticmethod
    def start_session(user, validated_data):
        session = InterviewSession.objects.create(user=user, **validated_data)

        InterviewMessage.objects.create(
            session=session,
            role=InterviewMessage.Role.AI,
            content=generate_question(session.category, question_number=1),
            question_number=1,
        )

        return session

    @staticmethod
    def list_sessions(user):
        return InterviewSession.objects.filter(user=user).order_by("-created_at")

    @staticmethod
    def get_owned_session(user, session_id):
        try:
            return InterviewSession.objects.get(id=session_id, user=user)
        except InterviewSession.DoesNotExist:
            raise Http404("Interview session not found")

    @staticmethod
    def submit_answer(session, content):
        current_question_number = session.messages.filter(
            role=InterviewMessage.Role.AI
        ).count()

        user_message = InterviewMessage.objects.create(
            session=session,
            role=InterviewMessage.Role.USER,
            content=content,
            question_number=current_question_number,
        )

        next_question_number = current_question_number + 1
        ai_message = InterviewMessage.objects.create(
            session=session,
            role=InterviewMessage.Role.AI,
            content=generate_question(session.category, next_question_number),
            question_number=next_question_number,
        )

        return user_message, ai_message

    @staticmethod
    def end_session(session):
        session.status = InterviewSession.Status.COMPLETED
        session.ended_at = timezone.now()
        session.save(update_fields=["status", "ended_at"])
        return session
