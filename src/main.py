from decouple import config

from notion_alchemy.client import NotionClient
from notion_alchemy.models import NotionDatabaseModel
from notion_alchemy.notion import NotionProperty

page_id = config('PAGE_ID')

NotionClient = NotionClient(config('NOTION_TOKEN'))

pagina = NotionClient.get_page(page_id)

model = NotionDatabaseModel.from_notion(page=pagina)