from rest_framework import serializers
from .models import InterviewSession, InterviewMessage, InterviewFeedback


class InterviewMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewMessage
        fields = [
            "id",
            "session",
            "role",
            "content",
            "transcript_text",
            "audio_url",
            "question_number",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

class InterviewFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewFeedback
        fields = [
            "id",
            "session",
            "overall_score",
            "technical_accuracy_score",
            "communication_score",
            "problem_solving_score",
            "depth_score",
            "confidence_score",
            "strengths",
            "weaknesses",
            "suggested_topics",
            "summary",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

class InterviewSessionSerializer(serializers.ModelSerializer):
    messages = InterviewMessageSerializer(many=True, read_only=True)
    feedback = InterviewFeedbackSerializer(read_only=True)

    class Meta:
        model = InterviewSession
        fields = [
            "id",
            "user",
            "category",
            "tech_stack",
            "level",
            "duration_minutes",
            "optional_topic",
            "status",
            "overall_score",
            "started_at",
            "ended_at",
            "created_at",
            "updated_at",
            "messages",
            "feedback",
        ]
        read_only_fields = [
            "id",
            "user",
            "overall_score",
            "started_at",
            "ended_at",
            "created_at",
            "updated_at",
        ]

class StartInterviewSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewSession
        fields = [
            "category",
            "tech_stack",
            "level",
            "duration_minutes",
            "optional_topic",
        ]


class SubmitAnswerSerializer(serializers.Serializer):
    content = serializers.CharField()