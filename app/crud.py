import copy
import uuid

from .models import Product, ProducScrapeEvent

def create_entry(data:dict):
    return Product.create(**data) # unpack the data

def create_scrape_entry(data:dict):
    data['uuid'] = uuid.uuid1()
    return ProducScrapeEvent.create(**data)

def add_scrape_event(data:dict, fresh=False):
    if fresh:
        data = copy.deepcopy(data)
    product = create_entry(data)
    scrape_obj = create_scrape_entry(data)
    return product, scrape_obj 


"""
cd -> pythont
>> from app.crud import create_entry
>> data = {
    "asin": "14545657567",
    "title": "hello world"
}

>> from app.crud import create_entry, Product
>> list(Product.objects().all())

>> from app import crud, models
>> ProducScrapeEvent = models.ProducScrapeEvent
>> data = models.data
>> crud.create_scrape_entry(data)
>>> for i in producScrape.objects.all():
...     print(i.uuid)

"""