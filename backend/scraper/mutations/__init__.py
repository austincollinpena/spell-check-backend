from ariadne import load_schema_from_path
from os import getcwd
from os.path import dirname, basename, isfile, join
import glob

modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

from backend.scraper.mutations import *

# Get all the typedefs
scraper_mutation_schema = load_schema_from_path(join(getcwd(), "backend/scraper/mutations"))
