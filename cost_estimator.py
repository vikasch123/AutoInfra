"""
Cost Estimator - Estimates monthly AWS costs for generated infrastructure
"""

from typing import Dict, Any


class CostEstimator:
    """Estimates AWS infrastructure costs"""

    # AWS pricing (approximate, as of 2024 - for PoC purposes)
    PRICING = {
        "ec2": {
            "t2.micro": 0.0116,  # per hour
            "t3.micro": 0.0104,
            "t3.small": 0.0208,
            "t3.medium": 0.0416,
        },
        "alb": 0.0225,  # per hour
        "vpc": 0.0,  # free
        "internet_gateway": 0.0,  # free
        "nat_gateway": 0.045,  # per hour (if used)
        "data_transfer": 0.09,  # per GB (first 10GB free)
    }

    def estimate(self, intent: Dict[str, Any], resource_count: int = 0) -> Dict[str, Any]:
        """
        Estimate monthly costs based on intent
        Returns: {
            "monthly_cost": float,
            "breakdown": Dict[str, float],
            "free_tier_eligible": bool,
            "cost_optimization_tips": List[str]
        }
        """
        instance_type = intent.get("instance_type", "t2.micro")
        app_count = int(intent.get("app_count", 1) or 1)
        load_balancer = bool(intent.get("load_balancer", False))

        hours_per_month = 24 * 30
        breakdown = {}
        monthly_cost = 0.0

        ec2_hour = self.PRICING["ec2"].get(instance_type, list(self.PRICING["ec2"].values())[0])
        ec2_monthly = ec2_hour * hours_per_month * app_count
        breakdown[f"EC2 ({instance_type}) x{app_count}"] = round(ec2_monthly, 2)
        monthly_cost += ec2_monthly

        if load_balancer:
            alb_monthly = self.PRICING["alb"] * hours_per_month
            breakdown["Application Load Balancer (ALB)"] = round(alb_monthly, 2)
            monthly_cost += alb_monthly

        # Data transfer estimate (100GB/month with first 10GB free)
        data_gb = 100
        data_cost = max(0.0, (data_gb - 10) * self.PRICING["data_transfer"])
        if data_cost > 0:
            breakdown["Data Transfer (100GB)"] = round(data_cost, 2)
            monthly_cost += data_cost

        # Free tier estimation heuristic
        free_tier_eligible = (instance_type in ["t2.micro", "t3.micro"] and app_count <= 2 and intent.get("database", "none") == "none")

        tips = []
        if instance_type not in ["t2.micro", "t3.micro"]:
            tips.append("Consider using t2/t3 micro instances for cost savings or burstable instances.")
        if app_count > 2:
            tips.append("Reduce number of instances or use auto-scaling groups to scale with demand.")
        if load_balancer and app_count == 1:
            tips.append("For single instance deployments consider skipping ALB to save costs.")
        if monthly_cost > 50:
            tips.append("Consider reserved instances or savings plans to reduce monthly cost.")

        monthly_cost = round(monthly_cost, 2)
        return {
            "monthly_cost": monthly_cost,
            "breakdown": breakdown,
            "free_tier_eligible": free_tier_eligible,
            "cost_optimization_tips": tips,
            "estimated_annual": round(monthly_cost * 12, 2)
        }
