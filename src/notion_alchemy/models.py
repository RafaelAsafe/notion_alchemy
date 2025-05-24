from typing import Dict
from notion_alchemy.notion import  NotionProperty, RichTextProperty

# refazendo
        # o campos de propriedades tem que ser transformados em propriedades Notion 
class NotionDatabaseModel():
    """Classe Notion para represtação de databases"""
 
    _database_id: str = None
    _properties: Dict[str, NotionProperty] = {}

    def __init__(self, page: Dict):
        self._database_id = page.get('id')         
    
    def _init_properties(self):
        """Inicializa as propriedades com base nas anotações da classe"""
        for prop_name, prop_type in self._properties.items():
            setattr(self, prop_name, prop_type)
    
    
    @classmethod
    def from_notion(cls, page: Dict) -> None:
        """Converte do formato Notion para o modelo"""
        instance = cls(page)
        instance._database_id = page.get('id')

        for prop_name,prop_values in page['properties'].items():
            prop_name_tratada = prop_name.strip().lower()
            prop_type = prop_values.get('type')
            if prop_name not in instance._properties:
                instance._properties[prop_name_tratada] = prop_type
        
        instance._init_properties()
        return instance
    

    

class NotionModel:
    """Base class for Notion models with hybrid approach"""
    
    _database_id: str = None
    _properties: Dict[str, NotionProperty] = {}
    
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self._init_properties()
        
        for name, value in kwargs.items():
            if name in self._properties:
                self._properties[name].value = value
    
    def _init_properties(self):
        """Initialize properties based on class annotations"""
        for name, prop_type in self.__annotations__.items():
            if name.startswith('_'):
                continue
            if hasattr(self.__class__, name) and isinstance(getattr(self.__class__, name), NotionProperty):
                self._properties[name] = getattr(self.__class__, name)
            else:
                # Default to text property if not specified
                self._properties[name] = RichTextProperty(name)
    
    @classmethod
    def from_notion(cls, page_data: Dict):
        """Create model instance from Notion API response"""
        instance = cls()
        instance.id = page_data['id']
        
        for prop_name, prop in instance._properties.items():
            if prop_name in page_data['properties']:
                prop.from_notion(page_data['properties'][prop_name])
        
        return instance
    
    def to_notion_properties(self) -> Dict:
        """Convert model to Notion API properties format"""
        return {
            name: prop.to_notion()
            for name, prop in self._properties.items()
            if prop.value is not None
        }
    
    def __getattr__(self, name):
        if name in self._properties:
            return self._properties[name].value
        raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{name}'")
    
    def __setattr__(self, name, value):
        if name.startswith('_') or name not in getattr(self, '_properties', {}):
            super().__setattr__(name, value)
        else:
            self._properties[name].value = value