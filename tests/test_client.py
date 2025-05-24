import os
from decouple import config
from src.notion_alchemy.client import NotionClient
from src.notion_alchemy.models import NotionDatabaseModel

API_KEY= config('NOTION_TOKEN')
PAGE_ID = config('PAGE_ID')
DATABASE_ID = config('DATABASE_ID')


def test_request_page():
    client = NotionClient(API_KEY)
    resultado = client.get_page(PAGE_ID)
    assert resultado is not None


def test_query_database():
    client = NotionClient(API_KEY)
    pagina = client.get_database(DATABASE_ID)
    database = NotionDatabaseModel.from_notion(page=pagina)
    resultado = client.query_database(database)
    assert resultado is not None