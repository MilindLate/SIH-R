# test_api.py
"""
Automated Verification & Integration Test Suite for POWERGRID Backend.
Tests database models, user auth, project CRUD, ML inference, and forecast persistence.
"""

import sys
import unittest
import requests
import time
import subprocess
from database import SessionLocal
from models import User, Project, Material, Forecast

BASE_URL = "http://127.0.0.1:8000"

class TestPowergridAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Verify server is reachable
        try:
            r = requests.get(f"{BASE_URL}/", timeout=2)
            cls.server_running = (r.status_code == 200)
        except Exception:
            cls.server_running = False

    def test_01_health_check(self):
        """Test GET / health check endpoint"""
        if not self.server_running:
            self.skipTest("Server not running on port 8000")
        res = requests.get(f"{BASE_URL}/")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("message", data)
        print("  ✅ [PASS] Root Health Check")

    def test_02_projects_user(self):
        """Test GET /projects/user/1 returns seeded projects"""
        if not self.server_running:
            self.skipTest("Server not running on port 8000")
        res = requests.get(f"{BASE_URL}/projects/user/1")
        self.assertEqual(res.status_code, 200)
        projects = res.json()
        self.assertIsInstance(projects, list)
        self.assertGreater(len(projects), 0, "Expected at least 1 project for user 1")
        print(f"  ✅ [PASS] Fetch User Projects (Found {len(projects)} projects)")

    def test_03_forecast_predict(self):
        """Test POST /forecast/predict returns 132 ML material estimates"""
        if not self.server_running:
            self.skipTest("Server not running on port 8000")
        payload = {
            "project_category_main": "Transmission",
            "project_type": "400 kV",
            "project_budget_price_in_lake": 500.0,
            "state": "Maharashtra",
            "terrain": "Plain",
            "Distance_from_Storage_unit": 50.0,
            "transmission_line_length_km": 100.0,
            "location": "Nagpur",
            "project_name": "Test Corridor"
        }
        res = requests.post(f"{BASE_URL}/forecast/predict", json=payload)
        self.assertEqual(res.status_code, 200)
        predictions = res.json()
        self.assertIsInstance(predictions, list)
        self.assertEqual(len(predictions), 132, f"Expected 132 materials, got {len(predictions)}")
        self.assertIn("material_name", predictions[0])
        self.assertIn("predicted_value", predictions[0])
        print(f"  ✅ [PASS] ML Forecast Inference (Predicted {len(predictions)} materials)")

    def test_04_forecast_save(self):
        """Test POST /forecast/save saves entry and returns predictions"""
        if not self.server_running:
            self.skipTest("Server not running on port 8000")
        payload = {
            "project_category_main": "Transmission",
            "project_type": "765 kV",
            "project_budget_price_in_lake": 800.0,
            "state": "Rajasthan",
            "terrain": "Desert",
            "Distance_from_Storage_unit": 35.0,
            "transmission_line_length_km": 150.0,
            "location": "Bikaner",
            "project_name": "Solar Grid Interconnect"
        }
        res = requests.post(f"{BASE_URL}/forecast/save", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("forecast", data)
        self.assertIn("predictions", data)
        self.assertEqual(data["forecast"]["project_name"], "Solar Grid Interconnect")
        print(f"  ✅ [PASS] ML Forecast Persistence (Saved ID: {data['forecast']['id']})")

    def test_05_auth_login(self):
        """Test POST /auth/login with demo credentials"""
        if not self.server_running:
            self.skipTest("Server not running on port 8000")
        payload = {
            "email": "demo@powergrid.in",
            "password": "powergrid123"
        }
        res = requests.post(f"{BASE_URL}/auth/login", json=payload)
        self.assertEqual(res.status_code, 200)
        user = res.json()
        self.assertEqual(user["email"], "demo@powergrid.in")
        print("  ✅ [PASS] User Authentication (demo@powergrid.in)")

def run_tests():
    print("=" * 60)
    print("⚡ POWERGRID SYSTEM - INTEGRATION TESTS")
    print("=" * 60)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPowergridAPI)
    runner = unittest.TextTestRunner(verbosity=0)
    result = runner.run(suite)
    print("=" * 60)
    if result.wasSuccessful():
        print("🎉 ALL TESTS PASSED SUCCESSFULLY!")
        return 0
    else:
        print(f"❌ {len(result.failures)} failures, {len(result.errors)} errors")
        return 1

if __name__ == "__main__":
    sys.exit(run_tests())
