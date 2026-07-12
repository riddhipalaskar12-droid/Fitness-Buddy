"""
Calculator Service
Handles BMI, BMR, TDEE, water intake, macro, and body fat calculations.
"""


class CalculatorService:
    """Pure-function service for health and fitness calculations."""

    # ------------------------------------------------------------------
    # BMI
    # ------------------------------------------------------------------
    @staticmethod
    def calculate_bmi(weight_kg: float, height_cm: float) -> dict:
        """Return BMI value, category, colour, advice, and recommendations."""
        if height_cm <= 0 or weight_kg <= 0:
            raise ValueError("Height and weight must be positive values.")

        height_m = height_cm / 100
        bmi = round(weight_kg / (height_m ** 2), 1)

        if bmi < 16:
            category = "Severely Underweight"
            color = "danger"
            advice = (
                "Your BMI indicates severe underweight. Please consult a doctor "
                "and a registered dietitian immediately."
            )
            recommendations = [
                "Consult a physician urgently.",
                "Increase caloric intake with nutrient-dense foods.",
                "Include healthy fats: nuts, avocado, ghee (in moderation).",
                "Avoid intense exercise until weight is stable.",
            ]
        elif bmi < 18.5:
            category = "Underweight"
            color = "warning"
            advice = "You are slightly underweight. Focus on a calorie surplus with wholesome foods."
            recommendations = [
                "Eat 300–500 kcal above your TDEE daily.",
                "Include protein at every meal (dal, paneer, eggs, tofu).",
                "Light strength training 3×/week to build muscle.",
                "Eat 5–6 smaller meals instead of 3 large ones.",
            ]
        elif bmi < 25:
            category = "Normal Weight"
            color = "success"
            advice = "Great! Your BMI is in the healthy range. Keep up the good work."
            recommendations = [
                "Maintain current dietary habits.",
                "Exercise 150 min/week (cardio + strength).",
                "Stay hydrated — at least 2.5 L water/day.",
                "Annual health check-ups to track vitals.",
            ]
        elif bmi < 30:
            category = "Overweight"
            color = "warning"
            advice = (
                "You are slightly overweight. A moderate calorie deficit and "
                "regular exercise will help you reach a healthy weight."
            )
            recommendations = [
                "Create a 300–500 kcal daily deficit.",
                "Walk 7,000–10,000 steps per day.",
                "Reduce refined carbs and sugary drinks.",
                "Include HIIT 2–3×/week alongside strength training.",
            ]
        elif bmi < 35:
            category = "Obese Class I"
            color = "danger"
            advice = (
                "BMI indicates Class I obesity. Structured diet and exercise changes "
                "will significantly improve your health markers."
            )
            recommendations = [
                "Consult a doctor before starting intense exercise.",
                "Begin with low-impact activities: walking, swimming, yoga.",
                "Track calories using an app (target 500 kcal deficit/day).",
                "Focus on whole foods; eliminate ultra-processed items.",
            ]
        else:
            category = "Obese Class II / III"
            color = "danger"
            advice = (
                "BMI indicates significant obesity. Medical supervision is strongly "
                "recommended before any exercise or diet program."
            )
            recommendations = [
                "Seek medical supervision immediately.",
                "Work with a dietitian for a structured meal plan.",
                "Start with chair exercises and gentle walking.",
                "Address underlying conditions (thyroid, PCOD, etc.).",
            ]

        # Ideal weight range (BMI 18.5–24.9)
        ideal_min = round(18.5 * (height_m ** 2), 1)
        ideal_max = round(24.9 * (height_m ** 2), 1)
        weight_to_lose = round(weight_kg - ideal_max, 1) if weight_kg > ideal_max else 0
        weight_to_gain = round(ideal_min - weight_kg, 1) if weight_kg < ideal_min else 0

        return {
            "bmi": bmi,
            "category": category,
            "color": color,
            "advice": advice,
            "recommendations": recommendations,
            "ideal_weight_min": ideal_min,
            "ideal_weight_max": ideal_max,
            "weight_to_lose": weight_to_lose,
            "weight_to_gain": weight_to_gain,
        }

    # ------------------------------------------------------------------
    # BMR & TDEE
    # ------------------------------------------------------------------
    @staticmethod
    def calculate_bmr_tdee(
        weight_kg: float,
        height_cm: float,
        age: int,
        gender: str,
        activity_level: str,
    ) -> dict:
        """Mifflin-St Jeor BMR + activity multiplier for TDEE."""
        if gender.lower() in ("male", "m"):
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
        else:
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

        multipliers = {
            "sedentary":   1.2,
            "light":       1.375,
            "moderate":    1.55,
            "active":      1.725,
            "very_active": 1.9,
        }
        multiplier = multipliers.get(activity_level.lower(), 1.55)
        tdee = round(bmr * multiplier)
        bmr  = round(bmr)

        return {
            "bmr":          bmr,
            "tdee":         tdee,
            "weight_loss":  tdee - 500,
            "weight_gain":  tdee + 300,
            "maintenance":  tdee,
            "activity_multiplier": multiplier,
        }

    # ------------------------------------------------------------------
    # Water Intake
    # ------------------------------------------------------------------
    @staticmethod
    def calculate_water_intake(weight_kg: float, activity_level: str) -> dict:
        """Recommend daily water intake in litres."""
        base_litres = weight_kg * 0.033
        activity_bonus = {
            "sedentary": 0, "light": 0.3, "moderate": 0.5,
            "active": 0.7, "very_active": 1.0,
        }
        bonus = activity_bonus.get(activity_level.lower(), 0.3)
        total = round(base_litres + bonus, 1)
        glasses = round(total / 0.25)

        return {
            "litres": total,
            "glasses": glasses,
            "schedule": [
                "1 glass on waking (before brushing)",
                "1 glass 30 min before breakfast",
                "1–2 glasses mid-morning",
                "1 glass before lunch",
                "1–2 glasses afternoon",
                "1 glass 30 min before dinner",
                "1 glass before bed",
            ],
        }

    # ------------------------------------------------------------------
    # Macronutrient Calculator
    # ------------------------------------------------------------------
    @staticmethod
    def calculate_macros(tdee: float, goal: str, diet_type: str = "balanced") -> dict:
        """
        Calculate daily macro targets (protein, carbs, fat) in grams.

        Args:
            tdee: Total Daily Energy Expenditure in kcal.
            goal: weight_loss | weight_gain | maintenance | muscle_gain.
            diet_type: balanced | high_protein | low_carb | keto.
        """
        # Adjust calories per goal
        calorie_targets = {
            "weight_loss":  tdee - 500,
            "weight_gain":  tdee + 300,
            "muscle_gain":  tdee + 200,
            "maintenance":  tdee,
        }
        target_kcal = calorie_targets.get(goal.lower(), tdee)

        # Macro splits (protein%, carb%, fat%)
        splits = {
            "balanced":     (0.25, 0.50, 0.25),
            "high_protein": (0.35, 0.40, 0.25),
            "low_carb":     (0.30, 0.25, 0.45),
            "keto":         (0.25, 0.05, 0.70),
        }
        p_pct, c_pct, f_pct = splits.get(diet_type.lower(), splits["balanced"])

        protein_g = round((target_kcal * p_pct) / 4)
        carbs_g   = round((target_kcal * c_pct) / 4)
        fat_g     = round((target_kcal * f_pct) / 9)

        return {
            "target_calories": round(target_kcal),
            "protein_g":       protein_g,
            "carbs_g":         carbs_g,
            "fat_g":           fat_g,
            "diet_type":       diet_type,
            "goal":            goal,
            "tips": {
                "protein": f"Aim for {protein_g}g protein/day — dal, paneer, tofu, eggs, sprouts.",
                "carbs":   f"Aim for {carbs_g}g carbs/day — prefer whole grains, oats, brown rice.",
                "fat":     f"Aim for {fat_g}g fat/day — nuts, ghee (small), olive oil, seeds.",
            },
        }

    # ------------------------------------------------------------------
    # Body Fat Estimate (U.S. Navy Method)
    # ------------------------------------------------------------------
    @staticmethod
    def estimate_body_fat(
        gender: str,
        waist_cm: float,
        neck_cm: float,
        height_cm: float,
        hip_cm: float = 0.0,
    ) -> dict:
        """
        U.S. Navy body fat formula.
        For females, hip_cm is required.
        """
        import math
        gender = gender.lower()
        if gender in ("male", "m"):
            if waist_cm <= neck_cm:
                raise ValueError("Waist must be larger than neck.")
            bf = 495 / (1.0324 - 0.19077 * math.log10(waist_cm - neck_cm) + 0.15456 * math.log10(height_cm)) - 450
        else:
            if not hip_cm:
                raise ValueError("Hip measurement is required for females.")
            bf = 495 / (1.29579 - 0.35004 * math.log10(waist_cm + hip_cm - neck_cm) + 0.22100 * math.log10(height_cm)) - 450

        bf = round(bf, 1)

        # Category
        if gender in ("male", "m"):
            if bf < 6:      cat, color = "Essential Fat",   "warning"
            elif bf < 14:   cat, color = "Athletic",        "success"
            elif bf < 18:   cat, color = "Fitness",         "success"
            elif bf < 25:   cat, color = "Average",         "warning"
            else:           cat, color = "Above Average",   "danger"
        else:
            if bf < 14:     cat, color = "Essential Fat",   "warning"
            elif bf < 21:   cat, color = "Athletic",        "success"
            elif bf < 25:   cat, color = "Fitness",         "success"
            elif bf < 32:   cat, color = "Average",         "warning"
            else:           cat, color = "Above Average",   "danger"

        return {
            "body_fat_pct": bf,
            "category":     cat,
            "color":        color,
            "lean_mass_pct": round(100 - bf, 1),
        }
