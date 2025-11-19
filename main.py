import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from database import db, create_document, get_documents
from schemas import Service, Project, Inquiry

app = FastAPI(title="RofaTech API", version="1.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "RofaTech Backend Running"}


# SERVICES
@app.get("/api/services", response_model=List[Service])
def list_services():
    try:
        items = get_documents("service")
        result = []
        for it in items:
            it.pop("_id", None)
            result.append(it)
        return result
    except Exception:
        # Fallback demo services if DB not connected
        return [
            Service(title="Web Development", slug="web-development", description="Modern websites and web apps.", features=["Next.js / React", "Fast, SEO-friendly", "Custom integrations"], icon="Code2", featured=True).model_dump(),
            Service(title="Content Creation", slug="content-creation", description="Copy, visuals, and videos that convert.", features=["Social content", "Explainer videos", "Brand design"], icon="PenTool", featured=True).model_dump(),
            Service(title="Website Maintenance", slug="website-maintenance", description="Ongoing updates and monitoring.", features=["Performance checks", "Security & backups", "Uptime monitoring"], icon="Wrench" ).model_dump(),
            Service(title="Social Media Marketing", slug="social-media-marketing", description="Grow your audience and conversions.", features=["Strategy & planning", "Paid ads", "Analytics"], icon="Share2").model_dump(),
        ]

@app.post("/api/services")
def create_service(payload: Service):
    try:
        _id = create_document("service", payload)
        return {"status": "ok", "id": _id}
    except Exception:
        raise HTTPException(status_code=500, detail="Database not available")


# PROJECTS
@app.get("/api/projects", response_model=List[Project])
def list_projects():
    try:
        items = get_documents("project")
        result = []
        for it in items:
            it.pop("_id", None)
            result.append(it)
        return result
    except Exception:
        return [
            Project(title="E-commerce Revamp", slug="ecommerce-revamp", summary="Performance-focused storefront redesign.", image="https://images.unsplash.com/photo-1523275335684-37898b6baf30", tags=["Next.js", "Stripe"], featured=True).model_dump(),
            Project(title="SaaS Dashboard", slug="saas-dashboard", summary="Clean analytics dashboard with role-based access.", image="https://images.unsplash.com/photo-1556157382-97eda2d62296", tags=["React", "Tailwind"], featured=True).model_dump(),
        ]

@app.post("/api/projects")
def create_project(payload: Project):
    try:
        _id = create_document("project", payload)
        return {"status": "ok", "id": _id}
    except Exception:
        raise HTTPException(status_code=500, detail="Database not available")


# INQUIRIES
@app.post("/api/inquiries")
def create_inquiry(payload: Inquiry):
    try:
        _id = create_document("inquiry", payload)
        return {"status": "ok", "id": _id}
    except Exception:
        # Accept even without DB to not block demo
        return {"status": "ok", "id": None}

@app.get("/api/inquiries")
def list_inquiries():
    try:
        items = get_documents("inquiry")
        result = []
        for it in items:
            it["id"] = str(it.pop("_id", ""))
            result.append(it)
        return result
    except Exception:
        # no fallback for inquiries
        return []


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = getattr(db, "name", None) or ("✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set")
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
