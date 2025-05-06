from dataclasses import dataclass, field
from typing import Dict, Optional, Any
from datetime import datetime

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
        return ''.join([t['plain_text'] for t in data.get('title', [])])

    def _format_value(self, value: str) -> Dict:
        return {"title": [{"text": {"content": value}}]}


@dataclass
class SelectProperty(NotionProperty):
    """Handles Notion select properties"""
    def __init__(self, name: str):
        super().__init__(name=name, type="select")

    def _parse_value(self, data: Dict) -> Optional[str]:
        select = data.get('select')
        return select['name'] if select else None

    def _format_value(self, value: str) -> Dict:
        return {"select": {"name": value}}


@dataclass
class DateProperty(NotionProperty):
    """Handles Notion date properties"""
    def __init__(self, name: str):
        super().__init__(name=name, type="date")

    def _parse_value(self, data: Dict) -> Optional[datetime]:
        date_data = data.get('date')
        if not date_data:
            return None
        return datetime.fromisoformat(date_data['start'])

    def _format_value(self, value: datetime) -> Dict:
        return {"date": {"start": value.isoformat()}}