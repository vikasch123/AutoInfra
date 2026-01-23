from diagram_generator import DiagramGenerator
import json
import codecs

def debug():
    generator = DiagramGenerator()
    intent = {
        "app_count": 1,
        "region": "us-east-1",
        "app": "nodejs",
        "database": "mongodb",
        "architecture": "3-tier",
        "load_balancer": True
    }
    
    try:
        diagram = generator.generate(intent)
        with codecs.open("debug_output.txt", "w", "utf-8") as f:
            f.write(diagram)
        print("Diagram written to debug_output.txt")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug()
