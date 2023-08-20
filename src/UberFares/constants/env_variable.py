from dotenv import find_dotenv,load_dotenv
import os
from dataclasses import dataclass
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

@dataclass
class EnvironmentVariable:
    mongo_url = os.getenv('MONGO_DB_URL')