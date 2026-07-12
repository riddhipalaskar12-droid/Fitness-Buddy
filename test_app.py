"""
Validation test — run with: python test_app.py
"""
import sys
import os
import json
import types

os.environ.setdefault("IBM_API_KEY", "")
os.environ.setdefault("IBM_PROJECT_ID", "")

# Mock ibm_watsonx_ai so tests work without the heavy ML package
fake = types.ModuleType("ibm_watsonx_ai")
fake.APIClient = None
fake.Credentials = None
fake_fm = types.ModuleType("ibm_watsonx_ai.foundation_models")
fake_fm.ModelInference = None
fake_meta = types.ModuleType("ibm_watsonx_ai.metanames")

class _GenParams:
    MAX_NEW_TOKENS    = "max_new_tokens"
    TEMPERATURE       = "temperature"
    TOP_P             = "top_p"
    REPETITION_PENALTY = "repetition_penalty"

fake_meta.GenTextParamsMetaNames = _GenParams
sys.modules["ibm_watsonx_ai"] = fake
sys.modules["ibm_watsonx_ai.foundation_models"] = fake_fm
sys.modules["ibm_watsonx_ai.metanames"] = fake_meta

from app import create_app   # noqa: E402

app = create_app()
client = app.test_client()

passed = 0
failed = 0

def check(name, cond, detail=""):
    global passed, failed
    if cond:
        print(f"  [PASS] {name}")
        passed += 1
    else:
        print(f"  [FAIL] {name} — {detail}")
        failed += 1

print("\n── Page Routes ──────────────────────────────────────────────")
for route in ["/", "/chat", "/dashboard", "/calculator", "/planner", "/profiles", "/health"]:
    r = client.get(route)
    check(f"GET {route}", r.status_code == 200, f"status={r.status_code}")

print("\n── BMI Calculator ───────────────────────────────────────────")
r = client.post("/api/calculator/bmi", json={"weight": 70, "height": 170})
d = json.loads(r.data)
check("BMI endpoint 200",     r.status_code == 200)
check("BMI value present",    "bmi" in d)
check("BMI category present", "category" in d)
check("BMI = 24.2",           d.get("bmi") == 24.2, str(d.get("bmi")))

r2 = client.post("/api/calculator/bmi", json={"weight": 40, "height": 170})
d2 = json.loads(r2.data)
check("BMI underweight",      "Underweight" in d2.get("category", ""))

r3 = client.post("/api/calculator/bmi", json={})
check("BMI missing input 400", r3.status_code == 400)

print("\n── BMR Calculator ───────────────────────────────────────────")
r = client.post("/api/calculator/bmr", json={
    "weight": 70, "height": 170, "age": 30,
    "gender": "male", "activity_level": "moderate"
})
d = json.loads(r.data)
check("BMR endpoint 200", r.status_code == 200)
check("BMR present",      "bmr" in d)
check("TDEE present",     "tdee" in d)
check("Weight loss col",  "weight_loss" in d)

print("\n── Water Calculator ─────────────────────────────────────────")
r = client.post("/api/calculator/water", json={"weight": 70, "activity_level": "moderate"})
d = json.loads(r.data)
check("Water endpoint 200",  r.status_code == 200)
check("Litres present",      "litres" in d)
check("Schedule present",    "schedule" in d and len(d["schedule"]) > 0)

print("\n── Fitness Service ──────────────────────────────────────────")
r = client.get("/api/fitness/motivation")
d = json.loads(r.data)
check("Motivation quote",  "quote" in d)
check("Motivation tip",    "tip" in d)
check("Motivation date",   "date" in d)

r = client.get("/api/fitness/exercises")
d = json.loads(r.data)
check("Exercise library",   "beginner" in d and "advanced" in d)

r = client.get("/api/fitness/meals?diet=vegetarian")
d = json.loads(r.data)
check("Meal suggestions",  "breakfast" in d and "lunch" in d)

r = client.get("/api/fitness/warmup")
d = json.loads(r.data)
check("Warmup routine",    "warmup" in d and len(d["warmup"]) > 0)

r = client.get("/api/fitness/cooldown")
d = json.loads(r.data)
check("Cooldown routine",  "cooldown" in d and len(d["cooldown"]) > 0)

r = client.post("/api/fitness/workout-plan", json={
    "fitness_level": "intermediate", "goal": "weight_loss"
})
d = json.loads(r.data)
check("Workout plan 7 days", len(d.get("plan", {})) == 7)
check("Workout plan level",  d.get("level") == "intermediate")

print("\n── Chat (Demo Mode) ─────────────────────────────────────────")
r = client.post("/api/chat/send", json={"message": "Hello give me a workout"})
d = json.loads(r.data)
check("Chat response present",  "response" in d)
check("Chat response non-empty", len(d.get("response", "")) > 10)

r = client.post("/api/chat/send", json={"message": ""})
check("Chat empty input 400",  r.status_code == 400)

r = client.get("/api/chat/history")
check("Chat history endpoint", r.status_code == 200)

r = client.post("/api/chat/clear", json={})
check("Chat clear endpoint",   r.status_code == 200)

r = client.get("/api/chat/status")
d = json.loads(r.data)
check("Chat status endpoint",  "connected" in d)

print("\n── Profile CRUD ─────────────────────────────────────────────")
with app.test_request_context():
    pass

r = client.post("/api/profiles/", json={
    "name": "Test User", "age": 30, "gender": "male",
    "height": 170, "weight": 70, "fitness_level": "intermediate"
})
check("Create profile 201",  r.status_code == 201)

r = client.get("/api/profiles/")
d = json.loads(r.data)
check("List profiles",       len(d.get("profiles", [])) >= 1)

r = client.post("/api/profiles/", json={"name": ""})
check("Profile missing name 400", r.status_code == 400)

print("\n--- Error Handling ---")
r = client.get("/nonexistent-route")
check("404 returns 404", r.status_code == 404)

print()
print(f"══ Results: {passed} passed, {failed} failed ══")
sys.exit(0 if failed == 0 else 1)
