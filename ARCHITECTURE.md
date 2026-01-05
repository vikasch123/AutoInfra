# AutoInfra.ai - System Architecture & Data Flow

## 📊 Complete Data Flow Diagram

```
User Input (Natural Language)
    ↓
┌─────────────────────────────────────┐
│  FastAPI Backend (/generate)        │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Step 1: Intent Extraction         │
│  - IntentExtractor.extract_intent() │
│  - Uses LLM (OpenAI) or Mock Mode   │
└─────────────────────────────────────┘
    ↓
    Intent JSON: {
      "app": "golang",
      "database": "mysql",
      "architecture": "2-tier",
      ...
    }
    ↓
┌─────────────────────────────────────┐
│  Step 2: Terraform Generation       │
│  - TerraformGenerator.generate()     │
│  - Jinja2 Template Rendering         │
└─────────────────────────────────────┘
    ↓
    Terraform Code (String)
    ↓
┌─────────────────────────────────────┐
│  Step 3: Diagram Generation         │
│  - DiagramGenerator.generate()      │
│  - Mermaid Syntax Generation        │
└─────────────────────────────────────┘
    ↓
    Mermaid Diagram Code (String)
    ↓
┌─────────────────────────────────────┐
│  Step 4: Code Validation            │
│  - TerraformValidator.validate()    │
│  - Pattern Matching & Analysis      │
└─────────────────────────────────────┘
    ↓
    Validation Results: {
      "valid": true,
      "errors": [],
      "warnings": [...],
      "suggestions": [...]
    }
    ↓
┌─────────────────────────────────────┐
│  Step 5: Cost Estimation            │
│  - CostEstimator.estimate()         │
│  - Pricing Lookup & Calculation    │
└─────────────────────────────────────┘
    ↓
    Cost Data: {
      "monthly_cost": 25.50,
      "breakdown": {...},
      "tips": [...]
    }
    ↓
┌─────────────────────────────────────┐
│  Step 6: Security Analysis          │
│  - SecurityAnalyzer.analyze()       │
│  - Pattern Matching & Scoring       │
└─────────────────────────────────────┘
    ↓
    Security Data: {
      "security_score": 85,
      "findings": [...],
      "recommendations": [...]
    }
    ↓
┌─────────────────────────────────────┐
│  Step 7: Explanation Generation     │
│  - _generate_explanation()          │
│  - Template-based Text Generation   │
└─────────────────────────────────────┘
    ↓
    Explanation (Markdown String)
    ↓
┌─────────────────────────────────────┐
│  Response Assembly                  │
│  - InfrastructureResponse Model     │
└─────────────────────────────────────┘
    ↓
JSON Response to Frontend
    ↓
Frontend Rendering
    - Display in Tabs
    - Render Mermaid Diagram
    - Show Validation Results
    - Display Cost Breakdown
    - Show Security Analysis
```

## 🔍 Detailed Component Breakdown

### 1. Intent Extraction (`intent_extractor.py`)

**How it works:**
```python
# Two modes:

# Mode 1: LLM-based (with OpenAI API key)
OpenAI GPT-3.5-turbo → System Prompt → JSON Response
  ↓
Parse JSON → Validate → Return Intent

# Mode 2: Mock Mode (keyword-based, no API key)
Description Text → Keyword Matching → Intent Dictionary
```

**Process:**
1. **Check for API key**: If `OPENAI_API_KEY` exists, use LLM mode
2. **LLM Mode**:
   - Send system prompt with JSON schema to GPT-3.5-turbo
   - System prompt instructs: "Extract infrastructure intent as JSON"
   - LLM analyzes natural language and returns structured JSON
   - Parse and validate the JSON response
3. **Mock Mode** (fallback):
   - Use keyword matching (e.g., "golang" → app: "golang")
   - Pattern matching for database types
   - Simple logic for architecture detection

**Example:**
```python
Input: "I want a golang app with mysql database"

Mock Mode Process:
1. Check for "golang" or "go" → app = "golang"
2. Check for "mysql" → database = "mysql"
3. No "load balancer" mentioned → load_balancer = False
4. No "high availability" → availability = "standard"

Output Intent:
{
  "app": "golang",
  "database": "mysql",
  "architecture": "2-tier",
  "load_balancer": False,
  ...
}
```

---

### 2. Terraform Generation (`terraform_generator.py`)

**How it works:**
```python
Intent Dictionary → Jinja2 Templates → Rendered Terraform Code
```

**Process:**
1. **Load Templates**: Read Jinja2 template files from `terraform_templates/`
   - `main.tf.j2` - Main infrastructure resources
   - `variables.tf.j2` - Variable definitions
   - `outputs.tf.j2` - Output values

2. **Prepare Variables**: Extract values from intent
   ```python
   template_vars = {
       "app": "golang",
       "database": "mysql",
       "app_count": 1,
       "load_balancer": False,
       ...
   }
   ```

3. **Template Rendering**: Jinja2 processes templates with variables
   ```jinja2
   {% if load_balancer %}
   resource "aws_lb" "main" { ... }
   {% endif %}
   
   {% for i in range(1, app_count + 1) %}
   resource "aws_instance" "app{{ i }}" { ... }
   {% endfor %}
   ```

4. **Combine**: Merge all rendered templates into single Terraform code string

**Example:**
```python
Intent: {"app": "golang", "database": "mysql", "app_count": 1}

Template Processing:
- main.tf.j2 checks: database != "none" → includes database resources
- main.tf.j2 checks: load_balancer == False → skips ALB resources
- Loop: app_count = 1 → creates 1 EC2 instance
- User data: app == "golang" → includes Go installation script

Output: Complete Terraform HCL code
```

---

### 3. Diagram Generation (`diagram_generator.py`)

**How it works:**
```python
Intent Dictionary → Mermaid Syntax Builder → Mermaid Diagram Code
```

**Process:**
1. **Extract Intent Values**:
   - App type, database, app_count, architecture, etc.

2. **Build Node Definitions**:
   ```python
   # For each EC2 instance
   EC21["EC2 Instance 1\nGo App\nPort: 80"]
   
   # Database node
   DB["MySQL\nEC2 Instance\nPort: 3306"]
   ```

3. **Build Connections**:
   ```python
   # 2-tier (no load balancer)
   Users -->|HTTP| EC21
   EC21 -->|MySQL Port 3306| DB
   
   # 3-tier (with load balancer)
   Users -->|HTTP| ALB
   ALB -->|HTTP| EC21
   EC21 -->|MySQL Port 3306| DB
   ```

4. **Add Styling**: Mermaid style directives for colors
   ```python
   style VPC fill:#e0f2fe,stroke:#0369a1,stroke-width:3px
   style EC21 fill:#dbeafe,stroke:#2563eb,stroke-width:2px
   ```

5. **Return Mermaid Code**: Frontend uses Mermaid.js to render SVG

**Example:**
```python
Intent: {
    "app": "golang",
    "database": "mysql",
    "app_count": 1,
    "load_balancer": False
}

Generated Mermaid:
graph TB
    subgraph Internet["Internet"]
        Users["Users"]
    end
    subgraph VPC["VPC: us-east-1"]
        subgraph PublicSubnet["Public Subnet 10.0.1.0/24"]
            EC21["EC2 Instance 1\nGo App\nPort: 80"]
        end
        subgraph PrivateSubnet["Private Subnet 10.0.2.0/24"]
            DB["MySQL\nEC2 Instance\nPort: 3306"]
        end
    end
    Users -->|HTTP| EC21
    EC21 -->|MySQL Port 3306| DB
```

**Frontend Rendering:**
```javascript
// Frontend receives Mermaid code string
const diagramText = data.diagram;

// Mermaid.js renders it to SVG
const { svg } = await mermaid.render('diagram-id', diagramText);
diagramElement.innerHTML = svg; // Display SVG
```

---

### 4. Code Validation (`terraform_validator.py`)

**How it works:**
```python
Terraform Code String → Pattern Matching & Analysis → Validation Results
```

**Process:**
1. **Structure Checks**:
   ```python
   if "terraform {" not in terraform_code:
       errors.append("Missing terraform block")
   ```

2. **Resource Counting**:
   ```python
   resource_count = len(re.findall(r'resource\s+"[^"]+"\s+"[^"]+"', terraform_code))
   ```

3. **Syntax Validation**:
   ```python
   open_braces = terraform_code.count('{')
   close_braces = terraform_code.count('}')
   if open_braces != close_braces:
       errors.append("Unmatched braces")
   ```

4. **Best Practice Checks**:
   ```python
   if "security_group" not in terraform_code.lower():
       warnings.append("No security groups found")
   ```

5. **Generate Suggestions**:
   ```python
   if "t2.micro" in terraform_code:
       suggestions.append("Using t2.micro (free tier eligible)")
   ```

**Example:**
```python
Input: Terraform code string

Analysis:
1. Check for "terraform {" → Found ✅
2. Check for "provider" → Found ✅
3. Count resources → Found 5 resources
4. Check braces → Balanced ✅
5. Check security groups → Found ✅
6. Check for hardcoded passwords → None found ✅

Output:
{
    "valid": true,
    "errors": [],
    "warnings": [],
    "suggestions": ["Using t2.micro (free tier eligible)"],
    "resource_count": 5
}
```

---

### 5. Cost Estimation (`cost_estimator.py`)

**How it works:**
```python
Intent Dictionary → Pricing Lookup → Cost Calculation → Breakdown
```

**Process:**
1. **Pricing Database**: Hardcoded AWS pricing (for PoC)
   ```python
   PRICING = {
       "ec2": {
           "t2.micro": 0.0116,  # per hour
           "t3.micro": 0.0104,
       },
       "alb": 0.0225,  # per hour
   }
   ```

2. **Calculate EC2 Costs**:
   ```python
   ec2_hourly = PRICING["ec2"][instance_type]  # e.g., 0.0116
   ec2_monthly = ec2_hourly * 24 * 30 * app_count
   # 0.0116 * 24 * 30 * 1 = $8.35/month
   ```

3. **Calculate Database Costs**:
   ```python
   if database != "none":
       db_monthly = ec2_hourly * 24 * 30  # Same as app instance
   ```

4. **Calculate Load Balancer Costs**:
   ```python
   if load_balancer:
       alb_monthly = PRICING["alb"] * 24 * 30
       # 0.0225 * 24 * 30 = $16.20/month
   ```

5. **Data Transfer Estimation**:
   ```python
   data_transfer_cost = max(0, (100 - 10) * 0.09)  # First 10GB free
   ```

6. **Free Tier Check**:
   ```python
   free_tier_eligible = (
       instance_type in ["t2.micro", "t3.micro"] and
       app_count <= 2
   )
   ```

7. **Generate Tips**:
   ```python
   if monthly_cost > 50:
       tips.append("Consider Reserved Instances for 30-40% savings")
   ```

**Example:**
```python
Intent: {
    "instance_type": "t2.micro",
    "app_count": 1,
    "database": "mysql",
    "load_balancer": False
}

Calculation:
- EC2 App: 0.0116 * 24 * 30 * 1 = $8.35
- EC2 DB: 0.0116 * 24 * 30 * 1 = $8.35
- Data Transfer: (100-10) * 0.09 = $8.10
- Total: $24.80/month

Output:
{
    "monthly_cost": 24.80,
    "breakdown": {
        "EC2 Instances (App)": 8.35,
        "EC2 Instance (MYSQL)": 8.35,
        "Data Transfer": 8.10
    },
    "free_tier_eligible": true,
    "cost_optimization_tips": [...]
}
```

---

### 6. Security Analysis (`security_analyzer.py`)

**How it works:**
```python
Intent + Terraform Code → Pattern Matching → Security Scoring → Findings
```

**Process:**
1. **VPC Check**:
   ```python
   if "vpc" in terraform_code.lower():
       findings.append({"type": "positive", "finding": "VPC configured"})
       score += 0  # Already at 100, no change
   else:
       findings.append({"type": "negative", "finding": "No VPC"})
       score -= 20  # Deduct points
   ```

2. **Security Groups Check**:
   ```python
   if "security_group" in terraform_code.lower():
       # Check for overly permissive rules
       if 'cidr_blocks = ["0.0.0.0/0"]' in terraform_code:
           if 'port   = 22' in terraform_code:
               findings.append({
                   "type": "warning",
                   "finding": "SSH open to 0.0.0.0/0",
                   "severity": "medium"
               })
               score -= 10
   ```

3. **Database Isolation Check**:
   ```python
   if database != "none":
       if "private" in terraform_code.lower() and "subnet" in terraform_code.lower():
           findings.append({"type": "positive", "finding": "DB in private subnet"})
       else:
           findings.append({"type": "warning", "finding": "DB should be in private subnet"})
           score -= 15
   ```

4. **Secrets Management Check**:
   ```python
   if 'password' in terraform_code.lower():
       if '= "' in terraform_code:  # Hardcoded value
           findings.append({"type": "negative", "finding": "Hardcoded credentials"})
           score -= 25
   ```

5. **Encryption Check**:
   ```python
   if "encryption" not in terraform_code.lower():
       findings.append({"type": "warning", "finding": "Encryption not configured"})
       score -= 10
   ```

6. **Calculate Security Level**:
   ```python
   if score >= 80:
       security_level = "Good"
   elif score >= 60:
       security_level = "Moderate"
   else:
       security_level = "Needs Improvement"
   ```

**Example:**
```python
Input:
- Intent: {"database": "mysql", "load_balancer": False}
- Terraform: Contains VPC, security groups, DB in private subnet

Analysis:
1. VPC found → +0 (already 100)
2. Security groups found → +0
3. DB in private subnet → +0
4. SSH open to 0.0.0.0/0 → -10
5. No encryption → -10
6. Final score: 80

Output:
{
    "security_score": 80,
    "security_level": "Good",
    "findings": [
        {"type": "positive", "finding": "VPC configured"},
        {"type": "warning", "finding": "SSH open to 0.0.0.0/0"},
        {"type": "warning", "finding": "Encryption not configured"}
    ],
    "recommendations": [
        "Restrict SSH access to specific IP ranges",
        "Enable encryption at rest"
    ],
    "compliance": {
        "network_isolation": true,
        "security_groups": true,
        "database_isolation": true,
        "encryption": false
    }
}
```

---

### 7. Explanation Generation (`app.py`)

**How it works:**
```python
Intent Dictionary → Template-based Text Generation → Markdown String
```

**Process:**
1. **Extract Values**: Get app, database, architecture from intent
2. **Build Sections**: Construct explanation parts
   ```python
   explanation_parts = [
       "## Architecture Overview",
       f"This infrastructure deploys a **{app} application**...",
       "### Components:",
       f"- **Compute**: {app_count} EC2 instance(s)...",
   ]
   ```
3. **Conditional Content**: Add sections based on intent
   ```python
   if load_balancer:
       explanation_parts.append("- **Load Balancer**: ALB...")
   
   if database != "none":
       explanation_parts.append(f"- **Database**: {db_label}...")
   ```
4. **Join**: Combine all parts with newlines
5. **Return**: Markdown string (rendered as HTML in frontend)

---

## 🔄 Complete Request/Response Flow

### Backend Flow (Python)

```python
# 1. User sends POST request
POST /generate
Body: {"description": "golang app with mysql"}

# 2. FastAPI receives request
@app.post("/generate")
async def generate_infrastructure(request: InfrastructureRequest):
    
    # 3. Extract intent
    intent = intent_extractor.extract_intent(request.description)
    # Returns: {"app": "golang", "database": "mysql", ...}
    
    # 4. Generate Terraform
    terraform_code = terraform_generator.generate(intent)
    # Returns: Complete Terraform HCL string
    
    # 5. Generate diagram
    diagram = diagram_generator.generate(intent)
    # Returns: Mermaid diagram code string
    
    # 6. Validate code
    validation = terraform_validator.validate(terraform_code)
    # Returns: {"valid": true, "errors": [], "warnings": [], ...}
    
    # 7. Estimate costs
    cost_estimation = cost_estimator.estimate(intent, validation["resource_count"])
    # Returns: {"monthly_cost": 24.80, "breakdown": {...}, ...}
    
    # 8. Analyze security
    security_analysis = security_analyzer.analyze(intent, terraform_code)
    # Returns: {"security_score": 80, "findings": [...], ...}
    
    # 9. Generate explanation
    explanation = _generate_explanation(intent)
    # Returns: Markdown string
    
    # 10. Return combined response
    return InfrastructureResponse(
        intent=intent,
        terraform_code=terraform_code,
        diagram=diagram,
        explanation=explanation,
        validation=validation,
        cost_estimation=cost_estimation,
        security_analysis=security_analysis
    )
```

### Frontend Flow (JavaScript)

```javascript
// 1. User clicks "Generate Infrastructure"
async function generateInfrastructure() {
    
    // 2. Send request to backend
    const response = await fetch('http://localhost:8000/generate', {
        method: 'POST',
        body: JSON.stringify({ description: userInput })
    });
    
    // 3. Receive JSON response
    const data = await response.json();
    // Contains: intent, terraform_code, diagram, validation, cost_estimation, security_analysis, explanation
    
    // 4. Display Terraform code
    document.getElementById('terraform-code').textContent = data.terraform_code;
    Prism.highlightElement(...); // Syntax highlighting
    
    // 5. Render diagram
    const { svg } = await mermaid.render('diagram-id', data.diagram);
    document.getElementById('diagram').innerHTML = svg;
    
    // 6. Display validation
    displayValidation(data.validation);
    // Creates HTML with errors, warnings, suggestions
    
    // 7. Display cost estimation
    displayCostEstimation(data.cost_estimation);
    // Creates HTML with cost breakdown table
    
    // 8. Display security analysis
    displaySecurityAnalysis(data.security_analysis);
    // Creates HTML with score, findings, compliance checklist
    
    // 9. Display explanation
    document.getElementById('explanation').innerHTML = data.explanation.replace(/\n/g, '<br>');
}
```

---

## 🎯 Key Design Decisions

### 1. **Why Pattern Matching for Validation/Security?**
- **Fast**: No external API calls needed
- **Deterministic**: Same input = same output
- **Lightweight**: Works without additional services
- **PoC Appropriate**: Good enough for demonstration

### 2. **Why Hardcoded Pricing?**
- **No External Dependencies**: Works offline
- **Predictable**: Consistent results
- **Fast**: No API rate limits
- **Note**: Production would use AWS Pricing API

### 3. **Why Mermaid for Diagrams?**
- **Client-side Rendering**: No server-side image generation
- **Scalable**: Vector graphics (SVG)
- **Interactive**: Can be enhanced with JavaScript
- **Standard**: Widely supported

### 4. **Why Jinja2 Templates?**
- **Flexible**: Conditional logic, loops
- **Maintainable**: Separate templates for each file
- **Reusable**: Same templates for different intents
- **Standard**: Common in infrastructure tools

---

## 📈 Scalability Considerations

### Current (PoC):
- ✅ All processing is synchronous
- ✅ No caching
- ✅ Single-threaded
- ✅ In-memory operations

### Production Improvements:
- Add caching for common intents
- Use AWS Pricing API for real-time costs
- Add Terraform syntax validation with `terraform validate`
- Use proper LLM for all analysis (not just intent)
- Add database for storing generated infrastructure
- Implement async processing for large requests

---

This architecture provides a complete, working PoC that demonstrates AI-assisted infrastructure generation with comprehensive analysis features!
