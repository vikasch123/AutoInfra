"""
AutoInfra.ai - Backend API
Converts natural language infrastructure requirements to Terraform code
"""

from fastapi import FastAPI, HTTPException
import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import json
import os
from pathlib import Path
from datetime import datetime
from openai import OpenAI

from terraform_generator import TerraformGenerator
from diagram_generator import DiagramGenerator
from intent_extractor import IntentExtractor
from terraform_validator import TerraformValidator
from cost_estimator import CostEstimator
from security_analyzer import SecurityAnalyzer
from cloud_bill_estimator import CloudBillEstimator

app = FastAPI(title="AutoInfra.ai API", version="1.0.0")

# Get the base directory
BASE_DIR = Path(__file__).parent

# Serve static files
static_dir = BASE_DIR / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
intent_extractor = IntentExtractor()
terraform_generator = TerraformGenerator()
diagram_generator = DiagramGenerator()
terraform_validator = TerraformValidator()
cost_estimator = CostEstimator()
security_analyzer = SecurityAnalyzer()
cloud_bill_estimator = CloudBillEstimator()


class ValidationResult(BaseModel):
    valid: bool = False
    errors: List[str] = []
    warnings: List[str] = []
    resource_count: int = 0
    suggestions: List[str] = []

class CostEstimationModel(BaseModel):
    monthly_cost: float = 0.0
    breakdown: Dict[str, float] = {}
    free_tier_eligible: bool = False
    cost_optimization_tips: List[str] = []
    estimated_annual: float = 0.0

class CloudBillModel(BaseModel):
    estimated_monthly: float = 0.0
    estimated_monthly_cost: float = 0.0
    estimated_annual: float = 0.0
    free_tier_savings: float = 0.0
    bill_items: List[Dict[str, Any]] = []
    category_breakdown: Dict[str, float] = {}
    region: str = "us-east-1"
    currency: str = "USD"
    estimation_date: str = ""
    recommendations: List[str] = []
    free_tier_eligible: bool = False
    cost_optimization_potential: Dict[str, Any] = {}

class SecurityAnalysisModel(BaseModel):
    security_score: int = 100
    security_level: str = "Good"
    findings: List[Dict[str, Any]] = []
    recommendations: List[str] = []
    compliance: Dict[str, bool] = {}

class InfrastructureRequest(BaseModel):
    description: str


class InfrastructureResponse(BaseModel):
    intent: Dict[str, Any]
    terraform_code: str
    diagram: str
    explanation: str
    validation: Dict[str, Any]
    cost_estimation: Dict[str, Any]
    cloud_bill: Dict[str, Any]
    security_analysis: Dict[str, Any]


@app.get("/")
async def root():
    """Serve the frontend"""
    index_path = BASE_DIR / "static" / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"message": "AutoInfra.ai API", "status": "running", "note": "Frontend not found"}


@app.post("/generate", response_model=InfrastructureResponse)
async def generate_infrastructure(request: InfrastructureRequest):
    """
    Main endpoint: Takes natural language description and returns
    Terraform code, diagram, and explanation
    """
    try:
        # Step 1: Extract structured intent using LLM
        intent = intent_extractor.extract_intent(request.description)
        
        # Step 2: Generate Terraform code from template
        terraform_code = terraform_generator.generate(intent)
        
        # Step 3: Generate architecture diagram
        diagram = diagram_generator.generate(intent)
        
        # Step 4: Generate explanation
        explanation = _generate_explanation(intent)
        
        # Step 5: Validate terraform
        validation = terraform_validator.validate(terraform_code)
        
        # Step 6: Estimate costs (basic)
        cost_estimation = cost_estimator.estimate(intent, validation.get("resource_count", 0))
        
        # Step 7: Detailed cloud bill estimation
        try:
            cloud_bill = cloud_bill_estimator.estimate_detailed_bill(intent, validation.get("resource_count", 0))
        except Exception as e:
            # Fallback to basic cost estimation if detailed bill fails
            cloud_bill = {
                "estimated_monthly": cost_estimation.get("monthly_cost", 0),
                "estimated_monthly_cost": cost_estimation.get("monthly_cost", 0),
                "estimated_annual": cost_estimation.get("estimated_annual", 0),
                "free_tier_savings": 0,
                "bill_items": [],
                "category_breakdown": {},
                "region": intent.get("region", "us-east-1"),
                "currency": "USD",
                "estimation_date": datetime.now().strftime("%Y-%m-%d"),
                "recommendations": cost_estimation.get("cost_optimization_tips", []),
                "free_tier_eligible": cost_estimation.get("free_tier_eligible", False),
                "cost_optimization_potential": {}
            }

        # Step 8: Analyze security
        security_analysis = security_analyzer.analyze(intent, terraform_code)
        
        # Defensive normalization of response fields to avoid undefined numeric fields
        def _to_float(v, default=0.0):
            try:
                if isinstance(v, (int, float)):
                    return float(v)
                if isinstance(v, str):
                    return float(v)
                if isinstance(v, dict):
                    for k in ("monthly_cost", "estimated_monthly_cost", "monthly", "total", "estimated"):
                        if k in v:
                            return _to_float(v[k], default)
                return float(default)
            except Exception:
                return float(default)

        terraform_code = terraform_code or ""
        diagram = diagram or ""
        explanation = explanation or ""

        validation = validation if isinstance(validation, dict) else {}
        validation.setdefault("valid", False)
        validation.setdefault("errors", [])
        validation.setdefault("warnings", [])
        validation.setdefault("resource_count", 0)
        validation.setdefault("suggestions", [])

        # cost_estimation normalization
        cost_estimation = cost_estimation if isinstance(cost_estimation, dict) else {}
        monthly_val = _to_float(cost_estimation.get("monthly_cost", None), 0.0)
        if monthly_val == 0.0 and isinstance(cost_estimation.get("breakdown"), dict):
            try:
                monthly_val = sum(float(v) for v in cost_estimation["breakdown"].values())
            except Exception:
                monthly_val = monthly_val
        cost_estimation["monthly_cost"] = round(monthly_val, 2)
        cost_estimation.setdefault("breakdown", {})
        cost_estimation.setdefault("free_tier_eligible", False)
        cost_estimation.setdefault("cost_optimization_tips", [])
        cost_estimation.setdefault("estimated_annual", round(cost_estimation["monthly_cost"] * 12, 2))

        # cloud_bill normalization
        cloud_bill = cloud_bill if isinstance(cloud_bill, dict) else {}
        # accept either estimated_monthly_cost (new) or estimated_monthly (older)
        cloud_val = _to_float(cloud_bill.get("estimated_monthly_cost", cloud_bill.get("estimated_monthly", None)), 0.0)
        cloud_bill["estimated_monthly_cost"] = round(cloud_val, 2)
        cloud_bill.setdefault("breakdown", {})

        # security_analysis normalization
        security_analysis = security_analysis if isinstance(security_analysis, dict) else {}
        sec_score = int(max(0, min(100, round(_to_float(security_analysis.get("security_score", None), 100)))))
        security_analysis["security_score"] = sec_score
        if "security_level" not in security_analysis:
            security_analysis["security_level"] = ("Good" if sec_score >= 80 else "Moderate" if sec_score >= 60 else "Poor" if sec_score >= 40 else "Critical")
        security_analysis.setdefault("findings", [])
        security_analysis.setdefault("recommendations", [])
        security_analysis.setdefault("compliance", {})

        response = {
             "intent": intent,
             "terraform_code": terraform_code,
             "diagram": diagram,
             "explanation": explanation,
             "validation": validation,
             "cost_estimation": cost_estimation,
             "cloud_bill": cloud_bill,
             "security_analysis": security_analysis
         }
        # write full response to disk for debugging (inspect when frontend errors)
        try:
            with open("/tmp/last_generate_response.json", "w") as _f:
                json.dump(response, _f)
        except Exception:
            logging.exception("Failed to write /tmp/last_generate_response.json")

        # log response summary for debugging (sensitive details omitted)
        logging.debug("generate_infrastructure response summary: monthly_cost=%s, cloud_est=%s, sec_score=%s",
                      response["cost_estimation"].get("monthly_cost"),
                      response["cloud_bill"].get("estimated_monthly_cost"),
                      response["security_analysis"].get("security_score"))

        # log full response payload for debugging (safe to redact later)
        try:
            logging.info("Full generate response: %s", json.dumps(response))
        except Exception:
            logging.debug("Response serialization failed for debug log")

        return InfrastructureResponse(**response)
    
    except Exception as e:
        logging.exception("Failed to generate infrastructure")
        raise HTTPException(status_code=500, detail=f"Error generating infrastructure: {str(e)}")


def _generate_explanation(intent: Dict[str, Any]) -> str:
    """Generate a brief explanation of the infrastructure"""
    
    app = intent.get("app", "application").upper()
    database = intent.get("database", "none")
    architecture = intent.get("architecture", "2-tier")
    load_balancer = intent.get("load_balancer", False)
    app_count = intent.get("app_count", 1)
    
    # Database labels
    db_labels = {
        "mysql": "MySQL",
        "postgresql": "PostgreSQL",
        "mongodb": "MongoDB",
        "redis": "Redis",
        "dynamodb": "DynamoDB",
        "none": "No Database"
    }
    db_label = db_labels.get(database, database.upper())
    
    explanation_parts = [
        "## Architecture Overview",
        "",
        f"This infrastructure deploys a **{app} application** on AWS using a **{architecture}** architecture:",
        "",
        "### Components:",
        f"- **Compute**: {app_count} EC2 instance(s) in public subnets for the {app} application",
    ]
    
    if load_balancer:
        explanation_parts.append("- **Load Balancer**: Application Load Balancer (ALB) for traffic distribution")
    
    if database != "none":
        explanation_parts.append(f"- **Database**: {db_label} running on EC2 in private subnet")
    else:
        explanation_parts.append("- **Database**: No database configured")
    
    explanation_parts.extend([
        "- **Networking**: Custom VPC with public and private subnets",
        "",
        "### Traffic Flow:",
    ])
    
    if load_balancer:
        explanation_parts.extend([
            "1. Internet traffic → Application Load Balancer (ALB)",
            f"2. ALB → EC2 instances ({app} app)",
        ])
        if database != "none":
            explanation_parts.append(f"3. {app} app → {db_label} (EC2 instance in private subnet)")
    else:
        explanation_parts.append(f"1. Internet traffic → EC2 instances ({app} app)")
        if database != "none":
            explanation_parts.append(f"2. {app} app → {db_label} (EC2 instance in private subnet)")
    
    explanation_parts.extend([
        "",
        "### Security:",
        "- Security groups restrict access to necessary ports only",
        "- VPC provides network isolation",
        "- Database is in a private subnet for enhanced security",
        "",
        "### PoC Limitations:",
        "- Single availability zone (for cost optimization)",
        "- No auto-scaling configured",
        f"- Manual {db_label} setup (not managed service)" if database != "none" else "- No database configured",
        "- Free-tier friendly configuration"
    ])
    
    return "\n".join(explanation_parts)


@app.get("/debug_sample", response_model=InfrastructureResponse)
async def debug_sample():
    """Return a known-good sample response to verify frontend numeric handling"""
    sample = {
        "intent": {"app": "nodejs", "database": "mongodb", "load_balancer": True, "app_count": 2},
        "terraform_code": "terraform {} provider \"aws\" {} resource \"aws_instance\" \"app\" {}",
        "diagram": "",
        "explanation": "Sample explanation",
        "validation": {"valid": True, "errors": [], "warnings": [], "resource_count": 3, "suggestions": []},
        "cost_estimation": {"monthly_cost": 12.34, "breakdown": {"EC2": 10.0, "ALB": 2.34}, "free_tier_eligible": False, "cost_optimization_tips": [], "estimated_annual": 148.08},
        "cloud_bill": {"estimated_monthly_cost": 12.34, "breakdown": {}},
        "security_analysis": {"security_score": 85, "security_level": "Good", "findings": [], "recommendations": [], "compliance": {}},
    }
    return InfrastructureResponse(**sample)


@app.get("/last_response")
async def last_response():
    """Return last /generate response payload (debug only)"""
    path = "/tmp/last_generate_response.json"
    if os.path.exists(path):
        return FileResponse(path)
    return {"error": "no debug response found"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
