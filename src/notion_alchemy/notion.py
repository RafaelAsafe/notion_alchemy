from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional, Any, List

from abc import ABC, abstractmethod

# essa classe de options ta meio perdida aqui coitada kkkkkkk
@dataclass
class OptionProperty:
    id: str = ""
    name: str = ""
    color: str = ""
    description: str = ""

@dataclass
class NotionProperty(ABC):
    property_id: str = ""
    name: str = ""
    dtype: str = ""
    value: Any = None
    raw_data: Dict = field(default_factory=dict)


    def __post_init__(self):
        self.value = self._parse_value(self.raw_data)
    
    def from_notion(self, data: Dict) -> None:
        self.raw_data = data
        self.value = self._parse_value(data)

    def to_notion(self) -> Dict:
        return self._format_value(self.value)

    @abstractmethod
    def _parse_value(self, data: Dict) -> Any:
        pass
    
    @abstractmethod
    def _format_value(self, value: Any) -> Dict:
        pass
    

@dataclass
class TitleProperty(NotionProperty):
    dtype: str = "title"

    def _parse_value(self, data: Dict) -> str:
        return "".join([t["plain_text"] for t in data.get("title", [])])

    def _format_value(self, value: str) -> Dict:
        return {"title": [{"text": {"content": value}}]}

    def contains(self, value): return {
        "property": self.name, self.dtype: {"contains": value}}

    def does_not_contain(self, value): return {
        "property": self.name, self.dtype: {"does_not_contain": value}}

    def starts_with(self, value): return {
        "property": self.name, self.dtype: {"starts_with": value}}
    def ends_with(self, value): return {
        "property": self.name, self.dtype: {"ends_with": value}}

@dataclass
class RichTextProperty(NotionProperty):
    dtype: str = "rich_text"


    def _parse_value(self, data: Dict) -> str:
        return "".join([t["plain_text"] for t in data.get("rich_text", [])])

    def _format_value(self, value: str) -> Dict:
        return {"rich_text": [{"text": {"content": value}}]}

    def contains(self, value): return {
        "property": self.name, self.dtype: {"contains": value}}

    def does_not_contain(self, value): return {
        "property": self.name, self.dtype: {"does_not_contain": value}}

    def starts_with(self, value): return {
        "property": self.name, self.dtype: {"starts_with": value}}
    def ends_with(self, value): return {
        "property": self.name, self.dtype: {"ends_with": value}}

@dataclass
class StatusProperty(NotionProperty):
    dtype: str = "status"

    def _parse_value(self, data: Dict) -> Optional[str]:
        status = data.get("status")
        return status.get("name","") if status else None

    def _format_value(self, value: str) -> Dict:
        return {"status": {"name": value}}

    def equals(self, value): return {
        "property": self.name, self.dtype: {"equals": value}}

    def does_not_equal(self, value): return {
        "property": self.name, self.dtype: {"does_not_equal": value}}

    def is_empty(self): return {
        "property": self.name, self.dtype: {"is_empty": True}}
    def is_not_empty(self): return {
        "property": self.name, self.dtype: {"is_not_empty": True}}

@dataclass
class NumberProperty(NotionProperty):
    dtype: str = "number"
    value: Optional[float] = None


    def _parse_value(self, data: Dict) -> Optional[float]:
        return data.get("number")

    def _format_value(self, value: float) -> Dict:
        return {"number": value}

    def greater_than(self, value): return {
        "property": self.name, self.dtype: {"greater_than": value}}

    def less_than(self, value): return {
        "property": self.name, self.dtype: {"less_than": value}}

    def greater_than_or_equal_to(self, value): return {
        "property": self.name, self.dtype: {"greater_than_or_equal_to": value}}
    def less_than_or_equal_to(self, value): return {
        "property": self.name, self.dtype: {"less_than_or_equal_to": value}}

@dataclass
class CheckboxProperty(NotionProperty):
    dtype: str = "checkbox" 
    value: bool = False


    def _parse_value(self, data: Dict) -> Optional[bool]:
        return data.get("checkbox")

    def _format_value(self, value: bool) -> Dict:
        return {"checkbox": value}

    def equals(self, value: bool): return {
        "property": self.name, self.dtype: {"equals": value}}

@dataclass
class SelectProperty(NotionProperty):
    dtype: str = "select"

    def _parse_value(self, data: Dict) -> Optional[str]:
        select = data.get("select")
        return select.get("name","") if select else None

    def _format_value(self, value: str) -> Dict:
        return {"select": {"name": value}}

@dataclass
class MultiSelectProperty(NotionProperty):
    dtype: str = "multi_select"

    def _parse_value(self, data: Dict) -> Optional[List[str]]:
        # Extrai os nomes das opções selecionadas
        multi_select = data.get("multi_select")
        if multi_select and isinstance(multi_select, list):
            return [opt.get("name") for opt in multi_select]
        return []
    
    def _format_value(self, value: List[str]) -> Dict:
        # Formata para o padrão esperado pela API do Notion
        return {"multi_select": [{"name": v} for v in value]}

    def contains(self, value): return {
        "property": self.name, self.dtype: {"contains": value}}
    def does_not_contain(self, value): return {
        "property": self.name, self.dtype: {"does_not_contain": value}}

@dataclass
class DateProperty(NotionProperty):
    dtype: str = "date"

    def _parse_value(self, data: Dict) -> Optional[datetime]:
        date_data = data.get("date")
        if not date_data:
            return None
        return datetime.fromisoformat(date_data["start"])

    def _format_value(self, value: datetime) -> Dict:
        return {"date": {"start": value.isoformat()}}

    def before(self, value): return {
        "property": self.name, self.dtype: {"before": value}}

    def after(self, value): return {
        "property": self.name, self.dtype: {"after": value}}

    def on_or_before(self, value): return {
        "property": self.name, self.dtype: {"on_or_before": value}}

    def on_or_after(self, value): return {
        "property": self.name, self.dtype: {"on_or_after": value}}

    def past_week(self): return {
        "property": self.name, self.dtype: {"past_week": {}}}

    def past_month(self): return {
        "property": self.name, self.dtype: {"past_month": {}}}

    def past_year(self): return {
        "property": self.name, self.dtype: {"past_year": {}}}

    def this_week(self): return {
        "property": self.name, self.dtype: {"this_week": {}}}

    def next_week(self): return {
        "property": self.name, self.dtype: {"next_week": {}}}

    def this_month(self): return {
        "property": self.name, self.dtype: {"this_month": {}}}

    def next_month(self): return {
        "property": self.name, self.dtype: {"next_month": {}}}

    def this_year(self): return {
        "property": self.name, self.dtype: {"this_year": {}}}
    def next_year(self): return {
        "property": self.name, self.dtype: {"next_year": {}}}

@dataclass
class PeopleProperty(NotionProperty):
    dtype: str = "people"

    def _parse_value(self, data: Dict) -> Optional[list]:
        # Extrai lista de nomes das pessoas
        people = data.get("people")
        if people and isinstance(people, list):
            return [p.get("name") for p in people]
        return []

    def _format_value(self, value: list) -> Dict:
        # Espera uma lista de nomes (ou ids, dependendo do uso)
        return {"people": value}

    def contains(self, value): return {
        "property": self.name, self.dtype: {"contains": value}}
    def does_not_contain(self, value): return {
        "property": self.name, self.dtype: {"does_not_contain": value}}

@dataclass
class FilesProperty(NotionProperty):
    dtype: str = "files"

    def _parse_value(self, data: Dict) -> Optional[list]:
        files = data.get("files")
        if files and isinstance(files, list):
            return [f.get("name") for f in files]
        return []

    def _format_value(self, value: list) -> Dict:
        # Espera uma lista de arquivos (nomes ou urls)
        return {"files": value}

@dataclass
class RelationProperty(NotionProperty):
    dtype: str = "relation"

    def _parse_value(self, data: Dict) -> Optional[list]:
        relation = data.get("relation",{})
        if relation and isinstance(relation, list):
            return [r.get("id","None") for r in relation]
        return ["None"]

    def _format_value(self, value: list) -> Dict:
        # Espera uma lista de ids de páginas relacionadas
        return {"relation": [{"id": v} for v in value]}

    def contains(self, value): return {
        "property": self.name, self.dtype: {"contains": value}}
    def does_not_contain(self, value): return {
        "property": self.name, self.dtype: {"does_not_contain": value}}

@dataclass
class FormulaProperty(NotionProperty):
    dtype: str = "formula"

    def _parse_value(self, data: Dict) -> Any:
        # Retorna o valor bruto da fórmula (pode ser string, number, boolean, date)
        return data.get("formula")

    def _format_value(self, value: Any) -> Dict:
        # Fórmulas são calculadas pelo Notion, geralmente não são enviadas
        return {"formula": value}

    def string_contains(self, value): return {
        "property": self.name, self.dtype: {"string": {"contains": value}}}

    def string_starts_with(self, value): return {
        "property": self.name, self.dtype: {"string": {"starts_with": value}}}

    def string_ends_with(self, value): return {
        "property": self.name, self.dtype: {"string": {"ends_with": value}}}

    def number_equals(self, value): return {
        "property": self.name, self.dtype: {"number": {"equals": value}}}

    def number_greater_than(self, value): return {
        "property": self.name, self.dtype: {"number": {"greater_than": value}}}

    def number_less_than(self, value): return {
        "property": self.name, self.dtype: {"number": {"less_than": value}}}

    def checkbox_equals(self, value): return {
        "property": self.name, self.dtype: {"checkbox": {"equals": value}}}

    def date_before(self, value): return {
        "property": self.name, self.dtype: {"date": {"before": value}}}

    def date_after(self, value): return {
        "property": self.name, self.dtype: {"date": {"after": value}}}

# Mapeamento do tipo do Notion para a classe Python correspondente
PROPERTY_TYPE_MAP = {
    "title": TitleProperty,
    "rich_text": RichTextProperty,
    "number": NumberProperty,
    "checkbox": CheckboxProperty,
    "select": SelectProperty,
    "multi_select": MultiSelectProperty,
    "date": DateProperty,
    "people": PeopleProperty,
    "files": FilesProperty,
    "relation": RelationProperty,
    "formula": FormulaProperty,
    "status": StatusProperty
}

def get_property_class(property_type: str) -> type:
    if property_type in PROPERTY_TYPE_MAP:
        return PROPERTY_TYPE_MAP[property_type]
    raise ValueError(f"Tipo de propriedade Notion não suportado: {property_type}")
    
def create_property(name: str, property_type: str, raw_data: Optional[Dict] = None) -> NotionProperty:
    prop_class = get_property_class(property_type)
    return prop_class(name=name, raw_data=raw_data)