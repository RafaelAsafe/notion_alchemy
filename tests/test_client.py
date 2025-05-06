import os
from decouple import config
from src.notion_alchemy.client import NotionClient

API_KEY= config('NOTION_TOKEN')
PAGE_ID = config('PAGE_ID')


def test_request_page():
    client = NotionClient(API_KEY)
    resultado = client.get_page(PAGE_ID)
    assert resultado