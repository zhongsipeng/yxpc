from pathlib import Path
from datetime import datetime

class Config(object):
    BASE_PATH = Path.cwd()
    INSTANCE_PATH = BASE_PATH / Path('instance')
    FILE_PATH = BASE_PATH / Path('file')
    UPLOAD_FOLDER = FILE_PATH / 'uploads'
    TEMP_FOLDER = FILE_PATH / 'temp'
    DATE_TEMP_FOLDER = TEMP_FOLDER / Path(f'{datetime.now().strftime("%Y/%m/%d")}')
    TEMPLATE_FOLDER = FILE_PATH / 'template'
    
    
    INSTANCE_PATH.mkdir(exist_ok=True, mode=0o750)
    FILE_PATH.mkdir(exist_ok=True)
    UPLOAD_FOLDER.mkdir(exist_ok=True)
    TEMP_FOLDER.mkdir(exist_ok=True)
    TEMPLATE_FOLDER.mkdir(exist_ok=True)
    DATE_TEMP_FOLDER.mkdir(parents=True, exist_ok=True)
config = Config()
class ProductionConfig(Config):
    DATABASE_URI = 'mysql://[email protected]/foo'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
