from diagram_generator import DiagramGenerator
import json

def test_diagrams():
    generator = DiagramGenerator()
    
    test_cases = [
        {
            "name": "3-Tier Node+Mongo+LB",
            "intent": {
                "app_count": 2,
                "region": "us-east-1",
                "app": "nodejs",
                "database": "mongodb",
                "architecture": "3-tier",
                "load_balancer": True
            }
        },
        {
            "name": "2-Tier Python+Postgres",
            "intent": {
                "app_count": 1,
                "region": "us-west-2",
                "app": "python",
                "database": "postgresql",
                "architecture": "2-tier",
                "load_balancer": False
            }
        }
    ]

    for test in test_cases:
        print(f"\n--- TEST CASE: {test['name']} ---")
        try:
            diagram = generator.generate(test['intent'])
            print(diagram)
        except Exception as e:
            print(f"FAILED: {e}")

if __name__ == "__main__":
    test_diagrams()
