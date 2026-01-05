<<<<<<< HEAD
# AutoInfra
=======
# AutoInfra.ai - AI-Powered Infrastructure Generation PoC

A proof-of-concept system that converts natural language cloud infrastructure requirements into validated Terraform code and architecture diagrams.

## 🎯 Overview

AutoInfra.ai demonstrates AI-assisted infrastructure design by:
1. Accepting plain English infrastructure requirements
2. Extracting structured infrastructure intent using an LLM
3. Mapping intent to pre-built Terraform templates
4. Generating deployable Terraform code and architecture diagrams

## 🏗️ Architecture

```
User Input (Natural Language)
    ↓
LLM Intent Extraction (JSON)
    ↓
Template Selection & Variable Injection
    ↓
Terraform Code Generation
    ↓
Architecture Diagram Generation (Mermaid)
    ↓
Output (Terraform + Diagram + Explanation)
```

## 📋 Supported Infrastructure Pattern

**Current Scope (PoC):**
- **Cloud Provider**: AWS
- **Application**: Node.js web application
- **Compute**: EC2 instances
- **Networking**: 
  - Custom VPC
  - Public Subnets
  - Application Load Balancer (ALB)
- **Database**: MongoDB (EC2)
- **Security**: Security Groups, Network isolation

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip
- (Optional) OpenAI API key for LLM intent extraction (falls back to mock mode if not provided)

### Installation

1. **Navigate to the project directory:**
   ```bash
   cd AutoInfra
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set OpenAI API key (optional):**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
   
   > **Note**: If no API key is provided, the system will use a mock intent extractor based on keyword matching.

### Running the Application

1. **Start the backend server:**
   ```bash
   python app.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Open your browser:**
   Navigate to `http://localhost:8000`

3. **Try it out:**
   Enter a natural language description like:
   ```
   I want a Node.js app on AWS behind a load balancer with MongoDB in a secure VPC
   ```

## 📁 Project Structure

```
AutoInfra/
├── app.py                      # FastAPI backend application
├── intent_extractor.py         # LLM-based intent extraction
├── terraform_generator.py      # Terraform code generation
├── diagram_generator.py        # Mermaid diagram generation
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── static/
│   └── index.html             # Frontend web interface
└── terraform_templates/
    ├── main.tf.j2             # Main Terraform template
    ├── variables.tf.j2        # Variables template
    └── outputs.tf.j2          # Outputs template
```

## 🔧 How It Works

### 1. Intent Extraction

The system uses an LLM (OpenAI GPT-3.5-turbo) to extract structured intent from natural language:

**Input:**
> "I need a high-availability Node.js application on AWS with MongoDB"

**Extracted Intent (JSON):**
```json
{
  "cloud": "aws",
  "app": "nodejs",
  "database": "mongodb",
  "availability": "high",
  "security": ["private_vpc", "security_groups"],
  "region": "us-east-1",
  "instance_type": "t2.micro",
  "app_count": 2
}
```

### 2. Terraform Generation

Pre-built Jinja2 templates are populated with intent values to generate valid, deployable Terraform code.

### 3. Diagram Generation

Mermaid diagrams are generated to visualize the infrastructure architecture.

### 4. Output

The system returns:
- **Terraform Code**: Ready-to-deploy infrastructure as code
- **Architecture Diagram**: Visual representation of the infrastructure
- **Explanation**: Brief overview of architecture, traffic flow, and security

## 🎨 Features

- ✅ Natural language to Terraform conversion
- ✅ Visual architecture diagrams
- ✅ Deterministic output (template-based)
- ✅ Free-tier friendly configurations
- ✅ No hardcoded credentials
- ✅ Clean, professional UI
- ✅ Mock mode (no API key required for testing)

## ⚠️ PoC Limitations

This is a **Proof of Concept** with intentional limitations:

- Single infrastructure pattern (AWS + Node.js + MongoDB)
- No multi-cloud support
- No Kubernetes
- No serverless
- No dynamic autoscaling
- Single availability zone (cost optimization)
- Manual MongoDB setup (not managed service)

## 🔒 Security Notes

- No credentials are hardcoded
- Security groups are configured for network isolation
- VPC provides network boundaries
- **Important**: This is a PoC - review all generated Terraform before deploying to production

## 🧪 Testing

1. Start the server: `python app.py`
2. Open `http://localhost:8000`
3. Enter infrastructure requirements
4. Review generated Terraform code
5. Validate with `terraform validate` (after downloading)

## 📝 Example Usage

**Input:**
```
I want a Node.js application on AWS with high availability, 
behind a load balancer, using MongoDB for the database, 
with secure networking in a VPC.
```

**Output:**
- Terraform code for:
  - VPC with public/private subnets
  - Application Load Balancer
  - 2x EC2 instances (Node.js app)
  - 1x EC2 instance (MongoDB)
  - Security groups with appropriate rules
- Mermaid architecture diagram
- Detailed explanation

## 🛠️ Development

### Adding New Templates

1. Create new Jinja2 templates in `terraform_templates/`
2. Update `terraform_generator.py` to use new templates
3. Update `intent_extractor.py` to handle new intent fields

### Extending Intent Extraction

Modify the system prompt in `intent_extractor.py` to extract additional fields or support new patterns.

## 📄 License

This is a proof-of-concept project for demonstration purposes.

## 🤝 Contributing

This is a PoC project. For production use, consider:
- Adding validation for Terraform syntax
- Supporting multiple infrastructure patterns
- Adding cost estimation
- Implementing authentication
- Adding deployment capabilities

---

**Built for demonstration and learning purposes.**
>>>>>>> f2ba635 (ADD the terraform templates and fastAPI code)
