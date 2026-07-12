"""
Fitness Service
Generates workout plans, exercise libraries, meal suggestions, and yoga routines.
"""

import random
from datetime import datetime


# ---------------------------------------------------------------------------
# Exercise Library
# ---------------------------------------------------------------------------
EXERCISE_LIBRARY = {
    "beginner": [
        {"name": "Wall Push-Up",        "muscles": "Chest, Triceps",          "duration": "3×10", "calories": 40,  "tip": "Keep body straight, chest touches wall."},
        {"name": "Chair Squat",          "muscles": "Quads, Glutes",           "duration": "3×12", "calories": 50,  "tip": "Sit back like sitting in a chair, keep knees over toes."},
        {"name": "Marching in Place",    "muscles": "Cardio, Hip Flexors",     "duration": "3 min","calories": 30,  "tip": "Drive knees high, pump arms for intensity."},
        {"name": "Seated Leg Raise",     "muscles": "Core, Hip Flexors",       "duration": "3×10", "calories": 25,  "tip": "Sit tall, raise both legs together, hold 2 sec."},
        {"name": "Standing Calf Raise",  "muscles": "Calves",                  "duration": "3×15", "calories": 20,  "tip": "Rise on toes fully, lower slowly for max stretch."},
        {"name": "Arm Circles",          "muscles": "Shoulders, Mobility",     "duration": "2×30s","calories": 15,  "tip": "Start small circles, gradually widen."},
        {"name": "Knee Push-Up",         "muscles": "Chest, Triceps",          "duration": "3×8",  "calories": 35,  "tip": "Keep core tight, lower chest to floor."},
        {"name": "Step Touch",           "muscles": "Cardio",                  "duration": "3 min","calories": 28,  "tip": "Keep a steady rhythm, add arm swings."},
        {"name": "Glute Bridge",         "muscles": "Glutes, Hamstrings",      "duration": "3×12", "calories": 35,  "tip": "Drive hips up, squeeze glutes at top, hold 1 sec."},
        {"name": "Bird Dog",             "muscles": "Core, Lower Back",        "duration": "3×8e", "calories": 20,  "tip": "Opposite arm and leg, keep hips square."},
    ],
    "intermediate": [
        {"name": "Standard Push-Up",     "muscles": "Chest, Triceps, Shoulders","duration": "4×15","calories": 65,  "tip": "Full range — chest skims floor, arms fully extended."},
        {"name": "Bodyweight Squat",     "muscles": "Quads, Glutes, Hamstrings","duration": "4×20","calories": 80,  "tip": "Break parallel, weight on heels, chest up."},
        {"name": "Reverse Lunge",        "muscles": "Quads, Glutes",           "duration": "3×12e","calories": 70, "tip": "Back knee hovers 1 inch off floor, front shin vertical."},
        {"name": "Plank Hold",           "muscles": "Core",                    "duration": "3×40s","calories": 30,  "tip": "Elbows under shoulders, body rigid, breathe steadily."},
        {"name": "Mountain Climber",     "muscles": "Core, Cardio",            "duration": "3×30s","calories": 90,  "tip": "Drive knees toward chest alternately, fast pace."},
        {"name": "Tricep Dip (chair)",   "muscles": "Triceps",                 "duration": "3×12", "calories": 45,  "tip": "Elbows point back, lower until 90°, press up."},
        {"name": "High Knees",           "muscles": "Cardio, Hip Flexors",     "duration": "3×30s","calories": 95,  "tip": "Drive knees above hip height, land softly on toes."},
        {"name": "Superman Hold",        "muscles": "Lower Back, Glutes",      "duration": "3×10", "calories": 25,  "tip": "Lift arms and legs simultaneously, hold 2 sec at top."},
        {"name": "Side Plank",           "muscles": "Obliques, Core",          "duration": "3×30e","calories": 28,  "tip": "Stack feet or stagger, keep hips raised throughout."},
        {"name": "Jump Rope (simulated)","muscles": "Cardio, Calves",          "duration": "3×1min","calories":110, "tip": "Wrist rotation only, light landing on toes."},
        {"name": "Sumo Squat",           "muscles": "Inner Thighs, Glutes",    "duration": "3×15", "calories": 70,  "tip": "Wide stance, toes out 45°, keep knees tracking toes."},
        {"name": "Donkey Kick",          "muscles": "Glutes",                  "duration": "3×15e","calories": 40,  "tip": "Keep 90° knee bend, drive heel toward ceiling."},
    ],
    "advanced": [
        {"name": "Diamond Push-Up",      "muscles": "Triceps, Chest",          "duration": "4×12", "calories": 80,  "tip": "Thumbs and index fingers form a diamond, elbows brush ribs."},
        {"name": "Jump Squat",           "muscles": "Quads, Glutes, Power",    "duration": "4×15", "calories":120,  "tip": "Land softly with bent knees, immediately into next rep."},
        {"name": "Bulgarian Split Squat","muscles": "Quads, Glutes",           "duration": "4×10e","calories": 95,  "tip": "Rear foot elevated, front shin vertical, torso upright."},
        {"name": "Pike Push-Up",         "muscles": "Shoulders, Triceps",      "duration": "4×12", "calories": 75,  "tip": "Hips high in inverted-V, lower crown toward floor."},
        {"name": "L-Sit (floor)",        "muscles": "Core, Hip Flexors",       "duration": "3×20s","calories": 55,  "tip": "Press palms down hard, legs parallel to floor."},
        {"name": "Burpee",               "muscles": "Full Body, Cardio",       "duration": "4×10", "calories":150,  "tip": "Flow: plank → push-up → jump → reach overhead."},
        {"name": "Pistol Squat (assisted)","muscles": "Quads, Balance",        "duration": "3×6e", "calories": 85,  "tip": "Hold a doorframe for balance, extend one leg, sit deep."},
        {"name": "Hollow Body Hold",     "muscles": "Core",                    "duration": "3×30s","calories": 45,  "tip": "Lower back pressed down, arms overhead, legs low."},
        {"name": "Plyometric Push-Up",   "muscles": "Chest, Explosive Power",  "duration": "3×8",  "calories": 95,  "tip": "Explode off floor, clap if able, absorb landing softly."},
        {"name": "Tuck Jump",            "muscles": "Legs, Core, Cardio",      "duration": "4×10", "calories":130,  "tip": "Drive knees to chest at peak, land on toes, immediately repeat."},
        {"name": "Archer Push-Up",       "muscles": "Chest, Shoulders",        "duration": "3×8e", "calories": 75,  "tip": "One arm extended for each rep, shift weight laterally."},
    ],
}

WARMUP_ROUTINE = [
    "Neck rolls — 30 sec each direction",
    "Shoulder shrugs & rolls — 1 min",
    "Arm swings (front & cross) — 1 min",
    "Hip circles — 30 sec each side",
    "Leg swings (forward & lateral) — 30 sec each",
    "Ankle circles — 30 sec each",
    "Light jogging in place — 2 min",
    "Dynamic quad stretch — 30 sec each leg",
    "World's greatest stretch — 30 sec each side",
    "Inchworm walk — 5 reps",
]

COOLDOWN_ROUTINE = [
    "Standing quad stretch — 30 sec each leg",
    "Hamstring stretch (seated reach) — 45 sec each",
    "Figure-4 glute stretch — 45 sec each",
    "Child's pose — 1 min",
    "Cat-Cow stretch — 1 min (10 reps)",
    "Pigeon pose — 45 sec each side",
    "Chest opener (hands clasped behind) — 30 sec",
    "Spinal twist (lying) — 30 sec each side",
    "Legs-up-the-wall — 2 min",
    "Deep diaphragmatic breathing — 2 min",
]

# ---------------------------------------------------------------------------
# Yoga Library
# ---------------------------------------------------------------------------
YOGA_LIBRARY = {
    "morning_flow": [
        {"name": "Surya Namaskar (Sun Salutation)", "sanskrit": "Sūrya Namaskāra",
         "duration": "5 rounds", "benefit": "Full body warm-up, energises, improves circulation",
         "level": "beginner"},
        {"name": "Mountain Pose", "sanskrit": "Tāḍāsana",
         "duration": "1 min", "benefit": "Posture alignment, grounding",
         "level": "beginner"},
        {"name": "Warrior I", "sanskrit": "Vīrabhadrāsana I",
         "duration": "45 sec each side", "benefit": "Strength, balance, hip flexor stretch",
         "level": "beginner"},
        {"name": "Warrior II", "sanskrit": "Vīrabhadrāsana II",
         "duration": "45 sec each side", "benefit": "Leg strength, endurance, focus",
         "level": "beginner"},
        {"name": "Tree Pose", "sanskrit": "Vṛkṣāsana",
         "duration": "1 min each leg", "benefit": "Balance, focus, ankle stability",
         "level": "beginner"},
    ],
    "flexibility": [
        {"name": "Downward Dog", "sanskrit": "Adho Mukha Śvānāsana",
         "duration": "1 min", "benefit": "Hamstrings, calves, shoulders, spine decompression",
         "level": "beginner"},
        {"name": "Seated Forward Bend", "sanskrit": "Paścimottānāsana",
         "duration": "1 min", "benefit": "Hamstrings, spine, calming",
         "level": "beginner"},
        {"name": "Pigeon Pose", "sanskrit": "Kapotāsana",
         "duration": "1 min each side", "benefit": "Deep hip opener, piriformis stretch",
         "level": "intermediate"},
        {"name": "Camel Pose", "sanskrit": "Uṣṭrāsana",
         "duration": "30 sec", "benefit": "Deep backbend, chest opener, hip flexors",
         "level": "intermediate"},
        {"name": "King Pigeon", "sanskrit": "Eka Pāda Rājakapotāsana",
         "duration": "45 sec each side", "benefit": "Advanced hip & quad stretch",
         "level": "advanced"},
    ],
    "strength": [
        {"name": "Chair Pose", "sanskrit": "Utkaṭāsana",
         "duration": "1 min", "benefit": "Quads, glutes, core, mental endurance",
         "level": "beginner"},
        {"name": "Boat Pose", "sanskrit": "Nāvāsana",
         "duration": "30 sec holds, 3 sets", "benefit": "Core, hip flexors, balance",
         "level": "intermediate"},
        {"name": "Crow Pose", "sanskrit": "Bakāsana",
         "duration": "3×10 sec holds", "benefit": "Arm strength, core, balance",
         "level": "advanced"},
        {"name": "Headstand", "sanskrit": "Śīrṣāsana",
         "duration": "30 sec–2 min", "benefit": "Upper body strength, inverted circulation, focus",
         "level": "advanced"},
    ],
    "pranayama": [
        {"name": "Belly Breathing",      "sanskrit": "Dīrgha Prāṇāyāma",
         "duration": "5 min", "benefit": "Reduces stress, activates parasympathetic nervous system",
         "level": "beginner"},
        {"name": "Alternate Nostril Breathing", "sanskrit": "Nāḍī Śodhana",
         "duration": "5 min", "benefit": "Balances nervous system, reduces anxiety, clears sinuses",
         "level": "beginner"},
        {"name": "Kapalabhati (Skull Shining)", "sanskrit": "Kapālabhāti",
         "duration": "3 min", "benefit": "Energises, detoxifies, strengthens diaphragm",
         "level": "intermediate"},
        {"name": "Bhramari (Humming Bee)", "sanskrit": "Bhrāmarī",
         "duration": "5 min", "benefit": "Calming, reduces anxiety and insomnia",
         "level": "beginner"},
    ],
}

# ---------------------------------------------------------------------------
# Meal Suggestions — expanded with calories and macros
# ---------------------------------------------------------------------------
INDIAN_MEALS = {
    "breakfast": [
        {"name": "Vegetable poha with peanuts and lemon",             "calories": 280, "protein": 8,  "carbs": 45, "fat": 8},
        {"name": "Moong dal chilla with green chutney",               "calories": 240, "protein": 12, "carbs": 32, "fat": 6},
        {"name": "Oats upma with mixed vegetables",                   "calories": 260, "protein": 9,  "carbs": 42, "fat": 6},
        {"name": "Ragi dosa with sambar",                             "calories": 290, "protein": 10, "carbs": 48, "fat": 7},
        {"name": "Whole wheat paratha with curd",                     "calories": 320, "protein": 10, "carbs": 50, "fat": 9},
        {"name": "Sprouts chaat with cucumber and tomato",            "calories": 200, "protein": 14, "carbs": 30, "fat": 3},
        {"name": "Idli (3) with sambar and coconut chutney",          "calories": 270, "protein": 8,  "carbs": 50, "fat": 4},
        {"name": "Besan cheela with mint chutney",                    "calories": 250, "protein": 12, "carbs": 35, "fat": 7},
        {"name": "Sattu drink + banana",                              "calories": 220, "protein": 10, "carbs": 40, "fat": 2},
        {"name": "Greek yogurt with honey, seeds and fruit",          "calories": 230, "protein": 15, "carbs": 30, "fat": 6},
    ],
    "lunch": [
        {"name": "Brown rice + dal tadka + mixed sabji + salad",      "calories": 480, "protein": 18, "carbs": 72, "fat": 10},
        {"name": "Jowar roti + chana masala + raita",                 "calories": 450, "protein": 20, "carbs": 65, "fat": 9},
        {"name": "Vegetable khichdi + papad + pickle",                "calories": 420, "protein": 16, "carbs": 68, "fat": 8},
        {"name": "Rajma rice + cucumber raita",                       "calories": 490, "protein": 20, "carbs": 75, "fat": 9},
        {"name": "Paneer bhurji + 2 whole wheat rotis + dal soup",    "calories": 520, "protein": 24, "carbs": 55, "fat": 18},
        {"name": "Tofu stir-fry + multigrain roti + sabji",           "calories": 440, "protein": 22, "carbs": 50, "fat": 12},
        {"name": "Chole bhature (1 bhatura) + salad",                 "calories": 550, "protein": 18, "carbs": 70, "fat": 18},
        {"name": "Methi dal + 2 bajra rotis + curd",                  "calories": 430, "protein": 18, "carbs": 62, "fat": 10},
    ],
    "dinner": [
        {"name": "Moong dal soup + 1–2 rotis + sautéed greens",      "calories": 360, "protein": 16, "carbs": 52, "fat": 7},
        {"name": "Palak paneer + 1 roti + small curd rice",           "calories": 400, "protein": 18, "carbs": 45, "fat": 15},
        {"name": "Dal khichdi (light) + roasted papad",               "calories": 340, "protein": 14, "carbs": 55, "fat": 6},
        {"name": "Vegetable stew + appam (2)",                        "calories": 370, "protein": 10, "carbs": 60, "fat": 8},
        {"name": "Methi thepla + curd + green chutney",               "calories": 320, "protein": 10, "carbs": 48, "fat": 9},
        {"name": "Grilled tofu + sautéed vegetables + 1 roti",        "calories": 350, "protein": 20, "carbs": 38, "fat": 12},
        {"name": "Besan curry + 2 jowar rotis",                       "calories": 380, "protein": 16, "carbs": 54, "fat": 10},
        {"name": "Vegetable daliya (broken wheat) bowl",              "calories": 300, "protein": 10, "carbs": 50, "fat": 5},
    ],
    "snacks": [
        {"name": "Handful of mixed nuts (almonds, walnuts, cashews)", "calories": 170, "protein": 5,  "carbs": 8,  "fat": 14},
        {"name": "Fruit bowl (banana, apple, guava)",                 "calories": 130, "protein": 2,  "carbs": 32, "fat": 1},
        {"name": "Chaas (buttermilk) with curry leaves",              "calories":  60, "protein": 3,  "carbs": 7,  "fat": 2},
        {"name": "Roasted makhana — 1 bowl",                          "calories": 100, "protein": 4,  "carbs": 18, "fat": 1},
        {"name": "Murmura bhel (low oil)",                            "calories": 120, "protein": 3,  "carbs": 22, "fat": 3},
        {"name": "Greek yogurt / curd with honey and seeds",          "calories": 140, "protein": 9,  "carbs": 14, "fat": 5},
        {"name": "Boiled chana chaat with spices",                    "calories": 150, "protein": 9,  "carbs": 22, "fat": 2},
        {"name": "Cucumber slices with hummus",                       "calories":  90, "protein": 3,  "carbs": 10, "fat": 4},
    ],
}

MOTIVATIONAL_QUOTES = [
    "💪 Every rep brings you one step closer to your goal!",
    "🌟 Your only competition is yesterday's version of yourself.",
    "🔥 Sweat today, shine tomorrow!",
    "🎯 Small daily improvements lead to stunning long-term results.",
    "🏆 The pain of discipline is far less than the pain of regret.",
    "🌱 Progress, not perfection. Keep moving forward!",
    "⚡ You are stronger than you think. Believe it!",
    "🚀 Champions are made when no one is watching.",
    "🌈 Fitness is not a destination — it's a way of life.",
    "🧘 Strong body, calm mind — you're building both today.",
    "🦁 Do something today that your future self will thank you for.",
    "🏅 Fall seven times, stand up eight. Keep going!",
    "🌊 The harder you work for something, the greater you'll feel when you achieve it.",
    "⭐ You don't have to be great to start, but you have to start to be great.",
]

DAILY_TIPS = [
    "Drink a glass of water first thing in the morning.",
    "Lay out your workout clothes the night before.",
    "Do 5 minutes of movement — even on rest days.",
    "Track your meals for just 3 days to spot patterns.",
    "Sleep 7–8 hours — it's when your muscles actually grow.",
    "Replace one unhealthy snack with a fruit today.",
    "Stand up and stretch every 60 minutes at your desk.",
    "Add a 10-minute walk after lunch — it lowers blood sugar.",
    "Meal-prep on Sundays to eat healthy all week.",
    "Take the stairs instead of the lift today.",
    "Do 10 deep breaths before a stressful meeting.",
    "Eat your last meal at least 2 hours before bed.",
]


class FitnessService:
    """Service for generating personalised fitness content."""

    # ------------------------------------------------------------------
    # Workout Plan
    # ------------------------------------------------------------------
    @staticmethod
    def generate_weekly_plan(profile: dict) -> dict:
        """
        Generate a 7-day workout plan based on the user's profile.

        Expected profile keys:
            fitness_level (beginner/intermediate/advanced)
            goal (weight_loss/muscle_gain/endurance/flexibility/general)
            days_per_week (int 2–6)
            equipment (list of strings)
        """
        level = profile.get("fitness_level", "beginner").lower()
        goal  = profile.get("goal", "general").lower()
        days  = min(max(int(profile.get("days_per_week", 3)), 2), 6)

        exercises = EXERCISE_LIBRARY.get(level, EXERCISE_LIBRARY["beginner"])

        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        rest_days = sorted(random.sample(range(7), 7 - days))

        plan = {}
        ex_pool = exercises[:]
        random.shuffle(ex_pool)
        ex_idx = 0

        for i, day in enumerate(day_names):
            if i in rest_days:
                plan[day] = {
                    "type": "Rest / Active Recovery",
                    "exercises": [
                        {"name": "Light walk (20–30 min)",     "muscles": "Cardio, Recovery",  "duration": "30 min", "calories": 100, "tip": "Keep pace conversational."},
                        {"name": "Foam rolling / stretching",  "muscles": "Full Body",         "duration": "15 min", "calories": 30,  "tip": "Hold each position 30–60 sec."},
                    ],
                    "warmup": [],
                    "cooldown": [],
                    "notes": "Focus on hydration, sleep, and nutrition today.",
                    "estimated_calories": 130,
                }
            else:
                session_exercises = []
                num_exercises = 5 if level == "advanced" else 4
                for _ in range(num_exercises):
                    session_exercises.append(ex_pool[ex_idx % len(ex_pool)])
                    ex_idx += 1

                est_calories = sum(e.get("calories", 50) for e in session_exercises)
                day_type = FitnessService._day_type(goal, i)
                plan[day] = {
                    "type": day_type,
                    "exercises": session_exercises,
                    "warmup": WARMUP_ROUTINE[:5],
                    "cooldown": COOLDOWN_ROUTINE[:5],
                    "notes": FitnessService._day_note(goal),
                    "estimated_calories": est_calories + 50,  # +50 for warmup/cooldown
                }

        return {
            "plan": plan,
            "level": level,
            "goal": goal,
            "days_active": days,
            "tip": random.choice(MOTIVATIONAL_QUOTES),
            "weekly_calories": sum(
                d.get("estimated_calories", 0) for d in plan.values()
            ),
        }

    @staticmethod
    def _day_type(goal: str, day_idx: int) -> str:
        types_by_goal = {
            "weight_loss": ["HIIT Cardio", "Strength", "HIIT Cardio", "Strength", "HIIT Cardio", "Active Recovery"],
            "muscle_gain": ["Upper Body Push", "Lower Body", "Rest", "Upper Body Pull", "Full Body", "Legs"],
            "endurance":   ["Cardio Run", "Circuit", "Cardio Run", "Full Body", "Long Cardio", "Mobility"],
            "flexibility": ["Yoga Flow", "Stretch & Mobility", "Yoga Flow", "Pilates Core", "Full Body Stretch", "Yin Yoga"],
            "general":     ["Full Body", "Cardio", "Strength", "Yoga / Stretch", "Full Body", "Cardio"],
        }
        types = types_by_goal.get(goal, types_by_goal["general"])
        return types[day_idx % len(types)]

    @staticmethod
    def _day_note(goal: str) -> str:
        notes = {
            "weight_loss": "Keep rest periods short (30–45 sec) to maximise calorie burn. Track your heart rate.",
            "muscle_gain": "Rest 60–90 sec between sets. Focus on muscle-mind connection. Go close to failure.",
            "endurance":   "Maintain a steady pace (RPE 6–7). Track distance and time each session.",
            "flexibility": "Never force a stretch. Breathe deeply into each position. Hold 30–60 sec.",
            "general":     "Listen to your body. Modify any exercise if needed. Consistency is key.",
        }
        return notes.get(goal, notes["general"])

    # ------------------------------------------------------------------
    # Exercise Library
    # ------------------------------------------------------------------
    @staticmethod
    def get_exercise_library(level: str | None = None) -> dict:
        if level:
            return {level: EXERCISE_LIBRARY.get(level.lower(), [])}
        return EXERCISE_LIBRARY

    # ------------------------------------------------------------------
    # Yoga Library
    # ------------------------------------------------------------------
    @staticmethod
    def get_yoga_library(category: str | None = None) -> dict:
        if category:
            return {category: YOGA_LIBRARY.get(category.lower(), [])}
        return YOGA_LIBRARY

    # ------------------------------------------------------------------
    # Meal Suggestions
    # ------------------------------------------------------------------
    @staticmethod
    def get_meal_suggestions(diet_type: str = "vegetarian") -> dict:
        meals = {k: random.sample(v, min(3, len(v))) for k, v in INDIAN_MEALS.items()}
        if diet_type.lower() == "vegan":
            dairy = ["paneer", "curd", "chaas", "yogurt", "ghee", "butter", "milk"]
            for key in meals:
                filtered = [m for m in meals[key]
                            if not any(d in m["name"].lower() for d in dairy)]
                meals[key] = filtered if filtered else meals[key][:2]
        elif diet_type.lower() in ("high_protein", "high protein"):
            # Sort by protein descending
            for key in meals:
                meals[key] = sorted(meals[key], key=lambda m: m.get("protein", 0), reverse=True)[:3]
        elif diet_type.lower() in ("low_carb", "keto", "low carb"):
            for key in meals:
                meals[key] = sorted(meals[key], key=lambda m: m.get("carbs", 999))[:3]
        return meals

    # ------------------------------------------------------------------
    # Motivation
    # ------------------------------------------------------------------
    @staticmethod
    def get_daily_motivation() -> dict:
        return {
            "quote": random.choice(MOTIVATIONAL_QUOTES),
            "tip":   random.choice(DAILY_TIPS),
            "date":  datetime.now().strftime("%A, %d %B %Y"),
        }

    # ------------------------------------------------------------------
    # Warm-up / Cool-down
    # ------------------------------------------------------------------
    @staticmethod
    def get_warmup() -> list:
        return WARMUP_ROUTINE

    @staticmethod
    def get_cooldown() -> list:
        return COOLDOWN_ROUTINE
