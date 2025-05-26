import requests
import datetime
import json

from typing import Dict,Type, List, Any
from notion_alchemy.models import NotionModel, NotionDatabaseModel
from notion_alchemy.notion import NotionProperty


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
    
    def get_database(self, database_id: str) -> Dict:
        """Get raw database data from Notion"""
        url = f"{self.base_url}/databases/{database_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()


    def query_database(self, model_class: Type[NotionDatabaseModel], filters: List[dict] = None) -> List[NotionDatabaseModel]:
       
        """Query database with optional filters"""
        if not model_class._database_id:
            raise ValueError("Model class must define _database_id")
        
        url = f"{self.base_url}/databases/{model_class._database_id}/query"
        query = self._build_query_payload(filters)
        
        response = requests.post(url, headers=self.headers, json=query)
        response.raise_for_status()
# melhorar a interação com o retorno
#    quero poder acessar as paginas e fazer operações com elas 
            #exemplo quero acessar todas as paginas da tags casa e excluir as que tem name repetidas, mandando patch com os ids para atualizar a pagina para arquivada    
#    Definir como objetos? 
#    Definir com dataframe?       
        return response.json()['results']

# refazendo
# precisa implementar o or 
    def _build_query_payload(self, filters: List[dict]) -> Dict:
        """
        Recebe uma lista de filtros (cada um já no formato Notion, ex: prop.contains("Python"))
        e monta o payload para a API.
        """
        if not filters:
            return {}

        return {
            "filter": {
                "and": [filters]
            }
        }


# refazer
#feito por ia 
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