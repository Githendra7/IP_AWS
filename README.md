# ProtoStruc: Professional Engineering Design Platform

ProtoStruc is an enterprise-grade, AI-assisted product development ecosystem designed to streamline and automate hardware and software engineering methodologies. By leveraging cutting-edge multi-agent systems via LangGraph, ProtoStruc handles **Functional Decomposition**, **Morphological Analysis**, and **Risk Mitigation** directly inside a clean, comprehensive dashboard.

---

## ⚡ Tech Stack Overview

### Frontend
- **Framework**: Next.js (App Router)
- **Styling**: Tailwind CSS + shadcn/ui components
- **Icons**: Lucide React
- **Animations**: Framer Motion

### Backend
- **Core API**: FastAPI (Python)
- **AI Orchestration**: LangGraph
- **LLM Capabilities**: Groq API (`llama-3.3-70b-versatile`)
- **Database / Auth**: Supabase (PostgreSQL)

---

## 📂 Repository Structure

The architecture is divided into two highly modular environments.

```text
IP_Deployment/
├── frontend/                 # Next.js Presentation Layer
│   ├── src/app/              # Dedicated routing (Login, Projects, Resets)
│   ├── src/components/       # Reusable React & Sidebar modules
│   └── src/lib/              # Standard frontend SDK and Hooks
├── backend/                  # FastAPI & AI Engine
│   ├── app/ai/               # LangGraph multi-agent logic
│   ├── app/api/              # JWT-secured network handlers
│   └── app/models/           # Pydantic schemas and database bindings
├── ARCHITECTURE.md           # Technical blueprint for the multi-agent AI flow
└── DEPLOYMENT.md             # Standard Operating Procedures for Vercel & Render
```

## 🚀 Getting Started

### 1. Database Setup
Ensure you have a connected Supabase cluster with the appropriate `users`, `password_resets`, and relational tables provisioned.

### 2. Run Backend (Local)
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 3. Run Frontend (Local)
```bash
cd frontend
npm install
npm run dev
```

For extended details into how the system logic parses information, refer to `ARCHITECTURE.md`. For live hosting mechanics, reference `DEPLOYMENT.md`.
