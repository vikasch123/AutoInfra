"""
Terraform Validator - Validates generated Terraform code syntax
"""

import re
from typing import Dict, Any, List, Tuple


class TerraformValidator:
    """Validates Terraform code syntax and structure"""
    
    def validate(self, terraform_code: str) -> Dict[str, Any]:
        """
        Validate Terraform code and return validation results
        Returns: {
            "valid": bool,
            "errors": List[str],
            "warnings": List[str],
            "resource_count": int,
            "suggestions": List[str]
        }
        """
        errors = []
        warnings = []
        suggestions = []
        
        # Check for basic Terraform structure
        if "terraform {" not in terraform_code:
            errors.append("Missing terraform block")
        
        if "provider" not in terraform_code:
            errors.append("Missing provider configuration")
        
        # Check for required blocks
        required_blocks = ["resource", "variable"]
        for block in required_blocks:
            if f"{block} " not in terraform_code and f"{block}\"" not in terraform_code:
                warnings.append(f"No {block} blocks found")
        
        # Count resources
        resource_count = len(re.findall(r'resource\s+"[^"]+"\s+"[^"]+"', terraform_code))
        
        # Check for common issues
        if resource_count == 0:
            errors.append("No resources defined")
        
        # Check for unclosed braces (basic check)
        open_braces = terraform_code.count('{')
        close_braces = terraform_code.count('}')
        if open_braces != close_braces:
            errors.append(f"Unmatched braces: {open_braces} opening, {close_braces} closing")
        
        # Check for security groups
        if "security_group" not in terraform_code.lower():
            warnings.append("No security groups found - consider adding network security")
        
        # Check for VPC
        if "vpc" not in terraform_code.lower():
            warnings.append("No VPC found - consider using VPC for network isolation")
        
        # Suggestions
        if "t2.micro" in terraform_code:
            suggestions.append("Using t2.micro instance type (free tier eligible)")
        
        if "enable_deletion_protection = false" in terraform_code:
            suggestions.append("Consider enabling deletion protection for production")
        
        # Check for hardcoded values
        if re.search(r'password\s*=\s*"[^"]+"', terraform_code, re.IGNORECASE):
            errors.append("Hardcoded passwords detected - use variables or secrets manager")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "resource_count": resource_count,
            "suggestions": suggestions
        }
