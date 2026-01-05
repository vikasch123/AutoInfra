"""
Cloud Bill Estimator - Detailed AWS cost estimation with breakdown
More accurate and comprehensive than basic cost estimator
"""

from typing import Dict, Any, List
from datetime import datetime


class CloudBillEstimator:
    """Detailed cloud bill estimation with service-level breakdown"""
    
    # AWS Pricing (as of 2024 - for PoC, can be updated or use AWS Pricing API)
    PRICING = {
        "ec2": {
            "t2.micro": {"hourly": 0.0116, "monthly": 8.35, "free_tier": True},
            "t2.small": {"hourly": 0.023, "monthly": 16.56, "free_tier": False},
            "t3.micro": {"hourly": 0.0104, "monthly": 7.49, "free_tier": True},
            "t3.small": {"hourly": 0.0208, "monthly": 14.98, "free_tier": False},
            "t3.medium": {"hourly": 0.0416, "monthly": 29.95, "free_tier": False},
        },
        "ebs": {
            "gp3": 0.08,  # per GB/month
            "gp2": 0.10,
        },
        "alb": {
            "hourly": 0.0225,
            "monthly": 16.20,
            "lcu_hourly": 0.008,  # Load Balancer Capacity Units
        },
        "nat_gateway": {
            "hourly": 0.045,
            "monthly": 32.40,
            "data_gb": 0.045,  # per GB
        },
        "data_transfer": {
            "first_10gb": 0.0,  # Free
            "next_40tb": 0.09,  # per GB
            "next_100tb": 0.085,
        },
        "cloudwatch": {
            "metrics": 0.30,  # per metric/month (first 10 free)
            "logs": 0.50,  # per GB ingested
        },
        "s3": {
            "storage": 0.023,  # per GB/month (first 5GB free)
            "requests": 0.005,  # per 1000 requests
        }
    }
    
    def estimate_detailed_bill(self, intent: Dict[str, Any], resource_count: int = 0) -> Dict[str, Any]:
        """
        Generate detailed cloud bill estimation
        Returns comprehensive breakdown with recommendations
        """
        instance_type = intent.get("instance_type", "t2.micro")
        app_count = intent.get("app_count", 1)
        load_balancer = intent.get("load_balancer", False)
        database = intent.get("database", "none")
        region = intent.get("region", "us-east-1")
        
        bill_items = []
        total_monthly = 0.0
        total_annual = 0.0
        
        # EC2 Instances - Application
        ec2_info = self.PRICING["ec2"].get(instance_type, self.PRICING["ec2"]["t2.micro"])
        ec2_monthly = ec2_info["monthly"] * app_count
        bill_items.append({
            "service": "EC2 Instances (Application)",
            "specification": f"{app_count}x {instance_type}",
            "unit": "per month",
            "quantity": app_count,
            "unit_price": ec2_info["monthly"],
            "total": round(ec2_monthly, 2),
            "free_tier": ec2_info["free_tier"] and app_count <= 2,
            "category": "Compute"
        })
        total_monthly += ec2_monthly
        
        # EC2 Instance - Database
        if database != "none":
            db_monthly = ec2_info["monthly"]
            bill_items.append({
                "service": f"EC2 Instance ({database.upper()})",
                "specification": f"1x {instance_type}",
                "unit": "per month",
                "quantity": 1,
                "unit_price": ec2_info["monthly"],
                "total": round(db_monthly, 2),
                "free_tier": ec2_info["free_tier"],
                "category": "Database"
            })
            total_monthly += db_monthly
        
        # EBS Storage (estimated 30GB per instance)
        ebs_per_instance = 30  # GB
        ebs_total_gb = ebs_per_instance * (app_count + (1 if database != "none" else 0))
        ebs_monthly = ebs_total_gb * self.PRICING["ebs"]["gp3"]
        if ebs_total_gb > 30:  # First 30GB free
            ebs_billable = max(0, ebs_total_gb - 30)
            ebs_monthly = ebs_billable * self.PRICING["ebs"]["gp3"]
            bill_items.append({
                "service": "EBS Storage",
                "specification": f"{ebs_total_gb}GB gp3",
                "unit": "per GB/month",
                "quantity": ebs_billable,
                "unit_price": self.PRICING["ebs"]["gp3"],
                "total": round(ebs_monthly, 2),
                "free_tier": ebs_billable == 0,
                "category": "Storage"
            })
            total_monthly += ebs_monthly
        
        # Application Load Balancer
        if load_balancer:
            alb_monthly = self.PRICING["alb"]["monthly"]
            # Estimate LCU usage (assume 1 LCU for small app)
            lcu_monthly = 1 * self.PRICING["alb"]["lcu_hourly"] * 24 * 30
            alb_total = alb_monthly + lcu_monthly
            bill_items.append({
                "service": "Application Load Balancer",
                "specification": "ALB + 1 LCU",
                "unit": "per month",
                "quantity": 1,
                "unit_price": round(alb_total, 2),
                "total": round(alb_total, 2),
                "free_tier": False,
                "category": "Networking"
            })
            total_monthly += alb_total
        
        # Data Transfer (estimate 100GB/month)
        data_transfer_gb = 100
        free_tier_gb = 10
        billable_gb = max(0, data_transfer_gb - free_tier_gb)
        if billable_gb > 0:
            data_transfer_cost = billable_gb * self.PRICING["data_transfer"]["next_40tb"]
            bill_items.append({
                "service": "Data Transfer (Outbound)",
                "specification": f"{billable_gb}GB (first {free_tier_gb}GB free)",
                "unit": "per GB",
                "quantity": billable_gb,
                "unit_price": self.PRICING["data_transfer"]["next_40tb"],
                "total": round(data_transfer_cost, 2),
                "free_tier": False,
                "category": "Networking"
            })
            total_monthly += data_transfer_cost
        
        # CloudWatch (estimated)
        cloudwatch_metrics = max(0, (app_count + (1 if database != "none" else 0)) * 5 - 10)  # 5 metrics per instance, first 10 free
        cloudwatch_cost = cloudwatch_metrics * self.PRICING["cloudwatch"]["metrics"]
        if cloudwatch_cost > 0:
            bill_items.append({
                "service": "CloudWatch Metrics",
                "specification": f"{cloudwatch_metrics} metrics",
                "unit": "per metric/month",
                "quantity": cloudwatch_metrics,
                "unit_price": self.PRICING["cloudwatch"]["metrics"],
                "total": round(cloudwatch_cost, 2),
                "free_tier": False,
                "category": "Monitoring"
            })
            total_monthly += cloudwatch_cost
        
        # VPC and Networking (free)
        bill_items.append({
            "service": "VPC & Networking",
            "specification": "VPC, Subnets, Internet Gateway",
            "unit": "per month",
            "quantity": 1,
            "unit_price": 0.0,
            "total": 0.0,
            "free_tier": True,
            "category": "Networking"
        })
        
        total_annual = total_monthly * 12
        
        # Free tier savings calculation
        free_tier_savings = sum(
            item["total"] for item in bill_items 
            if item.get("free_tier", False) and item["total"] > 0
        )
        
        # Cost optimization recommendations
        recommendations = self._generate_recommendations(intent, total_monthly, bill_items)
        
        # Cost breakdown by category
        category_breakdown = {}
        for item in bill_items:
            category = item["category"]
            if category not in category_breakdown:
                category_breakdown[category] = 0.0
            category_breakdown[category] += item["total"]
        
        return {
            "estimated_monthly": round(total_monthly, 2),
            # backward-compatible explicit numeric field the frontend expects
            "estimated_monthly_cost": round(total_monthly, 2),
            "estimated_annual": round(total_annual, 2),
            "free_tier_savings": round(free_tier_savings, 2),
            "bill_items": bill_items,
            "category_breakdown": {k: round(v, 2) for k, v in category_breakdown.items()},
            "region": region,
            "currency": "USD",
            "estimation_date": datetime.now().strftime("%Y-%m-%d"),
            "recommendations": recommendations,
            "free_tier_eligible": any(item.get("free_tier", False) for item in bill_items),
            "cost_optimization_potential": self._calculate_optimization_potential(total_monthly, intent)
         }
    
    def _generate_recommendations(self, intent: Dict[str, Any], monthly_cost: float, bill_items: List[Dict]) -> List[str]:
        """Generate cost optimization recommendations"""
        recommendations = []
        
        instance_type = intent.get("instance_type", "t2.micro")
        app_count = intent.get("app_count", 1)
        load_balancer = intent.get("load_balancer", False)
        
        # Instance type recommendations
        if instance_type not in ["t2.micro", "t3.micro"]:
            recommendations.append(f"Switch to t3.micro for better price/performance (save ~${self.PRICING['ec2']['t3.micro']['monthly'] - self.PRICING['ec2'].get(instance_type, {}).get('monthly', 0):.2f}/month)")
        
        # Reserved instances
        if monthly_cost > 50:
            ri_savings = monthly_cost * 0.35  # ~35% savings with Reserved Instances
            recommendations.append(f"Use Reserved Instances (1-year) to save ~${ri_savings:.2f}/month (35% discount)")
        
        # Load balancer optimization
        if load_balancer and app_count == 1:
            recommendations.append("Consider removing load balancer for single instance (save ~$16/month)")
        
        # Auto-scaling
        if app_count > 2:
            recommendations.append("Implement auto-scaling to reduce costs during low traffic periods")
        
        # Spot instances for non-critical workloads
        if monthly_cost > 100:
            spot_savings = sum(item["total"] for item in bill_items if "EC2" in item["service"]) * 0.7
            recommendations.append(f"Consider Spot Instances for dev/test (save up to ${spot_savings:.2f}/month, 70% discount)")
        
        # Data transfer optimization
        data_transfer_item = next((item for item in bill_items if "Data Transfer" in item["service"]), None)
        if data_transfer_item and data_transfer_item["total"] > 10:
            recommendations.append("Optimize data transfer: Use CloudFront CDN to reduce outbound data costs")
        
        return recommendations
    
    def _calculate_optimization_potential(self, monthly_cost: float, intent: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate potential savings"""
        potential_savings = {}
        
        # Reserved Instances
        if monthly_cost > 50:
            potential_savings["reserved_instances"] = {
                "savings_percentage": 35,
                "monthly_savings": round(monthly_cost * 0.35, 2),
                "annual_savings": round(monthly_cost * 0.35 * 12, 2)
            }
        
        # Spot Instances (for dev/test)
        instance_type = intent.get("instance_type", "t2.micro")
        ec2_monthly_price = self.PRICING["ec2"].get(instance_type, self.PRICING["ec2"]["t2.micro"]).get("monthly", 0)
        total_instances = intent.get("app_count", 1) + (1 if intent.get("database") != "none" else 0)
        ec2_cost = ec2_monthly_price * total_instances
        potential_savings["spot_instances"] = {
            "savings_percentage": 70,
            "monthly_savings": round(ec2_cost * 0.70, 2),
            "annual_savings": round(ec2_cost * 0.70 * 12, 2),
            "note": "For dev/test environments only"
        }
        
        return potential_savings
