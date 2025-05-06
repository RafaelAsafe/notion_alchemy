import requests
import datetime
from typing import Dict,Type, List, Any
from models import NotionModel


class NotionClient:
    """Hybrid Notion API client with model support"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
    
    def get_page(self, page_id: str) -> Dict:
        """Get raw page data from Notion"""
        url = f"{self.base_url}/pages/{page_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def query_database(self, model_class: Type[NotionModel], **filters) -> List[NotionModel]:
        """Query database with optional filters"""
        if not model_class._database_id:
            raise ValueError("Model class must define _database_id")
        
        url = f"{self.base_url}/databases/{model_class._database_id}/query"
        payload = self._build_query_payload(filters)
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        return [
            model_class.from_notion(page)
            for page in response.json()['results']
        ]
    
    def _build_query_payload(self, filters: Dict) -> Dict:
        """Convert Python filters to Notion API format"""
        if not filters:
            return {}
        
        filter_conditions = []
        for field, value in filters.items():
            filter_conditions.append({
                "property": field,
                self._get_filter_type(value): {
                    "equals": str(value) if not isinstance(value, (bool, int, float)) else value
                }
            })
        
        return {
            "filter": {
                "and": filter_conditions
            }
        }
    
    def _get_filter_type(self, value: Any) -> str:
        """Determine filter type based on value"""
        if isinstance(value, bool):
            return "checkbox"
        elif isinstance(value, (int, float)):
            return "number"
        elif isinstance(value, datetime):
            return "date"
        return "rich_text"
    
    def create_page(self, model: NotionModel) -> NotionModel:
        """Create new page from model"""
        if not model._database_id:
            raise ValueError("Model must have _database_id set")
        
        url = f"{self.base_url}/pages"
        payload = {
            "parent": {"database_id": model._database_id},
            "properties": model.to_notion_properties()
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        return model.__class__.from_notion(response.json())
    
    def update_page(self, model: NotionModel) -> NotionModel:
        """Update existing page"""
        if not model.id:
            raise ValueError("Model must have an id to update")
        
        url = f"{self.base_url}/pages/{model.id}"
        payload = {
            "properties": model.to_notion_properties()
        }
        
        response = requests.patch(url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        return model.__class__.from_notion(response.json())