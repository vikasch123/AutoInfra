"""
Diagram Generator - Generates Mermaid architecture diagrams
Supports 2-tier, 3-tier, and various tech stacks
"""

from typing import Dict, Any


class DiagramGenerator:
    """Generates Mermaid architecture diagrams from intent"""
    
    def generate(self, intent: Dict[str, Any]) -> str:
        """Generate Mermaid diagram code"""
        
        app_count = intent.get("app_count", 1)
        region = intent.get("region", "us-east-1")
        app = intent.get("app", "other")
        database = intent.get("database", "none")
        architecture = intent.get("architecture", "2-tier")
        load_balancer = intent.get("load_balancer", False)
        
        # App labels
        app_labels = {
            "golang": "Go App",
            "nodejs": "Node.js App",
            "python": "Python App",
            "java": "Java App",
            "dotnet": ".NET App",
            "php": "PHP App",
            "ruby": "Ruby App",
            "rust": "Rust App",
            "other": "Application"
        }
        app_label = app_labels.get(app, "Application")
        
        # Database labels and ports
        db_config = {
            "mysql": {"name": "MySQL", "port": 3306, "icon": "MySQL"},
            "postgresql": {"name": "PostgreSQL", "port": 5432, "icon": "PostgreSQL"},
            "mongodb": {"name": "MongoDB", "port": 27017, "icon": "MongoDB"},
            "redis": {"name": "Redis", "port": 6379, "icon": "Redis"},
            "dynamodb": {"name": "DynamoDB", "port": "N/A", "icon": "DynamoDB"},
            "none": {"name": "No Database", "port": "N/A", "icon": "None"}
        }
        db_info = db_config.get(database, {"name": database.upper(), "port": "N/A", "icon": "Database"})
        
        # Build EC2 instances - use simple labels without HTML
        ec2_instances = []
        for i in range(1, app_count + 1):
            ec2_instances.append(f'        EC2{i}["EC2 Instance {i}\\n{app_label}\\nPort: 80"]')
        
        ec2_section = "\n".join(ec2_instances)
        
        # Build connections based on architecture
        connections = []
        
        if architecture == "3-tier" and load_balancer:
            # 3-tier with load balancer
            connections.append("    Users -->|HTTP| ALB")
            for i in range(1, app_count + 1):
                connections.append(f"    ALB -->|HTTP| EC2{i}")
                if database != "none":
                    db_port = db_info['port']
                    connections.append(f"    EC2{i} -->|{db_info['name']} Port {db_port}| DB")
            
            diagram = f"""graph TB
    subgraph Internet["Internet"]
        Users["Users"]
    end
    
    subgraph VPC["VPC: {region}"]
        subgraph PublicSubnet["Public Subnet 10.0.1.0/24"]
            ALB["Application Load Balancer\\nALB Port: 80"]
{ec2_section}
        end
        
        subgraph PrivateSubnet["Private Subnet 10.0.2.0/24"]
            DB["{db_info['icon']}\\nEC2 Instance\\nPort: {db_info['port']}"]
        end
        
        subgraph Security["Security Groups"]
            ALBSG["ALB SG Allow: 80"]
            AppSG["App SG Allow: 80, 22"]
            DBSG["DB SG Allow: {db_info['port']}, 22"]
        end
    end

{chr(10).join(connections)}

    ALB -.->|Protected by| ALBSG
    EC2{1 if app_count == 1 else "1"} -.->|Protected by| AppSG
    DB -.->|Protected by| DBSG

    style VPC fill:#e0f2fe,stroke:#0369a1,stroke-width:3px
    style PublicSubnet fill:#fef3c7,stroke:#d97706,stroke-width:2px
    style PrivateSubnet fill:#fce7f3,stroke:#be185d,stroke-width:2px
    style Internet fill:#f3f4f6,stroke:#6b7280,stroke-width:2px
    style ALB fill:#d1fae5,stroke:#059669,stroke-width:2px
    style DB fill:#fce7f3,stroke:#be185d,stroke-width:2px
    style Security fill:#ede9fe,stroke:#7c3aed,stroke-width:2px
"""
            # Add EC2 styling
            for i in range(1, app_count + 1):
                diagram += f"\n    style EC2{i} fill:#dbeafe,stroke:#2563eb,stroke-width:2px"
        
        else:
            # 2-tier architecture (direct connection, no load balancer)
            for i in range(1, app_count + 1):
                connections.append(f"    Users -->|HTTP| EC2{i}")
                if database != "none":
                    db_port = db_info['port']
                    connections.append(f"    EC2{i} -->|{db_info['name']} Port {db_port}| DB")
            
            diagram = f"""graph TB
    subgraph Internet["Internet"]
        Users["Users"]
    end
    
    subgraph VPC["VPC: {region}"]
        subgraph PublicSubnet["Public Subnet 10.0.1.0/24"]
{ec2_section}
        end
        
        subgraph PrivateSubnet["Private Subnet 10.0.2.0/24"]
            DB["{db_info['icon']}\\nEC2 Instance\\nPort: {db_info['port']}"]
        end
        
        subgraph Security["Security Groups"]
            AppSG["App SG Allow: 80, 22"]
            DBSG["DB SG Allow: {db_info['port']}, 22"]
        end
    end

{chr(10).join(connections)}

    EC2{1 if app_count == 1 else "1"} -.->|Protected by| AppSG
    DB -.->|Protected by| DBSG

    style VPC fill:#e0f2fe,stroke:#0369a1,stroke-width:3px
    style PublicSubnet fill:#fef3c7,stroke:#d97706,stroke-width:2px
    style PrivateSubnet fill:#fce7f3,stroke:#be185d,stroke-width:2px
    style Internet fill:#f3f4f6,stroke:#6b7280,stroke-width:2px
    style DB fill:#fce7f3,stroke:#be185d,stroke-width:2px
    style Security fill:#ede9fe,stroke:#7c3aed,stroke-width:2px
"""
            # Add EC2 styling
            for i in range(1, app_count + 1):
                diagram += f"\n    style EC2{i} fill:#dbeafe,stroke:#2563eb,stroke-width:2px"
        
        return diagram
