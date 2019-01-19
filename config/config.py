from utils.coll import Config
#from sqlalchemy import create_engine

DB_PASSWORD = Config.get('DB.password')
DB_HOST = Config.get('DB.host')
"""
engine = create_engine(
    'mysql+pymysql://root:{}@{}/bico'.format(DB_PASSWORD, DB_HOST),
    echo=True
)
"""
