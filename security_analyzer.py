"""
Security Analyzer - Analyzes infrastructure security posture
"""

import re
from typing import Dict, Any, List


class SecurityAnalyzer:
    """Analyzes security aspects of generated infrastructure"""

    def analyze(self, intent: Dict[str, Any], terraform_code: str) -> Dict[str, Any]:
        """
        Analyze security posture
        Returns: {
            "security_score": int (0-100),
            "findings": List[Dict],
            "recommendations": List[str],
            "compliance": Dict[str, bool]
        }
        """
        tf = (terraform_code or "").lower()
        findings: List[Dict[str, Any]] = []
        recommendations: List[str] = []
        compliance: Dict[str, bool] = {}
        score = 100

        # Check VPC usage
        if "vpc" in tf:
            findings.append({
                "type": "positive",
                "category": "Network Isolation",
                "finding": "VPC is configured for network isolation",
                "severity": "info"
            })
            compliance["network_isolation"] = True
        else:
            findings.append({
                "type": "negative",
                "category": "Network Isolation",
                "finding": "No VPC configured - resources exposed to default network",
                "severity": "high"
            })
            score -= 20
            compliance["network_isolation"] = False
            recommendations.append("Configure VPC for network isolation")

        # Check security groups
        if "security_group" in tf or "aws_security_group" in tf:
            findings.append({
                "type": "positive",
                "category": "Network Security",
                "finding": "Security groups are configured",
                "severity": "info"
            })
            compliance["security_groups"] = True

            # Check for overly permissive rules (detect any 0.0.0.0/0 usage)
            if re.search(r'0\.0\.0\.0\s*/\s*0', tf) or re.search(r'["\']?0\.0\.0\.0/0["\']?', tf):
                findings.append({
                    "type": "negative",
                    "category": "Network Security",
                    "finding": "Security group with 0.0.0.0/0 detected",
                    "severity": "high"
                })
                score -= 20
                recommendations.append("Lock down security group CIDR blocks to least privilege")
        else:
            findings.append({
                "type": "negative",
                "category": "Network Security",
                "finding": "No security groups defined",
                "severity": "high"
            })
            compliance["security_groups"] = False
            score -= 20
            recommendations.append("Define security groups to restrict access")

        # Check database placement
        database = intent.get("database", "none")
        if database != "none":
            if "private" in tf or "private_subnet" in tf:
                findings.append({
                    "type": "positive",
                    "category": "Database Placement",
                    "finding": "Database placed in private subnet",
                    "severity": "info"
                })
                compliance["database_in_private_subnet"] = True
            else:
                findings.append({
                    "type": "negative",
                    "category": "Database Placement",
                    "finding": "Database not placed in private subnet",
                    "severity": "high"
                })
                compliance["database_in_private_subnet"] = False
                score -= 15
                recommendations.append("Place databases in private subnets and restrict access")

        # Check for hardcoded credentials (detect assignments like password = "..." or secret = '...')
        if re.search(r'(?i)\b(password|secret|access_key|secret_key)\b\s*=\s*["\'][^"\']+["\']', terraform_code or ""):
            findings.append({
                "type": "negative",
                "category": "Credentials",
                "finding": "Hardcoded credentials or secrets detected",
                "severity": "high"
            })
            recommendations.append("Use Secrets Manager or SSM Parameter Store for credentials")
            score -= 25
        else:
            findings.append({
                "type": "positive",
                "category": "Credentials",
                "finding": "No obvious hardcoded credentials found",
                "severity": "info"
            })

        # Check load balancer
        if intent.get("load_balancer", False):
            if "alb" in tf or "load_balancer" in tf or "aws_lb" in tf:
                # Check for TLS/HTTPS
                if "https" in tf or "certificate" in tf or "ssl" in tf or "443" in tf:
                    findings.append({
                        "type": "positive",
                        "category": "Load Balancer",
                        "finding": "Load balancer with TLS/HTTPS configured",
                        "severity": "info"
                    })
                else:
                    findings.append({
                        "type": "negative",
                        "category": "Load Balancer",
                        "finding": "Load balancer configured without TLS",
                        "severity": "medium"
                    })
                    recommendations.append("Enable TLS on the load balancer for secure traffic")
                    score -= 5
            else:
                findings.append({
                    "type": "negative",
                    "category": "Load Balancer",
                    "finding": "Load balancer expected but not found in config",
                    "severity": "medium"
                })
                score -= 5
        else:
            findings.append({
                "type": "info",
                "category": "Load Balancer",
                "finding": "No load balancer requested",
                "severity": "info"
            })

        # Check encryption
        if "encryption" not in tf and "kms" not in tf and "encrypted" not in tf:
            findings.append({
                "type": "negative",
                "category": "Encryption",
                "finding": "No encryption or KMS usage detected",
                "severity": "medium"
            })
            recommendations.append("Enable encryption at rest and use KMS for keys")
            score -= 10
        else:
            findings.append({
                "type": "positive",
                "category": "Encryption",
                "finding": "Encryption/KMS usage detected",
                "severity": "info"
            })

        # Ensure score doesn't go below 0
        score = max(0, score)

        # Security level
        if score >= 80:
            security_level = "Good"
        elif score >= 60:
            security_level = "Moderate"
        elif score >= 40:
            security_level = "Poor"
        else:
            security_level = "Critical"

        return {
            "security_score": int(score),
            "security_level": security_level,
            "findings": findings,
            "recommendations": recommendations,
            "compliance": compliance
        }
