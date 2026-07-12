"""
IBM Watsonx.ai Service
Handles all communication with the IBM Watsonx.ai Granite models.
"""

import os
import time
import logging
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# AGENT INSTRUCTIONS — Edit this block to customise FitBuddy's behaviour.
# ─────────────────────────────────────────────────────────────────────────────
AGENT_INSTRUCTIONS = """You are FitBuddy — an expert, warm, and encouraging AI personal fitness coach powered by IBM Watsonx.ai.

## IDENTITY & PERSONA
- You are a certified personal trainer, nutritionist, and wellness coach in one.
- Friendly, empathetic, motivating — never shame, criticise, or discourage.
- Use simple, clear language. Avoid jargon unless the user is advanced.
- Use light humour to keep the conversation engaging.
- Always address the user by name if their profile includes one.

## RESPONSE FORMAT RULES
- Use **bold** for key terms, exercise names, and important numbers.
- Use bullet lists (- item) for plans, steps, and options.
- Use numbered lists (1. step) for ordered instructions or progressions.
- Use headings (## Heading) to organise long responses.
- Keep responses concise but complete — avoid padding or filler phrases.
- When giving a workout plan, always format as: Exercise name | Sets × Reps | Rest | Muscle group.
- When giving meal suggestions, include approximate calories and macros.
- End every response with a short motivational sign-off line.

## MOTIVATION STYLE
- Celebrate small wins enthusiastically.
- Use science-backed motivation: habit stacking, streak building, micro-goals.
- Remind users that consistency beats perfection.
- Provide gentle nudges when users express frustration or laziness.

## FITNESS EXPERTISE
- Expert in home workouts: bodyweight, resistance bands, dumbbells, kettlebells.
- Deep knowledge of yoga (asanas + breathing), pilates, HIIT, strength training, functional fitness, mobility work.
- Familiar with injury prevention, warm-up/cool-down protocols, and deload weeks.
- Certified-level understanding of periodisation, progressive overload, and RPE (Rate of Perceived Exertion).
- Can suggest modifications for injuries (bad knees, lower back pain, shoulder issues).

## INDIAN FITNESS & DIET SPECIALISATION
- Recommend Indian foods: dal, sabji, roti, rice, curd, chaas, paneer, sprouts, idli, dosa, poha, upma, sattu, makhana, and seasonal Indian fruits.
- Acknowledge Indian meal timings: light breakfast, moderate lunch (main meal), light dinner before 8 PM.
- Suggest yoga asanas (with Sanskrit + English names) alongside modern workouts.
- Respect Indian festival seasons — suggest flexible schedules around Diwali, Navratri, Ramzan, etc.
- Understand that many Indian households are vegetarian — default to vegetarian unless told otherwise.

## DIET STYLES SUPPORTED
- **Vegetarian** (default): No meat or fish. Dairy and eggs allowed if user permits.
- **Vegan**: No animal products. Emphasise tofu, tempeh, legumes, seeds, nuts.
- **High Protein**: Protein-dense foods at every meal. Target 1.6–2.2g per kg body weight.
- **Low Carb / Keto**: Reduce grains; increase healthy fats and proteins. Suggest cauliflower rice, etc.
- **Balanced**: 50% carbs / 25% protein / 25% fat macro split.
- **Diabetic-Friendly**: Low GI foods, smaller portions, no refined sugars.
- Adapt automatically based on the user's stated preference or profile.

## SAFETY & MEDICAL RULES
- ALWAYS recommend consulting a doctor before starting any new exercise program.
- NEVER provide medical diagnoses or prescribe medications.
- Flag if BMI < 15 or > 40 — urge immediate medical consultation.
- For users 60+ or with stated conditions (diabetes, hypertension, PCOD, arthritis), suggest low-impact only.
- Remind users to stay hydrated (at least 2–3L/day) and take mandatory rest days.
- If a user reports sharp/sudden pain, tell them to STOP immediately and consult a doctor.

## WORKOUT INTENSITY GUIDELINES
- **Beginner**: 2–3 days/week, 20–30 min, bodyweight, low impact, RPE 4–6.
- **Intermediate**: 3–5 days/week, 30–45 min, moderate intensity, RPE 6–7.
- **Advanced**: 5–6 days/week, 45–60 min, progressive overload, compound movements, RPE 7–9.
- Always include warm-up (5–10 min) and cool-down (5–10 min) in every plan.
- Include deload week every 4–6 weeks for intermediate/advanced users.

## COACHING STYLE
- Ask clarifying questions before building any plan (goals, schedule, limitations, equipment).
- Break large goals into SMART weekly milestones.
- Give step-by-step instructions with form cues for every exercise.
- Provide 3–5 alternatives for every exercise.
- Track progress verbally — acknowledge improvements from previous messages.
- When a user completes a milestone, celebrate it enthusiastically.

## LANGUAGE & UNITS
- Default: English. Respond in Hindi/Hinglish if the user writes that way.
- Metric units (kg, cm, km) by default. Offer imperial if requested.
- Use Indian number formatting where appropriate (lakh, crore, etc.).

## SCOPE LIMITS
- Discuss only fitness, nutrition, wellness, sleep, stress management, and healthy lifestyle.
- Politely redirect all off-topic questions back to fitness and health.
- No financial, legal, or political advice.
"""
# ─────────────────────────────────────────────────────────────────────────────


class WatsonxService:
    """Singleton service class for IBM Watsonx.ai inference."""

    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialised = False
        return cls._instance

    def __init__(self):
        if self._initialised:
            return
        self._initialised = True

        self.api_key    = os.getenv("IBM_API_KEY", "")
        self.project_id = os.getenv("IBM_PROJECT_ID", "")
        self.url        = os.getenv("IBM_URL", "https://us-south.ml.cloud.ibm.com")
        self.model_id   = os.getenv("MODEL_ID", "ibm/granite-3-3-8b-instruct")
        self.max_tokens = int(os.getenv("MAX_TOKENS", "2048"))
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))
        self.top_p       = float(os.getenv("TOP_P", "0.9"))
        self._connect()

    # ------------------------------------------------------------------
    # Connection
    # ------------------------------------------------------------------
    def _connect(self):
        """Establish connection to IBM Watsonx.ai."""
        if not self.api_key or not self.project_id:
            logger.warning(
                "IBM_API_KEY or IBM_PROJECT_ID not set — running in demo mode."
            )
            return

        try:
            credentials = Credentials(url=self.url, api_key=self.api_key)
            self._model = ModelInference(
                model_id=self.model_id,
                credentials=credentials,
                project_id=self.project_id,
                params={
                    GenParams.MAX_NEW_TOKENS:     self.max_tokens,
                    GenParams.TEMPERATURE:        self.temperature,
                    GenParams.TOP_P:              self.top_p,
                    GenParams.REPETITION_PENALTY: 1.1,
                    GenParams.STOP_SEQUENCES:     ["User:", "\n\nUser:"],
                },
            )
            logger.info("WatsonxService connected — model: %s", self.model_id)
        except Exception as exc:
            msg = str(exc)
            if "BXNIM0462E" in msg or "API key is disabled" in msg:
                logger.error(
                    "WatsonxService: IBM API key is disabled. "
                    "Go to IBM Cloud → Manage → IAM → API keys and create a new key, "
                    "then update IBM_API_KEY in your .env file."
                )
            else:
                logger.error("WatsonxService connection failed: %s", exc)
            self._model = None

    def reconnect(self):
        """Force a fresh connection attempt (useful after credential update)."""
        self._model = None
        self._connect()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def is_connected(self) -> bool:
        return self._model is not None

    def generate(self, user_message: str, context: dict | None = None) -> str:
        """
        Generate a response from Granite given a user message and optional context.

        Args:
            user_message: The raw user input.
            context: Optional dict with keys: profile, history, intent.

        Returns:
            AI-generated response string.
        """
        ctx = context or {}
        prompt = self._build_prompt(user_message, ctx)

        if not self._model:
            return self._demo_response(user_message)

        # Retry once on transient failures
        for attempt in range(2):
            try:
                result = self._model.generate_text(prompt=prompt)
                if isinstance(result, dict):
                    text = result.get("results", [{}])[0].get("generated_text", "")
                else:
                    text = str(result)
                text = text.strip()
                # Remove any leaked prompt artefacts
                for stop in ["User:", "FitBuddy:", "CONVERSATION HISTORY"]:
                    if stop in text:
                        text = text.split(stop)[0].strip()
                return text or "I didn't quite get that — could you rephrase?"
            except Exception as exc:
                logger.warning("Watsonx attempt %d failed: %s", attempt + 1, exc)
                if attempt == 0:
                    time.sleep(1)

        return (
            "⚠️ I'm having trouble reaching my AI brain right now. "
            "Please check your IBM credentials and try again shortly."
        )

    def generate_suggestion(self, profile: dict) -> str:
        """Generate a proactive fitness tip based on the user's profile."""
        if not profile:
            return random_tip()
        prompt = (
            f"{AGENT_INSTRUCTIONS.strip()}\n\n"
            f"USER PROFILE: {_profile_summary(profile)}\n\n"
            "Give ONE short (2–3 sentence) personalised fitness tip for today. "
            "Make it specific to their goal and level. No preamble.\nFitBuddy:"
        )
        if not self._model:
            return random_tip()
        try:
            result = self._model.generate_text(prompt=prompt)
            return (str(result) if not isinstance(result, dict)
                    else result.get("results", [{}])[0].get("generated_text", "")).strip()
        except Exception as exc:
            logger.error("generate_suggestion error: %s", exc)
            return random_tip()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------
    def _build_prompt(self, user_message: str, context: dict) -> str:
        """Compose a rich prompt with system instructions, profile, and history."""
        parts = [AGENT_INSTRUCTIONS.strip(), ""]

        # User profile injection
        profile_raw = context.get("profile")
        if profile_raw:
            if isinstance(profile_raw, dict):
                parts.append(f"## ACTIVE USER PROFILE\n{_profile_summary(profile_raw)}")
            else:
                parts.append(f"## ACTIVE USER PROFILE\n{profile_raw}")
            parts.append("")

        # Conversation history (last 8 turns)
        history = context.get("history", [])
        if history:
            parts.append("## CONVERSATION HISTORY (most recent last)")
            for turn in history[-8:]:
                role = "User" if turn.get("role") == "user" else "FitBuddy"
                parts.append(f"{role}: {turn.get('content', '').strip()}")
            parts.append("")

        parts.append(f"User: {user_message}")
        parts.append("FitBuddy:")
        return "\n".join(parts)

    @staticmethod
    def _demo_response(user_message: str) -> str:
        """Rich fallback demo responses when credentials are not configured."""
        msg = user_message.lower()
        if any(w in msg for w in ["bmi", "weight", "height", "overweight", "underweight"]):
            return (
                "🏋️ **BMI Analysis**\n\n"
                "Head to the **BMI Calculator** tab — enter your height and weight, "
                "and I'll give you:\n"
                "- Your BMI category (Underweight / Normal / Overweight / Obese)\n"
                "- Ideal weight range\n"
                "- Personalised diet & exercise recommendations\n\n"
                "*(Demo mode — add your IBM Watsonx credentials in `.env` to unlock full AI)*"
            )
        if any(w in msg for w in ["workout", "exercise", "plan", "training", "gym", "hiit", "cardio"]):
            return (
                "💪 **Personalised Workout Plan**\n\n"
                "Go to the **Workout Planner** tab, fill in:\n"
                "- Fitness level (Beginner / Intermediate / Advanced)\n"
                "- Your goal (Weight Loss / Muscle Gain / Endurance / Flexibility)\n"
                "- Days per week\n\n"
                "I'll generate a full 7-day plan with warm-up, exercises, sets/reps, and cool-down!\n\n"
                "*(Demo mode — add your IBM Watsonx credentials in `.env` to unlock full AI)*"
            )
        if any(w in msg for w in ["diet", "food", "nutrition", "meal", "eat", "calories", "protein"]):
            return (
                "🥗 **Nutrition Guidance**\n\n"
                "Tell me your diet preference and I'll suggest balanced Indian meals:\n"
                "- 🌱 Vegetarian / Vegan\n"
                "- 🥚 High Protein\n"
                "- 🌾 Low Carb / Keto\n"
                "- ⚖️ Balanced (50/25/25 macros)\n\n"
                "*(Demo mode — add your IBM Watsonx credentials in `.env` to unlock full AI)*"
            )
        if any(w in msg for w in ["yoga", "stretch", "flexibility", "meditation", "breathing"]):
            return (
                "🧘 **Yoga & Flexibility**\n\n"
                "I can guide you through:\n"
                "- Morning yoga flows (Surya Namaskar, Yin Yoga)\n"
                "- Targeted stretches for back pain, tight hips, stiff shoulders\n"
                "- Pranayama (breathing exercises) for stress and energy\n\n"
                "*(Demo mode — add your IBM Watsonx credentials in `.env` to unlock full AI)*"
            )
        if any(w in msg for w in ["water", "hydration", "drink"]):
            return (
                "💧 **Hydration Guide**\n\n"
                "Use the **Calculator** tab to get your exact daily water target based on "
                "your weight and activity level.\n\n"
                "Quick rule: **weight (kg) × 33 ml** per day, plus extra for exercise.\n\n"
                "*(Demo mode — add your IBM Watsonx credentials in `.env` to unlock full AI)*"
            )
        if any(w in msg for w in ["motivat", "inspire", "quote", "tired", "lazy", "give up"]):
            return (
                "🔥 **You've Got This!**\n\n"
                "> *\"The pain of discipline is far less than the pain of regret.\"*\n\n"
                "Every workout you do is a promise kept to yourself. "
                "Even 10 minutes today is better than zero. Start small — momentum builds!\n\n"
                "*(Demo mode — add your IBM Watsonx credentials in `.env` to unlock full AI)*"
            )
        return (
            "👋 **Hi! I'm FitBuddy**, your AI personal fitness coach.\n\n"
            "I can help with:\n"
            "- 🏋️ Personalised workout plans\n"
            "- 🥗 Nutrition & meal suggestions\n"
            "- 📊 BMI, calorie & water intake analysis\n"
            "- 🧘 Yoga & flexibility routines\n"
            "- 💪 Exercise form & injury prevention\n"
            "- 🌟 Daily motivation & habit building\n\n"
            "*(Demo mode — add your IBM Watsonx credentials in `.env` to unlock full AI)*"
        )


def _profile_summary(profile: dict) -> str:
    """Convert a profile dict to a concise string for prompt injection."""
    parts = []
    if profile.get("name"):       parts.append(f"Name: {profile['name']}")
    if profile.get("age"):        parts.append(f"Age: {profile['age']}")
    if profile.get("gender"):     parts.append(f"Gender: {profile['gender']}")
    if profile.get("height"):     parts.append(f"Height: {profile['height']} cm")
    if profile.get("weight"):     parts.append(f"Weight: {profile['weight']} kg")
    if profile.get("fitness_level"): parts.append(f"Fitness Level: {profile['fitness_level']}")
    if profile.get("goal"):       parts.append(f"Goal: {profile['goal']}")
    if profile.get("diet"):       parts.append(f"Diet: {profile['diet']}")
    if profile.get("activity_level"): parts.append(f"Activity: {profile['activity_level']}")
    if profile.get("health_notes"): parts.append(f"Health Notes: {profile['health_notes']}")
    if profile.get("equipment"):  parts.append(f"Equipment: {', '.join(profile['equipment'])}")
    return " | ".join(parts) if parts else "No profile data."


def random_tip() -> str:
    import random
    tips = [
        "💧 Drink a glass of water right now — hydration boosts energy and focus.",
        "🌅 A 10-minute morning walk sets a positive tone for the entire day.",
        "🥗 Add one extra vegetable to your next meal — small changes compound.",
        "😴 Sleep 7–8 hours tonight — it's when your muscles actually repair and grow.",
        "🧘 Take 3 deep belly breaths right now to reduce cortisol instantly.",
        "🏃 Even 5 minutes of movement breaks the sedentary cycle — start there.",
        "💪 Progressive overload = add 1 more rep or 1 more kg each week.",
        "🎯 Write down your fitness goal today — written goals are 42% more likely to be achieved.",
    ]
    return random.choice(tips)
