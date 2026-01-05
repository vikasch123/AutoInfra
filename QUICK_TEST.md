# Quick Testing Guide

## 🚀 Fastest Way to Test

### Step 1: Start the Server

```bash
cd AutoInfra
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 2: Test via Web Browser (Easiest)

1. Open: **http://localhost:8000**
2. Enter this in the text box:
   ```
   I want a Node.js app on AWS behind a load balancer with MongoDB in a secure VPC
   ```
3. Click **"Generate Infrastructure"**
4. Wait a few seconds
5. Check the three tabs:
   - **Terraform Code**: Should show generated Terraform
   - **Architecture Diagram**: Should show a Mermaid diagram
   - **Explanation**: Should show infrastructure overview

### Step 3: Test via API Script

In a **new terminal** (keep server running):

```bash
cd AutoInfra
source venv/bin/activate
python test_api.py
```

This will run automated tests and show you:
- ✅ Server health check
- ✅ Intent extraction results
- ✅ Terraform validation
- ✅ Component checks

### Step 4: Test via cURL (Command Line)

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"description": "I want a Node.js app on AWS behind a load balancer with MongoDB in a secure VPC"}' \
  | python -m json.tool
```

---

## ✅ What to Check

1. **Server starts** without errors
2. **Web page loads** at http://localhost:8000
3. **Generate button works** and shows loading
4. **Terraform code** appears (should contain `aws_vpc`, `aws_lb`, `aws_instance`)
5. **Diagram renders** (should show VPC, ALB, EC2, MongoDB)
6. **Explanation** is readable

---

## 🐛 Common Issues

**Port 8000 already in use?**
```bash
# Use a different port
uvicorn app:app --port 8001
```

**Module not found?**
```bash
# Make sure you're in the AutoInfra directory
cd AutoInfra
# And virtual environment is activated
source venv/bin/activate
```

**Frontend not loading?**
- Check that `static/index.html` exists
- Check browser console (F12) for errors

---

## 📝 Test Examples

Try these different inputs:

1. **Basic:**
   ```
   I want a Node.js app on AWS behind a load balancer with MongoDB in a secure VPC
   ```

2. **High Availability:**
   ```
   I need a high-availability Node.js application on AWS with MongoDB database, load balancer, and secure networking
   ```

3. **Simple:**
   ```
   Create a Node.js application with MongoDB on AWS
   ```

---

That's it! 🎉
