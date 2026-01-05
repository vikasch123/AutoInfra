#!/usr/bin/env python3
"""
Simple test script for AutoInfra.ai API
Tests the /generate endpoint with sample inputs
"""

import requests
import json
import sys

API_URL = "http://localhost:8000"

def test_api():
    """Test the AutoInfra.ai API"""
    
    print("🧪 Testing AutoInfra.ai API\n")
    print("=" * 60)
    
    # Test 1: Check if server is running
    print("\n1️⃣ Testing server health...")
    try:
        response = requests.get(f"{API_URL}/", timeout=5)
        print(f"   ✅ Server is running (Status: {response.status_code})")
    except requests.exceptions.ConnectionError:
        print("   ❌ Server is not running!")
        print("   💡 Start the server with: python app.py")
        sys.exit(1)
    except Exception as e:
        print(f"   ❌ Error: {e}")
        sys.exit(1)
    
    # Test 2: Generate infrastructure
    print("\n2️⃣ Testing infrastructure generation...")
    test_cases = [
        {
            "name": "Basic Node.js + MongoDB",
            "description": "I want a Node.js app on AWS behind a load balancer with MongoDB in a secure VPC"
        },
        {
            "name": "High Availability Setup",
            "description": "I need a high-availability Node.js application on AWS with MongoDB database, load balancer, and secure networking"
        },
        {
            "name": "Simple Setup",
            "description": "Create a Node.js application with MongoDB on AWS"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n   Test {i}: {test_case['name']}")
        print(f"   Input: {test_case['description']}")
        
        try:
            response = requests.post(
                f"{API_URL}/generate",
                json={"description": test_case["description"]},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Success!")
                print(f"   📊 Intent extracted: {json.dumps(data['intent'], indent=6)}")
                print(f"   📝 Terraform code length: {len(data['terraform_code'])} characters")
                print(f"   🎨 Diagram generated: {len(data['diagram'])} characters")
                print(f"   📖 Explanation length: {len(data['explanation'])} characters")
                
                # Validate Terraform code has key components
                terraform = data['terraform_code']
                checks = {
                    "VPC": "aws_vpc" in terraform,
                    "ALB": "aws_lb" in terraform,
                    "EC2": "aws_instance" in terraform,
                    "Security Groups": "aws_security_group" in terraform,
                    "MongoDB": "mongodb" in terraform.lower()
                }
                
                print(f"   🔍 Validation:")
                for check, passed in checks.items():
                    status = "✅" if passed else "❌"
                    print(f"      {status} {check}")
                
            else:
                print(f"   ❌ Failed with status {response.status_code}")
                print(f"   Error: {response.text}")
        
        except requests.exceptions.Timeout:
            print("   ⏱️  Request timed out (>30s)")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("\n✅ Testing complete!")
    print("\n💡 Next steps:")
    print("   1. Open http://localhost:8000 in your browser")
    print("   2. Try different infrastructure descriptions")
    print("   3. Download and validate Terraform code with: terraform validate")


if __name__ == "__main__":
    try:
        test_api()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(0)
