from .queries import scraper_query_schema
from .types import scraper_type_schema
from .mutations import scraper_mutation_schema
from .subscriptions import scraper_subscription_schema

scraper_type_defs = [scraper_query_schema, scraper_type_schema, scraper_mutation_schema, scraper_subscription_schema]
