from django.db import models
from django.conf import settings
# Create your models here.

class InterviewSession(models.Model):
    class Category(models.TextChoices):
        DSA = "dsa", "DSA"
        SYSTEM_DESIGN = "system_design", "System Design"
        BEHAVIORAL = "behavioral", "Behavioral"
        PRODUCTION_ISSUE = "production_issue", "Production Issue"
        TECH_STACK = "tech_stack", "Tech Stack Specific"

    class level(models.TextChoices):
        JUNIOR = "junior", "Junior"
        MID = "mid", "Mid"
        SENIOR = "senior", "Senior"
        LEAD = "lead", "Lead"

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="interview_sessions"
    )

    category  = models.CharField(max_length=50, choices=Category.choices)
    level = models.CharField(max_length=50, choices=level.choices)
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.ACTIVE)
    tech_stack = models.CharField(max_length=255, blank=True, null=True)
    duration_minutes = models.PositiveIntegerField(default=30)
    optional_topic = models.CharField(max_length=255, blank=True, null=True)

    overall_score = models.DecimalField(
        max_digits=4, decimal_places=2, blank=True, null=True
    )

    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"InterviewSession {self.id} for {self.user.email} - {self.category} ({self.level})"
    
class InterviewMessage(models.Model):
    class Role(models.TextChoices):
        USER = "user", "User"
        AI = "ai", "AI"
    
    session = models.ForeignKey(
        InterviewSession, on_delete=models.CASCADE, related_name="messages"
    )

    role = models.CharField(max_length=10, choices=Role.choices)
    content = models.TextField()
    transcript_text = models.TextField(blank=True, null=True)
    audio_url = models.URLField(blank=True, null=True)
    question_number = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at", "id"]

    def __str__(self):
        return f"Message {self.id} in Session {self.session.id} - {self.role}"
    
class InterviewFeedback(models.Model):

    session = models.OneToOneField(
        InterviewSession, on_delete=models.CASCADE, related_name="feedback"
    )

    overall_score = models.DecimalField(max_digits=5, decimal_places=2)
    technical_accuracy_score = models.DecimalField(max_digits=5, decimal_places=2)
    communication_score = models.DecimalField(max_digits=5, decimal_places=2)
    problem_solving_score = models.DecimalField(max_digits=5, decimal_places=2)
    depth_score = models.DecimalField(max_digits=5, decimal_places=2)
    confidence_score = models.DecimalField(max_digits=5, decimal_places=2)

    strengths = models.JSONField(default=list)
    weaknesses = models.JSONField(default=list)
    suggested_topics = models.JSONField(default=list)
    summary = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for session {self.session.id}"