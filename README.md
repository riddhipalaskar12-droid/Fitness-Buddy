# 🏋️ AI Fitness Buddy — IBM Watsonx.ai Llama

> A fully-featured AI-powered personal fitness coach built with **Python Flask** and **IBM Watsonx.ai Llama models**. Includes a beautiful responsive frontend, AI chat, BMI/BMR calculators, weekly workout planner, family profiles, progress dashboard, and more.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-green?logo=flask)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?logo=bootstrap)
![IBM Watsonx](https://img.shields.io/badge/IBM-Watsonx.ai-0062FF?logo=ibm)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 **AI Chat Coach** | Powered by Meta Llama 3.3 70B Instruct via IBM Watsonx.ai |
| 📊 **BMI Calculator** | Full analysis with health category and recommendations |
| 🔥 **BMR & Calories** | Mifflin-St Jeor formula + activity multipliers + Chart.js visualisation |
| 💧 **Water Intake** | Personalised hydration calculator with daily schedule |
| 📅 **Weekly Planner** | AI-generated 7-day workout plans by level/goal/equipment |
| 📈 **Progress Dashboard** | BMI trends, calorie burn charts, streak tracker, daily goals |
| 👨‍👩‍👧‍👦 **Family Profiles** | Multiple member support with individual personalisation |
| 🥗 **Meal Suggestions** | Indian & international meals by diet preference |
| 🌙 **Dark Mode** | Smooth light/dark toggle persisted in localStorage |
| 📱 **Fully Responsive** | Bootstrap 5 + custom CSS, works on all screen sizes |

---

## 🏗️ Project Structure

```
ai-fitness-buddy/
├── app.py                    # Flask entry point
├── .env                      # Your credentials (gitignored)
├── .env.example              # Template — copy to .env
├── requirements.txt          # Python dependencies
├── README.md
│
├── routes/
│   ├── __init__.py
│   ├── chat.py               # /api/chat/*  — AI chat endpoints
│   ├── fitness.py            # /api/fitness/* — plans, meals, motivation
│   ├── calculator.py         # /api/calculator/* — BMI, BMR, water
│   └── profile.py            # /api/profiles/* — family profile CRUD
│
├── services/
│   ├── __init__.py
│   ├── watsonx_service.py    # IBM Watsonx.ai SDK + AGENT_INSTRUCTIONS
│   ├── fitness_service.py    # Workout plans, exercise library, meals
│   └── calculator_service.py # BMI, BMR, TDEE, water calculations
│
├── templates/
│   ├── base.html             # Shared layout (navbar, footer, theme)
│   ├── index.html            # Landing page
│   ├── chat.html             # AI chat interface
│   ├── calculator.html       # BMI / BMR / Water calculators
│   ├── planner.html          # Weekly workout planner
│   ├── dashboard.html        # Progress dashboard
│   ├── profiles.html         # Family profile management
│   └── 404.html              # Error page
│
└── static/
    ├── css/
    │   └── style.css         # Full custom stylesheet (dark mode, animations)
    └── js/
        ├── app.js            # Shared utilities: theme, toast, FitApp helpers
        ├── index.js          # Landing page: motivation ticker, quick BMI
        ├── chat.js           # Chat UI logic
        ├── calculator.js     # Calculator forms + Chart.js
        ├── planner.js        # Workout planner + exercise library
        ├── dashboard.js      # Dashboard charts + goals + workout log
        └── profiles.js       # Family profile CRUD UI
```

---

## 🚀 Quick Start (Local)

### 1. Prerequisites

- Python 3.10 or higher
- pip
- An IBM Cloud account with Watsonx.ai access

### 2. Clone the repository

```bash
git clone https://github.com/your-username/ai-fitness-buddy.git
cd ai-fitness-buddy
```

### 3. Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure credentials

```bash
cp .env.example .env
```

Open `.env` and fill in your IBM credentials:

```env
IBM_API_KEY=your_ibm_cloud_api_key_here
IBM_PROJECT_ID=your_watsonx_project_id_here
IBM_URL=https://us-south.ml.cloud.ibm.com
MODEL_ID=meta-llama/llama-3-3-70b-instruct

FLASK_SECRET_KEY=generate_a_long_random_string_here
FLASK_ENV=development
FLASK_DEBUG=True
APP_NAME=AI Fitness Buddy
MAX_TOKENS=1024
TEMPERATURE=0.7
TOP_P=0.9
```

### 6. Run the app

```bash
python app.py
```

Open your browser: **http://localhost:5000**

---

## 🔑 IBM Cloud Configuration

### Step 1 — Create an IBM Cloud Account
Go to [cloud.ibm.com](https://cloud.ibm.com) and sign up for a free account.

### Step 2 — Create a Watsonx.ai Project
1. Navigate to **IBM Watsonx** → [watsonx.ai](https://dataplatform.cloud.ibm.com/wx/home)
2. Click **Create a project** → **Create an empty project**
3. Give it a name (e.g., "FitBuddy") and click **Create**
4. Copy the **Project ID** from the project URL or settings

### Step 3 — Generate an API Key
1. Go to **Manage** → **Access (IAM)** → **API Keys**
2. Click **Create** → give it a name → **Create**
3. Copy the API key immediately (shown only once)

### Step 4 — Get the Service URL
- Default US South: `https://us-south.ml.cloud.ibm.com`
- EU Frankfurt: `https://eu-de.ml.cloud.ibm.com`
- Japan Tokyo: `https://jp-tok.ml.cloud.ibm.com`

### Step 5 — Enable Llama Model Access
1. In your Watsonx project, go to **Manage** → **Services and integrations**
2. Add **Watson Machine Learning** service
3. Enable **Meta Llama** models from the model catalog

---

## 🤖 Customising the AI Agent

The AI personality, tone, and capabilities are fully configurable in `services/watsonx_service.py`.

Find the `AGENT_INSTRUCTIONS` block (around line 18) and edit any section:

```python
AGENT_INSTRUCTIONS = """
You are FitBuddy — a warm, encouraging, and knowledgeable AI fitness coach.

PERSONALITY & TONE
- Friendly, motivating, empathetic, and professional.
...

INDIAN FITNESS & DIET PREFERENCES
- Recommend Indian foods: dal, sabji, roti, rice...

DIET STYLES SUPPORTED
- Vegetarian (default)
- Vegan
- High Protein
...
"""
```

**Customisable sections:**
- `PERSONALITY & TONE` — Agent character, language style
- `MOTIVATION STYLE` — Encouragement frequency and approach
- `FITNESS SPECIALISATION` — Training modalities (yoga, HIIT, strength, etc.)
- `INDIAN FITNESS & DIET PREFERENCES` — Indian food, meal timings, yoga
- `DIET STYLES SUPPORTED` — Vegetarian / Vegan / High Protein / Keto
- `SAFETY RULES` — Medical disclaimers, injury prevention
- `WORKOUT INTENSITY GUIDELINES` — Beginner / Intermediate / Advanced parameters
- `COACHING STYLE` — Question-first approach, progressive milestones
- `LANGUAGE` — English / Hindi / Hinglish auto-detect
- `ENCOURAGEMENT FREQUENCY` — How often to celebrate wins

---

## 🌐 API Reference

### Chat
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/chat/send` | Send message, get AI response |
| `GET` | `/api/chat/history` | Get session chat history |
| `POST` | `/api/chat/clear` | Clear chat history |
| `GET` | `/api/chat/status` | Check Watsonx connection status |

### Calculators
| Method | Endpoint | Body |
|---|---|---|
| `POST` | `/api/calculator/bmi` | `{ weight, height }` |
| `POST` | `/api/calculator/bmr` | `{ weight, height, age, gender, activity_level }` |
| `POST` | `/api/calculator/water` | `{ weight, activity_level }` |

### Fitness
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/fitness/workout-plan` | Generate 7-day plan |
| `GET` | `/api/fitness/exercises?level=` | Exercise library |
| `GET` | `/api/fitness/meals?diet=` | Meal suggestions |
| `GET` | `/api/fitness/motivation` | Daily motivation |
| `GET` | `/api/fitness/warmup` | Warm-up routine |
| `GET` | `/api/fitness/cooldown` | Cool-down routine |

### Profiles
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/profiles/` | List all profiles |
| `POST` | `/api/profiles/` | Create profile |
| `GET` | `/api/profiles/<id>` | Get profile |
| `PUT` | `/api/profiles/<id>` | Update profile |
| `DELETE` | `/api/profiles/<id>` | Delete profile |
| `POST` | `/api/profiles/<id>/activate` | Set active profile for chat |
| `POST` | `/api/profiles/<id>/bmi` | Log BMI reading |

---

## 🌍 Deployment Guide

### Option 1 — IBM Cloud Code Engine

```bash
# Install IBM Cloud CLI
# https://cloud.ibm.com/docs/cli

ibmcloud login
ibmcloud target -r us-south -g Default

# Create Code Engine project
ibmcloud ce project create --name fitbuddy

# Deploy from container registry or GitHub
ibmcloud ce application create \
  --name fitbuddy-app \
  --image us.icr.io/your-namespace/fitbuddy \
  --cpu 0.5 \
  --memory 1G \
  --port 5000 \
  --env IBM_API_KEY=your_key \
  --env IBM_PROJECT_ID=your_id \
  --env IBM_URL=https://us-south.ml.cloud.ibm.com

ibmcloud ce application get --name fitbuddy-app
```

### Option 2 — Render.com (Free Tier)

1. Push code to GitHub
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your GitHub repo
4. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn -w 2 -b 0.0.0.0:$PORT app:app`
5. Add environment variables in the Render dashboard
6. Deploy!

### Option 3 — Railway

1. Install Railway CLI: `npm install -g @railway/cli`
2. Run:
```bash
railway login
railway init
railway up
railway variables set IBM_API_KEY=your_key
railway variables set IBM_PROJECT_ID=your_id
railway variables set IBM_URL=https://us-south.ml.cloud.ibm.com
```

### Option 4 — Docker

```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

```bash
docker build -t fitbuddy .
docker run -p 5000:5000 \
  -e IBM_API_KEY=your_key \
  -e IBM_PROJECT_ID=your_id \
  -e IBM_URL=https://us-south.ml.cloud.ibm.com \
  fitbuddy
```

---

## 📦 requirements.txt

```
Flask==3.0.3
python-dotenv==1.0.1
ibm-watsonx-ai==1.1.2
requests==2.32.3
Werkzeug==3.0.3
gunicorn==22.0.0
flask-cors==4.0.1
```

---

## 🔒 Security Notes

- Never commit your `.env` file — it's listed in `.gitignore`
- Use environment variables in all production deployments
- Rotate your IBM API key periodically
- The `FLASK_SECRET_KEY` should be a long random string in production:
  ```bash
  python -c "import secrets; print(secrets.token_hex(32))"
  ```

---

## 🛠️ Demo Mode

If IBM credentials are not configured, the app runs in **Demo Mode**:
- The AI chat returns helpful pre-programmed responses
- All calculators, planner, and dashboard work fully
- A red indicator in the navbar shows "Demo Mode"
- Simply add credentials to `.env` to activate full AI

---

## 📜 License

MIT License — feel free to use, modify, and distribute.

---

## 🙏 Acknowledgements

- [IBM Watsonx.ai](https://www.ibm.com/watsonx) — Llama models
- [Bootstrap 5](https://getbootstrap.com) — UI framework
- [Font Awesome](https://fontawesome.com) — Icons
- [Chart.js](https://www.chartjs.org) — Data visualisation
- [Google Fonts — Inter & Poppins](https://fonts.google.com)
