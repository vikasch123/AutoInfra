import sys
from diagram_generator import DiagramGenerator

generator = DiagramGenerator()
# Simulate the request that likely caused the error
intent = {
    "app_count": 1,
    "region": "us-east-1",
    "app": "nodejs",
    "database": "mongodb",
    "architecture": "3-tier", # Implicitly from "high availability" usually
    "load_balancer": True
}

try:
    diagram = generator.generate(intent)
    print("--- DIAGRAM START ---")
    print(diagram)
    print("--- DIAGRAM END ---")
except Exception as e:
    print(f"Error: {e}")
