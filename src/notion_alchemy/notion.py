from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional, Any, List

@dataclass
class OptionProperty:
    color: str = "default"
    id: str = "default"
    name: str = "default"


#feito por ia 
@dataclass
class NotionProperty:
    name: str = ""
    type: str = ""
    value: Any = None
    raw_data: Dict = field(default_factory=dict)
    
    def from_notion(self, data: Dict) -> None:
        self.raw_data = data
        self.value = self._parse_value(data)
    
    def to_notion(self) -> Dict:
        return self._format_value(self.value)

    
    def _parse_value(self, data: Dict) -> Any:
        raise NotImplementedError
   
    def _format_value(self, value: Any) -> Dict:
        raise NotImplementedError

    # Filtros genéricos
    def equals(self, value): return {
        "property": self.name, self.type: {"equals": value}}

    def does_not_equal(self, value): return {
        "property": self.name, self.type: {"does_not_equal": value}}

    def is_empty(self): return {
        "property": self.name, self.type: {"is_empty": True}}
    def is_not_empty(self): return {
        "property": self.name, self.type: {"is_not_empty": True}}
    
     


@dataclass
class TitleProperty(NotionProperty):
    def __init__(self, name: str):
        super().__init__(name=name, type="title")

    def _parse_value(self, data: Dict) -> str:
        return "".join([t["plain_text"] for t in data.get("title", [])])

    def _format_value(self, value: str) -> Dict:
        return {"title": [{"text": {"content": value}}]}

    def contains(self, value): return {
        "property": self.name, self.type: {"contains": value}}

    def does_not_contain(self, value): return {
        "property": self.name, self.type: {"does_not_contain": value}}

    def starts_with(self, value): return {
        "property": self.name, self.type: {"starts_with": value}}
    def ends_with(self, value): return {
        "property": self.name, self.type: {"ends_with": value}}


@dataclass
class RichTextProperty(NotionProperty):
    def __init__(self, name: str):
        super().__init__(name=name, type="rich_text")

    def _parse_value(self, data: Dict) -> str:
        return "".join([t["plain_text"] for t in data.get("rich_text", [])])

    def _format_value(self, value: str) -> Dict:
        return {"rich_text": [{"text": {"content": value}}]}

    def contains(self, value): return {
        "property": self.name, self.type: {"contains": value}}

    def does_not_contain(self, value): return {
        "property": self.name, self.type: {"does_not_contain": value}}

    def starts_with(self, value): return {
        "property": self.name, self.type: {"starts_with": value}}
    def ends_with(self, value): return {
        "property": self.name, self.type: {"ends_with": value}}


@dataclass
class NumberProperty(NotionProperty):
    def __init__(self, name: str):
        super().__init__(name=name, type="number")

    def _parse_value(self, data: Dict) -> Optional[float]:
        return data.get("number")

    def _format_value(self, value: float) -> Dict:
        return {"number": value}

    def greater_than(self, value): return {
        "property": self.name, self.type: {"greater_than": value}}

    def less_than(self, value): return {
        "property": self.name, self.type: {"less_than": value}}

    def greater_than_or_equal_to(self, value): return {
        "property": self.name, self.type: {"greater_than_or_equal_to": value}}
    def less_than_or_equal_to(self, value): return {
        "property": self.name, self.type: {"less_than_or_equal_to": value}}


@dataclass
class CheckboxProperty(NotionProperty):
    def __init__(self, name: str):
        super().__init__(name=name, type="checkbox")

    def _parse_value(self, data: Dict) -> Optional[bool]:
        return data.get("checkbox")

    def _format_value(self, value: bool) -> Dict:
        return {"checkbox": value}

    def equals(self, value: bool): return {
        "property": self.name, self.type: {"equals": value}}


@dataclass
class SelectProperty(NotionProperty):
    def __init__(self, name: str):
        super().__init__(name=name, type="select")

    def _parse_value(self, data: Dict) -> Optional[str]:
        select = data.get("select")
        return select["name"] if select else None

    def _format_value(self, value: str) -> Dict:
        return {"select": {"name": value}}

# revisado inicio 
@dataclass
class MultiSelectProperty(NotionProperty):
    
    def __init__(self, name: str, options: Optional[List[OptionProperty]] = None):
        super().__init__(name=name, type="multi_select")
        self.options: List[OptionProperty] = field(default_factory=list)

    def contains(self, value): return {
        "property": self.name, self.type: {"contains": value}}
    def does_not_contain(self, value): return {
        "property": self.name, self.type: {"does_not_contain": value}}

# revisado fim 

@dataclass
class DateProperty(NotionProperty):
    def __init__(self, name: str):
        super().__init__(name=name, type="date")

    def _parse_value(self, data: Dict) -> Optional[datetime]:
        date_data = data.get("date")
        if not date_data:
            return None
        return datetime.fromisoformat(date_data["start"])

    def _format_value(self, value: datetime) -> Dict:
        return {"date": {"start": value.isoformat()}}

    def before(self, value): return {
        "property": self.name, self.type: {"before": value}}

    def after(self, value): return {
        "property": self.name, self.type: {"after": value}}

    def on_or_before(self, value): return {
        "property": self.name, self.type: {"on_or_before": value}}

    def on_or_after(self, value): return {
        "property": self.name, self.type: {"on_or_after": value}}

    def past_week(self): return {
        "property": self.name, self.type: {"past_week": {}}}

    def past_month(self): return {
        "property": self.name, self.type: {"past_month": {}}}

    def past_year(self): return {
        "property": self.name, self.type: {"past_year": {}}}

    def this_week(self): return {
        "property": self.name, self.type: {"this_week": {}}}

    def next_week(self): return {
        "property": self.name, self.type: {"next_week": {}}}

    def this_month(self): return {
        "property": self.name, self.type: {"this_month": {}}}

    def next_month(self): return {
        "property": self.name, self.type: {"next_month": {}}}

    def this_year(self): return {
        "property": self.name, self.type: {"this_year": {}}}
    def next_year(self): return {
        "property": self.name, self.type: {"next_year": {}}}


@dataclass
class PeopleProperty(NotionProperty):
    def __init__(self, name: str):
        super().__init__(name=name, type="people")

    def contains(self, value): return {
        "property": self.name, self.type: {"contains": value}}
    def does_not_contain(self, value): return {
        "property": self.name, self.type: {"does_not_contain": value}}


@dataclass
class FilesProperty(NotionProperty):
    def __init__(self, name: str):
        super().__init__(name=name, type="files")
    # Apenas is_empty e is_not_empty (herdado)


@dataclass
class RelationProperty(NotionProperty):
    def __init__(self, name: str):
        super().__init__(name=name, type="relation")

    def contains(self, value): return {
        "property": self.name, self.type: {"contains": value}}
    def does_not_contain(self, value): return {
        "property": self.name, self.type: {"does_not_contain": value}}


@dataclass
class FormulaProperty(NotionProperty):
    def __init__(self, name: str):
        super().__init__(name=name, type="formula")
    # Filtros para formula são aninhados por tipo:

    def string_contains(self, value): return {
        "property": self.name, self.type: {"string": {"contains": value}}}

    def string_starts_with(self, value): return {
        "property": self.name, self.type: {"string": {"starts_with": value}}}

    def string_ends_with(self, value): return {
        "property": self.name, self.type: {"string": {"ends_with": value}}}

    def number_equals(self, value): return {
        "property": self.name, self.type: {"number": {"equals": value}}}

    def number_greater_than(self, value): return {
        "property": self.name, self.type: {"number": {"greater_than": value}}}

    def number_less_than(self, value): return {
        "property": self.name, self.type: {"number": {"less_than": value}}}

    def checkbox_equals(self, value): return {
        "property": self.name, self.type: {"checkbox": {"equals": value}}}

    def date_before(self, value): return {
        "property": self.name, self.type: {"date": {"before": value}}}

    def date_after(self, value): return {
        "property": self.name, self.type: {"date": {"after": value}}}


#feito por mim 
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
}


def get_property_class(property_type: str) -> Optional[type]:
    """Retorna a classe correspondente ao tipo de propriedade do Notion."""
    return PROPERTY_TYPE_MAP.get(property_type, NotionProperty)