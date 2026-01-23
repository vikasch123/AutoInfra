"""
Diagram Generator - Generates Mermaid architecture diagrams
Supports 2-tier, 3-tier, and various tech stacks
"""

from typing import Dict, Any


class DiagramGenerator:
    """Generates Mermaid architecture diagrams from intent"""
    
    def generate(self, intent: Dict[str, Any]) -> str:
        """Generate hardcoded Mermaid diagram based on intent for demo stability"""
        
        app = intent.get("app", "other").lower()
        database = intent.get("database", "none").lower()
        
        # Scenario 1: User Request (Golang + Postgres + Nginx + LB)
        if app == "golang" and database == "postgresql":
            return """graph TB
    subgraph Internet ["Internet"]
        Users["Users"]
    end
    
    subgraph VPC ["VPC: us-east-1"]
        subgraph PublicSubnet ["Public Subnet"]
            Nginx["Nginx Reverse Proxy<br/>Port: 80"]
            ALB["Application Load Balancer<br/>Port: 80"]
            Go1["Go App Instance 1<br/>Port: 8080"]
            Go2["Go App Instance 2<br/>Port: 8080"]
        end
        
        subgraph PrivateSubnet ["Private Subnet"]
            DB["PostgreSQL Database<br/>Port: 5432"]
        end
    end

    Users -->|HTTPS| Nginx
    Nginx -->|HTTP| ALB
    ALB -->|Round Robin| Go1
    ALB -->|Round Robin| Go2
    Go1 -->|SQL| DB
    Go2 -->|SQL| DB

    style VPC fill:#e0f2fe,stroke:#0369a1,stroke-width:2px
    style PublicSubnet fill:#fef3c7,stroke:#d97706,stroke-width:2px
    style PrivateSubnet fill:#fce7f3,stroke:#be185d,stroke-width:2px
    style Nginx fill:#d1fae5,stroke:#059669
    style ALB fill:#d1fae5,stroke:#059669
    style Go1 fill:#dbeafe,stroke:#2563eb
    style Go2 fill:#dbeafe,stroke:#2563eb
    style DB fill:#fce7f3,stroke:#be185d
"""

        # Scenario 2: Node.js + MongoDB (Standard PoC)
        if app == "nodejs" and database == "mongodb":
            return """graph TB
    subgraph Internet ["Internet"]
        Users["Users"]
    end
    
    subgraph VPC ["AWS Cloud"]
        subgraph Public ["Public Subnet"]
            ALB["Load Balancer<br/>AWS ALB"]
            Node1["Node.js App<br/>Instance A"]
            Node2["Node.js App<br/>Instance B"]
        end
        
        subgraph Private ["Private Subnet"]
            Mongo["MongoDB Atlas<br/>Managed Cluster"]
        end
    end

    Users -->|HTTP| ALB
    ALB -->|Traffic| Node1
    ALB -->|Traffic| Node2
    Node1 -->|Mongoose| Mongo
    Node2 -->|Mongoose| Mongo

    style VPC fill:#f8fafc,stroke:#475569
    style Public fill:#f0f9ff,stroke:#0ea5e9
    style Private fill:#fdf4ff,stroke:#d946ef
    style ALB fill:#fff7ed,stroke:#ea580c
    style Node1 fill:#dcfce7,stroke:#16a34a
    style Node2 fill:#dcfce7,stroke:#16a34a
    style Mongo fill:#ecfccb,stroke:#65a30d
"""

        # Scenario 3: Python + Redis
        if app == "python" and database == "redis":
            return """graph LR
    subgraph Cloud ["Cloud Infrastructure"]
        Users(("Users"))
        
        subgraph AppLayer ["App Layer"]
            Py["Python Worker<br/>Flask/Django"]
        end
        
        subgraph CacheLayer ["Cache Layer"]
            Redis[("Redis Cache<br/>In-Memory")]
        end
    end

    Users -->|API Requests| Py
    Py <-->|Get/Set| Redis

    style Cloud fill:#fafafa,stroke:#ccc
    style AppLayer fill:#e0f7fa,stroke:#006064
    style CacheLayer fill:#ffebee,stroke:#b71c1c
    style Py fill:#fff3e0,stroke:#e65100
    style Redis fill:#f3e5f5,stroke:#4a148c
"""

        # Scenario 4: Java + MySQL
        if app == "java" and database == "mysql":
            return """graph TB
    subgraph Enterprise_VPC ["Enterprise VPC"]
        LB["Hardware LB"]
        
        subgraph App_Server ["Application Server"]
            Java["Java Spring Boot<br/>JVM Container"]
        end
        
        subgraph Data_Tier ["Data Tier"]
            MySQL[("MySQL Database<br/>Primary")]
            Replica[("MySQL Replica<br/>Read-Only")]
        end
    end

    Client -->|TCP| LB
    LB -->|HTTP| Java
    Java -->|JDBC Write| MySQL
    Java -->|JDBC Read| Replica
    MySQL -.->|Replication| Replica

    style Enterprise_VPC fill:#eceff1,stroke:#455a64
    style Java fill:#fbe9e7,stroke:#bf360c
    style MySQL fill:#e1f5fe,stroke:#01579b
    style Replica fill:#e1f5fe,stroke:#01579b,stroke-dasharray: 5 5
"""

        # Scenario 5: Python + Postgres (Data Science / API)
        if app == "python" and database == "postgresql":
            return """graph TB
    subgraph AWS ["AWS Region"]
        API["FastAPI / Flask<br/>Python Service"]
        DB[("PostgreSQL<br/>RDS Instance")]
        S3[("S3 Bucket<br/>Object Storage")]
    end

    User --> API
    API -->|SQL Queries| DB
    API -->|File Uploads| S3

    style AWS fill:#f5f5f5,stroke:#232f3e
    style API fill:#ffecb3,stroke:#ff6f00
    style DB fill:#e3f2fd,stroke:#1565c0
    style S3 fill:#e8f5e9,stroke:#2e7d32
"""

        # Scenario 6: Ruby + Postgres
        if "ruby" in (app or ""):
            return """graph TB
    subgraph Heroku_Like ["App Environment"]
        Router["Router / LB"]
        Web["Rails Dyno<br/>Web Process"]
        Worker["Sidekiq Worker<br/>Background Job"]
        PG[("Postgres<br/>Database")]
        Redis[("Redis<br/>Job Queue")]
    end

    User --> Router
    Router --> Web
    Web -->|Enqueue| Redis
    Redis -->|Dequeue| Worker
    Web -->|Query| PG
    Worker -->|Process| PG

    style Web fill:#fce4ec,stroke:#880e4f
    style Worker fill:#f3e5f5,stroke:#4a148c
    style PG fill:#e3f2fd,stroke:#0d47a1
"""

        # Scenario 7: Simple / Fallback
        return """graph TB
    subgraph Cloud ["Simple Cloud Deployment"]
        User["User"]
        Server["Single Server<br/>App + DB"]
    end

    User -->|HTTP| Server

    style Server fill:#f5f5f5,stroke:#333
"""
