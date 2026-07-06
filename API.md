# Loopback API — Frontend Integration Guide

Base URL (dev): `http://127.0.0.1:8000/api/v1`

Interactive docs: `http://127.0.0.1:8000/api/docs/` (Swagger UI)
Raw OpenAPI spec: `http://127.0.0.1:8000/api/schema/` or [openapi.yaml](openapi.yaml) in this repo — import either into Postman/Insomnia or use for client codegen.

All endpoints except `register`, `login`, and `refresh` require an `Authorization: Bearer <access_token>` header. CORS is open to all origins in dev.

---

## Auth

### Register
`POST /auth/register/`

Request:
```json
{ "username": "jane", "email": "jane@example.com", "full_name": "Jane Doe", "password": "at-least-8-chars" }
```
Response `201`:
```json
{ "id": 1, "username": "jane", "email": "jane@example.com", "full_name": "Jane Doe" }
```

### Login
`POST /auth/login/`

Request:
```json
{ "email": "jane@example.com", "password": "at-least-8-chars" }
```
Response `200`:
```json
{ "access": "<jwt>", "refresh": "<jwt>" }
```
`access` expires in 60 minutes, `refresh` in 7 days.

### Refresh token
`POST /auth/refresh/`

Request:
```json
{ "refresh": "<refresh_token>" }
```
Response `200`:
```json
{ "access": "<new_jwt>" }
```

### Current user
`GET /auth/me/` (auth required)

Response `200`:
```json
{ "id": 1, "username": "jane", "email": "jane@example.com", "full_name": "Jane Doe" }
```

---

## Interviews

All routes below require `Authorization: Bearer <access_token>`. Sessions are scoped to the requesting user — accessing another user's session returns `404`.

Category choices: `dsa`, `system_design`, `behavioral`, `production_issue`, `tech_stack`
Level choices: `junior`, `mid`, `senior`, `lead`
Status values: `active`, `completed`, `cancelled`

### Start interview
`POST /interviews/start/`

Request:
```json
{ "category": "dsa", "level": "mid", "duration_minutes": 30, "tech_stack": null, "optional_topic": null }
```
Response `201` — full session, with the first AI question already generated in `messages`:
```json
{
  "id": 1,
  "user": 1,
  "category": "dsa",
  "tech_stack": null,
  "level": "mid",
  "duration_minutes": 30,
  "optional_topic": null,
  "status": "active",
  "overall_score": null,
  "started_at": "2026-07-05T12:17:35Z",
  "ended_at": null,
  "created_at": "2026-07-05T12:17:35Z",
  "updated_at": "2026-07-05T12:17:35Z",
  "messages": [
    { "id": 1, "session": 1, "role": "ai", "content": "Can you describe an approach to reverse a linked list?", "transcript_text": null, "audio_url": null, "question_number": 1, "created_at": "2026-07-05T12:17:35Z" }
  ],
  "feedback": null
}
```

### List my interviews
`GET /interviews/`

Response `200`: array of session objects (same shape as above), newest first.

### Get interview detail
`GET /interviews/{id}/`

Response `200`: single session object, `messages` in chronological order, `feedback` populated once the session has ended.

### Submit answer
`POST /interviews/{id}/answer/`

Request:
```json
{ "content": "My answer to the question" }
```
Response `201` — the saved user message and the auto-generated next AI question:
```json
{
  "user_message": { "id": 2, "session": 1, "role": "user", "content": "My answer...", "transcript_text": null, "audio_url": null, "question_number": 1, "created_at": "..." },
  "ai_message": { "id": 3, "session": 1, "role": "ai", "content": "How would you find two numbers in an array that sum to a target value?", "transcript_text": null, "audio_url": null, "question_number": 2, "created_at": "..." }
}
```

### End interview
`POST /interviews/{id}/end/`

No request body. Marks the session `completed` and sets `ended_at`.
Response `200`: the updated session object.

> Feedback generation (mock scores/summary created on end) is not implemented yet — `feedback` will remain `null` and `GET .../feedback/` will 404 until that's built.

### Get feedback
`GET /interviews/{id}/feedback/`

Response `200` once feedback exists:
```json
{
  "id": 1, "session": 1,
  "overall_score": "0.00", "technical_accuracy_score": "0.00", "communication_score": "0.00",
  "problem_solving_score": "0.00", "depth_score": "0.00", "confidence_score": "0.00",
  "strengths": [], "weaknesses": [], "suggested_topics": [], "summary": "",
  "created_at": "..."
}
```
Response `404` before feedback exists:
```json
{ "detail": "Feedback not available for this session yet." }
```

---

## Error shapes

- Validation errors (`400`): DRF's standard `{ "field_name": ["error message"] }`.
- Unauthenticated (`401`): `{ "detail": "Authentication credentials were not provided." }`.
- Missing or not-owned resource (`404`): `{ "detail": "Interview session not found" }` (or Django's default 404 body).
