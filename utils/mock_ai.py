MOCK_QUESTIONS = {
    "dsa": [
        "Can you describe an approach to reverse a linked list?",
        "How would you find two numbers in an array that sum to a target value?",
        "What's the time complexity of your solution, and can it be improved?",
        "How would you handle duplicate values in this problem?",
    ],
    "system_design": [
        "How would you design a URL shortening service?",
        "How would you scale this system to handle 10x traffic?",
        "What are the trade-offs of a relational vs NoSQL database here?",
        "How would you handle failover for this service?",
    ],
    "behavioral": [
        "Tell me about a time you disagreed with a teammate. How did you resolve it?",
        "Describe a project you're proud of and why.",
        "How do you prioritize tasks when everything feels urgent?",
        "Tell me about a time you failed and what you learned.",
    ],
    "production_issue": [
        "Walk me through how you'd debug a sudden spike in API latency.",
        "How would you identify the root cause of an intermittent 500 error?",
        "What steps would you take if a deployment caused a partial outage?",
        "How do you communicate incidents to stakeholders during an outage?",
    ],
    "tech_stack": [
        "What features of this stack do you find most useful, and why?",
        "How would you optimize performance in this stack?",
        "What common pitfalls have you seen when using this stack?",
        "How do you approach testing in this stack?",
    ],
}

DEFAULT_CATEGORY = "dsa"


def generate_question(category, question_number):
    questions = MOCK_QUESTIONS.get(category, MOCK_QUESTIONS[DEFAULT_CATEGORY])
    return questions[(question_number - 1) % len(questions)]
