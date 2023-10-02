from typing import List
from fastapi import FastAPI
from cassandra.cqlengine.management import sync_table

from . import (
    db,
    config,
    models,
    schema,
    crud
)

app = FastAPI()

settings = config.get_setting()


session = None
@app.on_event("startup")
def on_startup():
    global session
    session = db.get_session()
    sync_table(models.Product)
    sync_table(models.ProducScrapeEvent)

@app.get("/")
def read_index():
    return {"hello": "world", "name": settings.name}


@app.get("/products", response_model=List[schema.ProductListSchema])
def product_list_view():
    return list(models.Product.objects.all())


@app.post("/events/scrape")
def events_scrape_create_view(data: schema.ProductListSchema):
    product, _ = crud.add_scrape_event(data.dict())
    return product


@app.get("/products/{asin}")
def products_detail_view(asin):
    data = dict(models.Product.objects.get(asin=asin))
    """
    events = list(models.ProducScrapeEvent.objects().filter(asin=asin).limit(5))
    events = [schema.ProductScrapeEventDetailSchema(**data) for data in events]
    data['events'] = events
    data['events_urls'] = f'/products/{asin}/events'  
    """
    return data

@app.get("/products/{asin}/events", response_model=List[schema.ProductScrapeEventDetailSchema])
def products_scrape_list_view(asin):
    return list(models.ProducScrapeEvent.objects().filter(asin=asin))

"""
>> uvicorn app.main:app --reload  
>> ngrok http 800
"""