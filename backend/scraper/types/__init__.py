from ariadne import load_schema_from_path
import os

scraper_type_schema = load_schema_from_path(
    os.path.join(os.getcwd(), "backend/scraper/types"))
