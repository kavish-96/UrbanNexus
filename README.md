# 🏙️ UrbanNexus
> **Data-Driven Urban Systems for Sustainable, Healthy and Agriculturally-Supported Smart Cities**

UrbanNexus is a unified digital platform that breaks down data silos between **Urban Planning, Public Health, Agriculture, and Traffic**. It aggregates real-time data from 4 distinct sectors, processes it through a central Django backend, and visualizes cross-sector analytics on an interactive React dashboard.

---

## 🚀 Key Features
*   **Unified Dashboard**: View real-time Air Quality, Traffic, and Health metrics in one place.
*   **Cross-Sector Analytics**: See how Traffic Jams affect Air Quality, and how Pollution spikes impact Health Risk scores.
*   **Time-Series Tracking**: Historical data logging for Weather, Crop Yields, and Hospital Admissions.
*   **Simulation Engine**: "What-if" scenario analyzer for urban planners.
*   **Live Connect**: Zero-deployment local network system for instant team collaboration.

---

## 🛠️ Tech Stack
| Domain | Technologies |
| :--- | :--- |
| **Frontend** | React, Vite, TailwindCSS, Recharts, Lucide Icons |
| **Backend** | Django 5.2, Django REST Framework, Python 3.10 |
| **Database** | PostgreSQL |
| **DevOps** | Dotenv, CORS, Git Flow |

---

## 📦 Setup & How to Run Locally

### 1. Prerequisites
*   Node.js & npm
*   Python 3.10+
*   PostgreSQL (Local or Cloud)

### 2. Backend Setup (Django)
Open a terminal in the `Backend/` folder:

```bash
# 1. Create Virtual Environment
python -m venv venv
# Windows: .\venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# 2. Install Dependencies
pip install -r requirements.txt

# 3. Create .env file (See below) and configure DB

# 4. Migrate Database
python manage.py migrate

# 5. Run Server (Exposed on 0.0.0.0 for LAN access)
python manage.py runserver 0.0.0.0:8000
```
> The API will be available at `http://localhost:8000/api/`

### 3. Frontend Setup (React)
Open a new terminal in the `Frontend/` folder:

```bash
# 1. Install Dependencies
npm install

# 2. Configure API Endpoint
# Edit src/services/api.js if the backend IP changes.

# 3. Run Dev Server
npm run dev
```

---

## � Backend API Reference

**Base URL**: `http://localhost:8000/api/`

| Resource | Method | URL | Description |
| :--- | :--- | :--- | :--- |
| **City Dashboard** | `GET` | `/dashboard/?city_id=1` | **Main Aggregation API**. Returns Latest Weather, AQI, Traffic, Health Stats. |
| **Cities** | `GET`/`POST` | `/cities/` | Manage supported cities list. |
| **Weather** | `GET`/`POST` | `/weather/` | Daily weather logs (Temp, Humidity). |
| **Air Quality** | `GET`/`POST` | `/air-quality/` | Daily Pollution logs (AQI, PM2.5). |
| **Traffic** | `GET`/`POST` | `/traffic/` | Daily congestion levels & speed. |
| **Agriculture** | `GET`/`POST` | `/agriculture/` | Crop yields & soil moisture logs. |
| **Health** | `GET`/`POST` | `/health/` | Derived health risk scores. |

> For detailed JSON payloads, see [Backend/API_DOCS.md](Backend/API_DOCS.md).

---

## �🔑 Environment Variables
Create a `.env` file inside the `Backend/` folder.
**Note: This file is ignored by Git for security.**

```ini
# Backend/.env
DB_NAME=urbannexus_db
DB_USER=postgres
DB_PASSWORD=your_real_password
DB_HOST=localhost
DB_PORT=5432

# Optional
DEBUG=True
SECRET_KEY=dev-secret-key
```

---

## ⚠️ Basic Error Handling
*   **`OperationalError: connection to server failed`**: Ensure PostgreSQL is running and your `.env` password is correct.
*   **`ModuleNotFoundError`**: Ensure you activated the virtual environment (`venv`) before running `python manage.py`.
*   **`Network Error` (Frontend)**: Verify that `api.js` points to the correct Backend IP Address (if running on different machines).

---

## 🔒 Security Statement
*   **No Secrets in Repo**: All sensitive keys (DB Passwords, Secret Keys) are stored in `.env` files which are included in `.gitignore`.
*   **Local LAN Access**: Use of `0.0.0.0` is for development/demo purposes only. For production, use Gunicorn/Nginx.
