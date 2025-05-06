from dataclasses import dataclass, field
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, Optional, Any


@dataclass
class NotionProperty:
    """Base class for Notion property handling"""

    name: str
    type: str
    value: Any = None
    raw_data: Dict = field(default_factory=dict)

    def from_notion(self, data: Dict) -> None:
        """Parse Notion API data into Python value"""
        self.raw_data = data
        self.value = self._parse_value(data)

    def to_notion(self) -> Dict:
        """Convert Python value back to Notion format"""
        return self._format_value(self.value)

    def _parse_value(self, data: Dict) -> Any:
        """Implement in child classes"""
        raise NotImplementedError

    def _format_value(self, value: Any) -> Dict:
        """Implement in child classes"""
        raise NotImplementedError

@dataclass
class TitleProperty(NotionProperty):
    """Handles Notion title properties"""

    def __init__(self, name: str):
        super().__init__(name=name, type="title")

    def _parse_value(self, data: Dict) -> str:
        return "".join([t["plain_text"] for t in data.get("title", [])])

    def _format_value(self, value: str) -> Dict:
        return {"title": [{"text": {"content": value}}]}


@dataclass
class SelectProperty(NotionProperty):
    """Handles Notion select properties"""

    def __init__(self, name: str):
        super().__init__(name=name, type="select")

    def _parse_value(self, data: Dict) -> Optional[str]:
        select = data.get("select")
        return select["name"] if select else None

    def _format_value(self, value: str) -> Dict:
        return {"select": {"name": value}}


@dataclass
class DateProperty(NotionProperty):
    """Handles Notion date properties"""

    def __init__(self, name: str):
        super().__init__(name=name, type="date")

    def _parse_value(self, data: Dict) -> Optional[datetime]:
        date_data = data.get("date")
        if not date_data:
            return None
        return datetime.fromisoformat(date_data["start"])

    def _format_value(self, value: datetime) -> Dict:
        return {"date": {"start": value.isoformat()}}

    from typing import Dict, List, Optional, Union, Any

class RichTextProperty:
    """Versão simplificada para manipular textos formatados do Notion"""
    
    def __init__(self, name: str):
        self.name = name
        self.text = ""  # Armazena o texto simples
        self.formats = []  # Armazena a formatação
        
    def from_notion(self, notion_data: list) -> None:
        """Converte do formato Notion para texto simples"""
        self.text = ""
        self.formats = []
        
        for item in notion_data:
            if 'text' in item:
                self.text += item['text']['content']
                self.formats.append({
                    'bold': item.get('annotations', {}).get('bold', False),
                    'italic': item.get('annotations', {}).get('italic', False),
                    'link': item['text'].get('link', {}).get('url')
                })
    
    def to_notion(self) -> list:
        """Converte para o formato Notion"""
        if not self.text:
            return []
            
        return [{
            "type": "text",
            "text": {"content": self.text},
            "annotations": {
                "bold": any(fmt.get('bold') for fmt in self.formats),
                "italic": any(fmt.get('italic') for fmt in self.formats)
            }
        }]
    
    def __str__(self) -> str:
        return self.text