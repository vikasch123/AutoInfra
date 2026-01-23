import requests
import json

def test_backend_response():
    url = "http://localhost:8000/generate"
    payload = {
        "description": "I want a scalable golang app with postgresql as database and along with a loadbalancer and nginx as reverse proxy"
    }
    
    try:
        print("Sending request to backend...")
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        data = response.json()
        diagram = data.get("diagram", "")
        
        print("\n--- RAW DIAGRAM STRING from JSON ---")
        print(diagram)
        print("------------------------------------")
        
        # Save to file to check for hidden characters
        with open("backend_response_diagram.txt", "w", encoding="utf-8") as f:
            f.write(diagram)
            
        print("Diagram saved to backend_response_diagram.txt")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_backend_response()
