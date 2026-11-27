# seed_db.py
"""
Database Seeder for POWERGRID Material Demand Forecasting System.
Populates realistic demo users, transmission line projects, and materials.
"""

import hashlib
from database import SessionLocal, engine, Base
import models
from models import User, Project, Material, Forecast

def hash_pw(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Create Demo User (ID: 1) if not exists
        demo_user = db.query(User).filter(User.id == 1).first()
        if not demo_user:
            demo_user = User(
                id=1,
                email="demo@powergrid.in",
                password_hash=hash_pw("powergrid123")
            )
            db.add(demo_user)
            db.commit()
            db.refresh(demo_user)
            print("✅ Created Demo User: demo@powergrid.in (ID: 1)")
        else:
            print("ℹ️ Demo User (ID: 1) already exists.")

        # 2. Seed Transmission Projects if none exist
        existing_projects = db.query(Project).filter(Project.user_id == 1).count()
        if existing_projects == 0:
            demo_projects = [
                {
                    "user_id": 1,
                    "project_name": "Nagpur - Wardha 765 kV D/C Transmission Corridor",
                    "project_budget": 6500.0,
                    "location": "Maharashtra",
                    "category": "Transmission",
                    "tower_type": "765kV D/C Lattice",
                    "terrain": "Plain",
                    "materials": [
                        ("Tower Steel", 28000.0, 1904000.0),
                        ("Conductor ACSR", 450.0, 2250000.0),
                        ("Insulator Discs (765kV)", 9200.0, 736000.0),
                        ("OPGW Telecomm Cable", 180.0, 360000.0),
                        ("Cement", 15000.0, 540000.0),
                    ]
                },
                {
                    "user_id": 1,
                    "project_name": "Bhadla - Bikaner 400 kV Solar Evacuation Link",
                    "project_budget": 4200.0,
                    "location": "Rajasthan",
                    "category": "Transmission",
                    "tower_type": "400kV D/C",
                    "terrain": "Desert",
                    "materials": [
                        ("Tower Steel", 19500.0, 1326000.0),
                        ("Conductor ACSR", 310.0, 1550000.0),
                        ("Insulator Discs (400kV)", 6400.0, 512000.0),
                        ("OPGW Telecomm Cable", 125.0, 250000.0),
                        ("Ready-Mix Concrete", 2200.0, 1100000.0),
                    ]
                },
                {
                    "user_id": 1,
                    "project_name": "Shimla - Mandi 220 kV Hill Terrain Interconnector",
                    "project_budget": 2800.0,
                    "location": "Himachal Pradesh",
                    "category": "Transmission",
                    "tower_type": "Narrow Base Guyed",
                    "terrain": "Hilly",
                    "materials": [
                        ("Tower Steel High Tensile", 12000.0, 816000.0),
                        ("HTLS High-Temp Conductor", 160.0, 1200000.0),
                        ("Composite Polymer Insulators", 4100.0, 492000.0),
                        ("Vibration Dampers", 1800.0, 216000.0),
                    ]
                }
            ]

            for p_data in demo_projects:
                mats = p_data.pop("materials")
                proj = Project(**p_data)
                db.add(proj)
                db.commit()
                db.refresh(proj)

                for m_name, qty, cost in mats:
                    mat = Material(
                        project_id=proj.id,
                        material_name=m_name,
                        quantity=qty,
                        cost=cost
                    )
                    db.add(mat)
                db.commit()
                print(f"✅ Seeded Project: {proj.project_name} (ID: {proj.id})")
        else:
            print(f"ℹ️ Projects already seeded ({existing_projects} existing projects).")

        print("🎉 Database seeding completed successfully!")

    except Exception as e:
        db.rollback()
        print(f"❌ Seeding error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
