#  Object Detection System — FastAPI

A production-ready REST API for real-time object detection using YOLOv8,
built with FastAPI, MongoDB, and Streamlit dashboard.


##  Features

-  Detect 80+ objects using YOLOv8 pretrained model
-  User authentication with JWT tokens
-  Save detection history to MongoDB
-  Streamlit dashboard for easy interaction
-  Fast and lightweight REST API
-  Per-user detection history


##  Tech Stack

| Layer | Technology |
|-------|-----------|
| ML Model | YOLOv8 (Ultralytics) |
| Backend | FastAPI |
| Database | MongoDB |
| Frontend | Streamlit |
| Authentication | JWT + bcrypt |
| Language | Python 3.10+ |


##  Project Structure

\`\`\`
object-detection-system/
├── main.py                  # FastAPI application
├── model/
│   └── detector.py          # YOLOv8 detection logic
├── database/
│   ├── db.py                # MongoDB connection
│   └── models.py            # Data schema
├── auth/
│   └── auth.py              # JWT authentication
├── frontend/
│   └── streamlit_app.py     # Streamlit dashboard
├── .env                     # Environment variables
├── .gitignore
└── requirements.txt
\`\`\`

---

##  Installation & Setup

### Prerequisites
- Python 3.10+
- MongoDB installed locally
- Git

### 1. Clone the repository
\`\`\`bash
git clone https://github.com/Piyush05062006/object-detection-system--fast-Api
cd object-detection-system--fast-Api
\`\`\`

### 2. Create virtual environment
\`\`\`bash
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux
\`\`\`

### 3. Install dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Create .env file
\`\`\`
MONGO_URL=mongodb://localhost:27017
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
\`\`\`

---

##  Running the Project

You need 3 terminals running simultaneously:

**Terminal 1 — Start MongoDB:**
\`\`\`bash
mongod
\`\`\`

**Terminal 2 — Start FastAPI:**
\`\`\`bash
uvicorn main:app --reload
\`\`\`

**Terminal 3 — Start Streamlit:**
\`\`\`bash
streamlit run frontend/streamlit_app.py
\`\`\`

- API runs at: http://localhost:8000
- Swagger docs at: http://localhost:8000/docs
- Streamlit dashboard at: http://localhost:8501

---

