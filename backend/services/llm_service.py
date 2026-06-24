"""
LLM Service - Mock Mode Only (No API Key Required)
"""
import json
import re
from typing import Dict, Any
from utils.logger import logger


class LLMService:
    """Service that uses mock responses (no API key needed)"""
    
    def call(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """Generate mock responses without calling any API"""
        logger.info("Using mock LLM response (no API key needed)")
        return self._generate_mock_response(system_prompt, user_prompt)
    
    def _generate_mock_response(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """Generate intelligent mock responses"""
        prompt_lower = user_prompt.lower()
        
        # Stage 1: Intent Extraction
        if "extract structured intent" in system_prompt:
            return self._extract_intent(prompt_lower)
        
        # Stage 2: System Design
        elif "system architect" in system_prompt:
            return self._design_system(user_prompt)
        
        # Stage 3: Schema Generation
        elif "schema generator" in system_prompt:
            return self._generate_schemas(user_prompt)
        
        # Stage 4: Refinement
        else:
            return {"_refined": True, "_notes": "All schemas validated and consistent"}
    
    def _extract_intent(self, prompt: str) -> Dict[str, Any]:
        """Extract intent from user prompt"""
        # Detect app type
        app_type = "web-app"
        if "crm" in prompt: app_type = "crm"
        elif "ecommerce" in prompt or "store" in prompt or "shop" in prompt: app_type = "ecommerce"
        elif "project" in prompt or "task" in prompt or "board" in prompt: app_type = "project-management"
        elif "social" in prompt or "media" in prompt or "post" in prompt: app_type = "social-media"
        elif "learn" in prompt or "course" in prompt or "quiz" in prompt: app_type = "lms"
        
        # Extract features
        features = ["user-authentication"]
        if "contact" in prompt: features.append("contact-management")
        if "payment" in prompt or "pay" in prompt: features.append("payment-processing")
        if "analytics" in prompt or "report" in prompt: features.append("analytics")
        if "premium" in prompt: features.append("premium-plan")
        if "dashboard" in prompt: features.append("dashboard")
        if "role" in prompt: features.append("role-based-access")
        if "collaboration" in prompt: features.append("team-collaboration")
        if "file" in prompt or "share" in prompt: features.append("file-sharing")
        if "time" in prompt or "track" in prompt: features.append("time-tracking")
        
        # Extract entities
        entities = ["users"]
        if "contact" in prompt: entities.append("contacts")
        if "product" in prompt: entities.append("products")
        if "order" in prompt: entities.append("orders")
        if "task" in prompt: entities.append("tasks")
        if "project" in prompt: entities.append("projects")
        if "team" in prompt: entities.append("teams")
        
        return {
            "appType": app_type,
            "features": features,
            "entities": entities,
            "roles": ["admin", "user"],
            "auth": "email-password",
            "payments": "stripe" if "payment" in prompt else None,
            "premium": "subscription" if "premium" in prompt else None,
            "complexity": "complex" if len(features) > 5 else "moderate" if len(features) > 3 else "simple",
            "confidence": 0.85
        }
    
    def _design_system(self, user_prompt: str) -> Dict[str, Any]:
        """Design system architecture"""
        try:
            intent = json.loads(user_prompt)
            entities = intent.get("entities", ["users"])
            roles = intent.get("roles", ["admin", "user"])
        except:
            entities = ["users", "contacts"]
            roles = ["admin", "user"]
        
        return {
            "entities": [
                {"name": e, "fields": ["id", "createdAt", "updatedAt"]} for e in entities
            ],
            "flows": ["login", "signup", "dashboard"],
            "roles": [
                {"name": r, "permissions": ["*" if r == "admin" else "read,write"]} for r in roles
            ],
            "modules": ["auth", "core", "api"],
            "architecture": "monolithic",
            "database": "postgres"
        }
    
    def _generate_schemas(self, user_prompt: str) -> Dict[str, Any]:
        """Generate schemas"""
        try:
            design = json.loads(user_prompt)
            entities = design.get("entities", [])
            entity_names = [e.get("name", "item") for e in entities] if entities else ["users", "contacts"]
        except:
            entity_names = ["users", "contacts"]
        
        return {
            "ui": {
                "pages": [
                    {"name": "login", "path": "/login", "layout": "auth", "requiresAuth": False},
                    {"name": "register", "path": "/register", "layout": "auth", "requiresAuth": False},
                    {"name": "dashboard", "path": "/", "layout": "main", "requiresAuth": True}
                ] + [
                    {"name": e, "path": f"/{e}", "layout": "main", "requiresAuth": True} for e in entity_names
                ],
                "components": ["Navbar", "Sidebar", "Table", "Form", "Modal", "Card"],
                "layout": {
                    "default": "MainLayout",
                    "auth": "AuthLayout"
                }
            },
            "api": {
                "endpoints": [
                    {"path": "/auth/login", "method": "POST"},
                    {"path": "/auth/register", "method": "POST"},
                    {"path": "/auth/logout", "method": "POST"},
                    {"path": "/auth/me", "method": "GET"}
                ] + [
                    {"path": f"/{e}", "method": "GET"} for e in entity_names
                ] + [
                    {"path": f"/{e}", "method": "POST"} for e in entity_names
                ] + [
                    {"path": f"/{e}/{{id}}", "method": "GET"} for e in entity_names
                ] + [
                    {"path": f"/{e}/{{id}}", "method": "PUT"} for e in entity_names
                ] + [
                    {"path": f"/{e}/{{id}}", "method": "DELETE"} for e in entity_names
                ]
            },
            "db": {
                "tables": [
                    {
                        "name": "users",
                        "columns": ["id", "email", "password_hash", "name", "role", "created_at", "updated_at"]
                    }
                ] + [
                    {
                        "name": e,
                        "columns": ["id", "user_id", "created_at", "updated_at"]
                    } for e in entity_names if e != "users"
                ],
                "relations": [
                    {"from": f"{e}.user_id", "to": "users.id"} for e in entity_names if e != "users"
                ]
            },
            "auth": {
                "roles": ["admin", "user"],
                "permissions": {
                    "admin": ["*"],
                    "user": ["read", "write:self"]
                },
                "rules": [
                    {"role": "admin", "resource": "*", "action": "*"},
                    {"role": "user", "resource": "profile", "action": "read,update"}
                ]
            }
        }


# Create singleton instance
llm_service = LLMService()