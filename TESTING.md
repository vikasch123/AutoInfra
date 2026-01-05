# Testing Guide for AutoInfra.ai

This guide covers multiple ways to test the AutoInfra.ai PoC system.

## 🚀 Quick Start Testing

### Method 1: Web UI Testing (Recommended)

1. **Start the server:**
   ```bash
   cd AutoInfra
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python app.py
   ```

2. **Open your browser:**
   Navigate to `http://localhost:8000`

3. **Test with sample inputs:**
   - Basic: `"I want a Node.js app on AWS behind a load balancer with MongoDB in a secure VPC"`
   - High Availability: `"I need a high-availability Node.js application on AWS with MongoDB database, load balancer, and secure networking"`
   - Simple: `"Create a Node.js application with MongoDB on AWS"`

4. **Verify output:**
   - Check Terraform code tab for generated code
   - Check Architecture Diagram tab for Mermaid diagram
   - Check Explanation tab for infrastructure overview
   - Download Terraform code and validate

---

### Method 2: API Testing with Test Script

1. **Start the server** (in one terminal):
   ```bash
   python app.py
   ```

2. **Run the test script** (in another terminal):
   ```bash
   python test_api.py
   ```

   This will:
   - Check if server is running
   - Test multiple infrastructure descriptions
   - Validate generated Terraform components
   - Show extracted intent

---

### Method 3: Manual API Testing with cURL

1. **Start the server:**
   ```bash
   python app.py
   ```

2. **Test the API:**
   ```bash
   curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{
       "description": "I want a Node.js app on AWS behind a load balancer with MongoDB in a secure VPC"
     }'
   ```

3. **Save output to file:**
   ```bash
   curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{"description": "I want a Node.js app on AWS behind a load balancer with MongoDB in a secure VPC"}' \
     -o response.json
   ```

---

### Method 4: Python Interactive Testing

```python
import requests
import json

# Test the API
response = requests.post(
    "http://localhost:8000/generate",
    json={
        "description": "I want a Node.js app on AWS behind a load balancer with MongoDB in a secure VPC"
    }
)

data = response.json()

# Print results
print("Intent:", json.dumps(data['intent'], indent=2))
print("\nTerraform Code (first 500 chars):")
print(data['terraform_code'][:500])
print("\nDiagram:")
print(data['diagram'])
```

---

## ✅ Validation Checklist

### 1. Server Health
- [ ] Server starts without errors
- [ ] Root endpoint (`/`) returns frontend or API message
- [ ] CORS is enabled (no CORS errors in browser console)

### 2. Intent Extraction
- [ ] Extracts `cloud: "aws"` correctly
- [ ] Extracts `app: "nodejs"` correctly
- [ ] Extracts `database: "mongodb"` correctly
- [ ] Detects high availability (sets `app_count: 2`)
- [ ] Falls back to mock mode if no API key

### 3. Terraform Generation
- [ ] Generated code is valid Terraform syntax
- [ ] Contains VPC resources (`aws_vpc`)
- [ ] Contains ALB resources (`aws_lb`)
- [ ] Contains EC2 instances (`aws_instance`)
- [ ] Contains Security Groups (`aws_security_group`)
- [ ] Contains MongoDB instance
- [ ] Variables are properly injected
- [ ] No hardcoded credentials

### 4. Diagram Generation
- [ ] Mermaid diagram is valid
- [ ] Shows VPC structure
- [ ] Shows ALB
- [ ] Shows EC2 instances (correct count)
- [ ] Shows MongoDB
- [ ] Shows network connections

### 5. Frontend
- [ ] Page loads correctly
- [ ] Input field accepts text
- [ ] Generate button works
- [ ] Loading indicator shows
- [ ] Results display in tabs
- [ ] Terraform code is syntax-highlighted
- [ ] Diagram renders correctly
- [ ] Download button works

---

## 🔍 Detailed Testing Scenarios

### Scenario 1: Basic Infrastructure
**Input:**
```
I want a Node.js app on AWS behind a load balancer with MongoDB in a secure VPC
```

**Expected Output:**
- `app_count: 1`
- `availability: "standard"`
- Terraform with 1 EC2 app instance
- MongoDB instance in private subnet
- ALB configured

### Scenario 2: High Availability
**Input:**
```
I need a high-availability Node.js application on AWS with MongoDB database, load balancer, and secure networking
```

**Expected Output:**
- `app_count: 2`
- `availability: "high"`
- Terraform with 2 EC2 app instances
- Both instances attached to ALB target group

### Scenario 3: Error Handling
**Input:**
```
(empty string)
```

**Expected Output:**
- Frontend shows error message
- API returns 422 validation error

---

## 🛠️ Terraform Validation

After generating Terraform code:

1. **Save to file:**
   ```bash
   # Copy generated Terraform code to a file
   mkdir test-terraform
   cd test-terraform
   # Paste Terraform code into main.tf
   ```

2. **Initialize Terraform:**
   ```bash
   terraform init
   ```

3. **Validate syntax:**
   ```bash
   terraform validate
   ```

4. **Format code:**
   ```bash
   terraform fmt
   ```

5. **Plan (dry-run):**
   ```bash
   terraform plan
   ```
   
   ⚠️ **Note:** This requires AWS credentials configured. For PoC, syntax validation is sufficient.

---

## 🐛 Troubleshooting

### Server won't start
- Check if port 8000 is already in use
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python3 --version` (needs 3.8+)

### API returns 500 error
- Check server logs for error messages
- Verify Terraform templates exist in `terraform_templates/`
- Check if Jinja2 is installed

### Frontend doesn't load
- Verify `static/index.html` exists
- Check browser console for errors
- Ensure server is running on correct port

### Diagram doesn't render
- Check browser console for Mermaid errors
- Verify Mermaid CDN is accessible
- Check if diagram syntax is valid

### Mock mode not working
- Verify `intent_extractor.py` has mock fallback
- Check if OpenAI API key is set (mock mode activates when not set)

---

## 📊 Performance Testing

Test response times:

```bash
time curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"description": "I want a Node.js app on AWS behind a load balancer with MongoDB in a secure VPC"}'
```

Expected: < 5 seconds (with mock mode) or < 10 seconds (with OpenAI API)

---

## 🎯 Success Criteria

Your testing is successful if:
- ✅ Server starts without errors
- ✅ Web UI loads and is functional
- ✅ API accepts natural language input
- ✅ Terraform code is generated and valid
- ✅ Diagram renders correctly
- ✅ Explanation is clear and accurate
- ✅ No hardcoded credentials in output
- ✅ Response time < 5 seconds (mock) or < 10 seconds (API)

---

## 📝 Test Report Template

```
Test Date: ___________
Tester: ___________

Environment:
- Python Version: ___________
- OS: ___________
- OpenAI API Key: [ ] Set [ ] Not Set (Mock Mode)

Results:
- Server Startup: [ ] Pass [ ] Fail
- Web UI: [ ] Pass [ ] Fail
- API Endpoint: [ ] Pass [ ] Fail
- Intent Extraction: [ ] Pass [ ] Fail
- Terraform Generation: [ ] Pass [ ] Fail
- Diagram Generation: [ ] Pass [ ] Fail
- Response Time: ___________

Issues Found:
1. ___________
2. ___________

Notes:
___________
```

---

Happy Testing! 🚀
