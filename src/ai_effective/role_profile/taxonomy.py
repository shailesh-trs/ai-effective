"""Role taxonomy: domains, identifying keywords, and expected task types.

Each domain entry has:
  keywords      — terms that signal this role in a job description
  task_keywords — dict mapping task-type name → list of detection phrases
                  (used by heuristics.py to classify query intent)
"""

ROLE_TAXONOMY: dict[str, dict] = {
    "software_engineering": {
        "keywords": [
            "software", "engineer", "developer", "programming", "coding",
            "backend", "frontend", "fullstack", "api", "python", "javascript",
            "typescript", "java", "golang", "rust", "react", "node", "django",
            "flask", "database", "sql", "nosql", "git", "docker", "kubernetes",
            "microservices", "architecture", "testing", "cicd", "repository",
            "deployment", "refactor", "algorithm", "data structure", "scalability",
            "codebase", "pull request", "sprint", "agile",
        ],
        "task_keywords": {
            "code_review": [
                "review", "pull request", "pr", "diff", "refactor", "code smell",
                "linting", "style", "readability",
            ],
            "debugging": [
                "bug", "error", "fix", "debug", "issue", "exception", "crash",
                "traceback", "stack trace", "reproduce", "root cause",
            ],
            "code_generation": [
                "implement", "create a function", "generate code", "write a function",
                "build a", "function that", "class that", "algorithm for",
                "write a class", "write a script",
            ],
            "documentation": [
                "document", "readme", "docstring", "comment", "explain this code",
                "describe", "wiki", "api docs",
            ],
            "testing": [
                "test", "unit test", "integration test", "mock", "assert",
                "coverage", "pytest", "jest", "test case",
            ],
            "architecture_design": [
                "design", "architecture", "system design", "pattern",
                "data model", "schema", "diagram", "service boundary",
            ],
            "performance": [
                "optimize", "performance", "latency", "memory leak", "cache",
                "bottleneck", "profiling", "throughput", "slow query",
            ],
        },
    },

    "data_science": {
        "keywords": [
            "data", "science", "analyst", "machine learning", "statistics",
            "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "keras",
            "model", "dataset", "visualization", "feature", "training",
            "prediction", "classification", "regression", "clustering", "nlp",
            "deep learning", "neural network", "spark", "etl", "pipeline",
            "hypothesis", "experiment", "dashboard", "tableau", "power bi",
            "a/b test", "feature engineering", "model evaluation",
        ],
        "task_keywords": {
            "data_analysis": [
                "analyze", "explore", "eda", "trend", "pattern", "insight",
                "summary statistics", "describe the data", "distribution of",
            ],
            "model_building": [
                "model", "train", "predict", "classify", "fit", "hyperparameter",
                "cross-validation", "evaluate", "baseline model",
            ],
            "visualization": [
                "plot", "chart", "visualize", "graph", "histogram", "heatmap",
                "matplotlib", "seaborn", "plotly", "dashboard",
            ],
            "feature_engineering": [
                "feature", "transform", "encode", "scale", "normalize",
                "one-hot", "embedding", "feature selection",
            ],
            "data_cleaning": [
                "clean", "missing value", "null", "nan", "duplicate",
                "outlier", "preprocess", "impute", "drop column",
            ],
            "statistical_analysis": [
                "hypothesis test", "significance", "p-value", "confidence interval",
                "correlation", "variance", "anova", "chi-square",
            ],
            "reporting": [
                "report", "summarize findings", "present results", "stakeholder",
                "executive summary", "slide", "notebook",
            ],
        },
    },

    "product_management": {
        "keywords": [
            "product", "manager", "roadmap", "user story", "stakeholder",
            "requirements", "sprint", "agile", "scrum", "backlog", "feature",
            "strategy", "metrics", "kpi", "okr", "customer", "market",
            "competitive", "prioritize", "launch", "mvp", "epic", "persona",
            "user research", "go-to-market", "north star metric",
        ],
        "task_keywords": {
            "requirements_writing": [
                "user story", "acceptance criteria", "prd", "requirements doc",
                "write an epic", "feature spec", "product brief",
            ],
            "roadmap_planning": [
                "roadmap", "prioritize", "quarter", "milestone", "timeline",
                "now next later", "planning", "release plan",
            ],
            "stakeholder_communication": [
                "stakeholder update", "status update", "presentation",
                "alignment", "meeting notes", "executive", "communicate to",
            ],
            "market_research": [
                "competitor", "market analysis", "positioning", "differentiation",
                "survey", "swot", "market size", "benchmark",
            ],
            "metrics_analysis": [
                "metric", "kpi", "okr", "retention", "conversion", "funnel",
                "churn", "engagement", "dau", "mau", "north star",
            ],
            "user_research": [
                "user interview", "persona", "feedback", "pain point",
                "job to be done", "usability", "user testing",
            ],
        },
    },

    "marketing": {
        "keywords": [
            "marketing", "content", "campaign", "brand", "seo", "social media",
            "email", "copywriting", "advertising", "growth", "acquisition",
            "retention", "funnel", "conversion", "audience", "engagement",
            "analytics", "lead generation", "demand gen", "b2b", "b2c",
            "messaging", "positioning", "influencer", "paid media",
        ],
        "task_keywords": {
            "content_creation": [
                "blog post", "article", "write copy", "headline", "caption",
                "content calendar", "social post", "case study",
            ],
            "campaign_planning": [
                "campaign", "channel strategy", "budget", "launch plan",
                "go-to-market", "audience targeting", "campaign brief",
            ],
            "seo_optimization": [
                "seo", "keyword research", "meta description", "organic",
                "backlink", "search ranking", "serp", "on-page",
            ],
            "email_marketing": [
                "email", "newsletter", "subject line", "open rate",
                "drip campaign", "email sequence", "cta",
            ],
            "social_media": [
                "social", "instagram", "linkedin", "twitter", "post",
                "hashtag", "engagement rate", "community",
            ],
            "analytics_reporting": [
                "analytics", "roi", "attribution", "performance report",
                "campaign results", "cost per", "roas",
            ],
        },
    },

    "finance": {
        "keywords": [
            "finance", "accounting", "financial", "budget", "forecast",
            "revenue", "cost", "profit", "margin", "cash flow", "balance sheet",
            "income statement", "valuation", "dcf", "model", "variance",
            "reporting", "audit", "compliance", "tax", "investment", "portfolio",
            "risk", "liquidity", "p&l", "ebitda", "capex", "opex",
        ],
        "task_keywords": {
            "financial_modeling": [
                "financial model", "dcf", "forecast", "projection", "valuation",
                "scenario analysis", "sensitivity", "build a model",
            ],
            "budget_analysis": [
                "budget", "variance analysis", "actual vs", "forecast vs",
                "overspend", "allocation", "budget review",
            ],
            "reporting": [
                "earnings", "quarterly report", "annual report", "financial statement",
                "p&l summary", "board presentation",
            ],
            "compliance_audit": [
                "audit", "compliance", "sox", "internal control", "reconcile",
                "review controls", "regulatory",
            ],
            "investment_analysis": [
                "investment", "irr", "npv", "return on", "portfolio analysis",
                "due diligence", "cap table",
            ],
        },
    },

    "hr_people": {
        "keywords": [
            "hr", "human resources", "recruiting", "talent", "hiring",
            "onboarding", "performance", "engagement", "culture", "compensation",
            "benefits", "employee", "workforce", "learning", "development",
            "diversity", "inclusion", "policy", "handbook", "job description",
            "interview", "offer letter", "people operations",
        ],
        "task_keywords": {
            "recruiting": [
                "job description", "job posting", "interview questions",
                "candidate", "screening", "offer letter", "sourcing",
            ],
            "onboarding": [
                "onboarding", "new hire", "orientation", "checklist",
                "first day", "welcome email",
            ],
            "performance_management": [
                "performance review", "feedback", "goal setting", "pip",
                "1:1", "rating", "development plan",
            ],
            "policy_writing": [
                "policy", "employee handbook", "guideline", "procedure",
                "code of conduct", "leave policy",
            ],
            "employee_communication": [
                "announcement", "all-hands", "town hall", "employee update",
                "internal communication",
            ],
        },
    },

    "legal_compliance": {
        "keywords": [
            "legal", "lawyer", "attorney", "contract", "compliance",
            "regulation", "gdpr", "privacy", "intellectual property", "ip",
            "litigation", "clause", "agreement", "terms", "policy", "risk",
            "liability", "court", "jurisdiction", "nda", "msa", "sow",
        ],
        "task_keywords": {
            "contract_review": [
                "review this contract", "redline", "clause", "agreement",
                "terms and conditions", "nda review", "contract language",
            ],
            "compliance_analysis": [
                "gdpr", "hipaa", "compliance requirement", "regulatory",
                "gap analysis", "risk assessment", "audit",
            ],
            "policy_drafting": [
                "draft a policy", "privacy policy", "terms of service",
                "acceptable use", "data retention",
            ],
            "risk_assessment": [
                "legal risk", "liability", "exposure", "mitigate",
                "indemnification", "force majeure",
            ],
        },
    },

    "design_ux": {
        "keywords": [
            "design", "ux", "ui", "user experience", "figma", "prototype",
            "wireframe", "mockup", "visual", "typography", "color palette",
            "layout", "accessibility", "user testing", "usability",
            "interaction design", "design system", "component library",
        ],
        "task_keywords": {
            "wireframing": [
                "wireframe", "prototype", "mockup", "user flow",
                "layout", "sketch the", "low-fidelity",
            ],
            "user_research": [
                "user research", "usability test", "interview", "persona",
                "user journey", "pain points", "empathy map",
            ],
            "visual_design": [
                "color scheme", "typography", "style guide", "brand identity",
                "design tokens", "visual hierarchy",
            ],
            "design_writing": [
                "microcopy", "button label", "error message", "onboarding copy",
                "ui text", "tooltip",
            ],
        },
    },

    "devops_infrastructure": {
        "keywords": [
            "devops", "infrastructure", "cloud", "aws", "azure", "gcp",
            "kubernetes", "docker", "terraform", "ansible", "cicd", "jenkins",
            "github actions", "monitoring", "alerting", "reliability", "sre",
            "on-call", "incident", "linux", "bash", "networking", "iam",
            "load balancer", "helm", "prometheus", "grafana",
        ],
        "task_keywords": {
            "pipeline_setup": [
                "ci/cd", "pipeline", "github actions", "build step",
                "deploy workflow", "jenkins", "artifact",
            ],
            "infrastructure_as_code": [
                "terraform", "ansible", "cloudformation", "provision",
                "iac", "module", "infrastructure code",
            ],
            "monitoring_alerting": [
                "monitor", "alert", "dashboard", "slo", "sla",
                "prometheus", "grafana", "log", "trace",
            ],
            "incident_response": [
                "incident", "outage", "on-call", "postmortem", "runbook",
                "escalate", "pagerduty", "root cause",
            ],
            "security": [
                "iam role", "permission", "secret", "certificate",
                "vulnerability", "patch", "least privilege",
            ],
        },
    },

    "operations": {
        "keywords": [
            "operations", "process", "efficiency", "workflow", "vendor",
            "supply chain", "logistics", "inventory", "procurement", "sop",
            "capacity", "quality", "lean", "six sigma", "project management",
            "coordination", "cross-functional",
        ],
        "task_keywords": {
            "process_improvement": [
                "improve process", "sop", "workflow optimization", "lean",
                "eliminate waste", "efficiency", "bottleneck",
            ],
            "project_coordination": [
                "project plan", "timeline", "milestone", "track progress",
                "gantt", "status report", "coordinate",
            ],
            "vendor_management": [
                "vendor", "supplier", "rfp", "procurement", "contract",
                "negotiation", "third party",
            ],
            "reporting": [
                "ops report", "kpi dashboard", "weekly update", "capacity",
                "metrics summary",
            ],
        },
    },
}
