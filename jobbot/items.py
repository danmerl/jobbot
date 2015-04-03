from scrapy.item import Item, Field

class JobItem(Item):
    organization = Field()
    date = Field()
    title = Field()
    jobid = Field()
    description = Field()

