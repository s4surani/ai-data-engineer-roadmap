# data_utils/__init__.py

from .api_client import fetch_news, fetch_github_repos, fetch_weather
from .pipeline import process_large_csv, monitor_file
from .validators import schema_validate, type_checks, null_value_handling, duplicate_detection
# Import anything else you add in data_utils (e.g., decorators, transformers)

# Optionally, set __all__ for clean import *
__all__ = [
    "fetch_news", "fetch_github_repos", "fetch_weather",
    "process_large_csv", "monitor_file",
    "schema_validate", "type_checks", "null_value_handling", "duplicate_detection",
]
