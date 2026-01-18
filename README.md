# 🏙️ UrbanNexus: Intelligent Urban Monitoring System

**UrbanNexus** is a next-generation urban analytics platform designed to unify siloed city data—Weather, Traffic, Air Quality, and Agriculture—into a single intelligent ecosystem. It empowers city planners and citizens with real-time insights and predictive "What-If" simulations to build smarter, healthier cities.

---

## 🚀 Key Features

*   **⚡ Real-Time Dashboard:** Aggregates live data streams (Weather, AQI, Traffic) into a unified visual interface using the OpenWeatherMap API.
*   **🏥 Urban Health Index:** A proprietary algorithm that synthesizes environmental factors into a single **0-100 Livability Score**, providing instant situational awareness.
*   **e🧪 Interactive "What-If" Simulator:** A dynamic scenario lab where users can tweak variables (e.g., "Increase Traffic by 20%") to visualize cascading impacts on Air Quality and Crop Yields.
*   **🌍 Multi-City Explorer:** Browse and filter cities based on their current Health Risk levels (Low, Medium, High).
*   **🔄 Automated Data Pipeline:** Robust ETL (Extract, Transform, Load) jobs that sync, normalize, and archive live data into a PostgreSQL database.

---

## 🛠️ Technology Stack

**Frontend (User Experience)**
*   **Framework:** React.js (Vite)
*   **Styling:** Tailwind CSS (Premium Glassmorphism Design)
*   **Visualization:** Framer Motion (Animations), Lucide React (Icons)
*   **State Management:** React Hooks

**Backend (Intelligence & Logic)**
*   **Framework:** Django Access Framework (DRF)
*   **Language:** Python 3.10+
*   **Database:** PostgreSQL 15+
*   **AI/Analytics:** Scikit-Learn (Predictive Modeling), Pandas (Data Processing)
*   **External APIs:** OpenWeatherMap (Live Environmental Data)

---

## ⚙️ Installation & Setup

### Prerequisites
*   Node.js & npm
*   Python 3.10+
*   PostgreSQL

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/UrbanNexus.git
cd UrbanNexus
```

### 2. Backend Setup
```bash
cd Backend

# Create Virtual Environment
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate # Mac/Linux

# Install Dependencies
pip install -r requirements.txt

# Run Migrations
python manage.py migrate

# Start Server
python manage.py runserver
```
*The Backend will run at `http://localhost:8000`*

### 3. Frontend Setup
```bash
cd Frontend

# Install Node Modules
npm install

# Start Dev Server
npm run dev
```
*The Frontend will run at `http://localhost:5173`*

### 4. Environment Variables
Create a `.env` file in the root directory:
```env
DB_NAME=urbannexus_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
OPENWEATHER_API_KEY=your_api_key
```

---

## 📂 API Documentation

### **Data & Management**
| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/cities/` | `GET`, `POST` | List all cities or register a new city. |
| `/api/weather/` | `GET`, `POST` | Historical weather logs per city. |
| `/api/air-quality/` | `GET`, `POST` | Air quality (AQI, PM2.5) logs. |
| `/api/traffic/` | `GET`, `POST` | Traffic density and speed data. |
| `/api/agriculture/` | `GET`, `POST` | Crop yield and soil moisture sensors. |
| `/api/health/` | `GET`, `POST` | Historical Health Index/Risk logs. |

### **Analytics & Orchestration**
| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/dashboard/` | `GET` | **Main Dashboard:** Returns latest aggregated stats for a city (requires `city_id`). |
| `/api/sync/weather/` | `POST` | **On-Demand ETL:** Triggers a live sync with OpenWeatherMap API for all cities. |

---

## 📂 Project Structure

```
UrbanNexus/
├── Backend/                 # Django API & Logic
│   ├── analytics/           # AI Models & Risk Engines
│   │   ├── services/
│   │   │   ├── risk_engine.py      # Health Score Algorithm
│   │   │   └── scenario_engine.py  # Simulation Logic
│   ├── api/                 # REST Endpoints
│   │   ├── services/
│   │   │   └── weather_sync.py     # Live Data ETL Job
│   │   ├── models.py        # Database Schema
│   │   └── views.py         # API Controllers
│
├── Frontend/                # React UI
│   ├── src/
│   │   ├── components/      # Reusable UI (Navbar, Cards)
│   │   ├── pages/
│   │   │   ├── DashboardPage.jsx   # Main Real-time View
│   │   │   ├── SimulationPage.jsx  # What-If Lab
│   │   │   └── CitiesPage.jsx      # City Choice & Filters
│   │   └── services/        # API Integration (Axios)
│
└── README.md                # Documentation
```

**Developed with ❤️ by Team Try;Catch:Finally;**
