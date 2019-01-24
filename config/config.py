from utils.coll import Config
import os

login = Config.get('AUTH.login')
password = Config.get('AUTH.password')
DATA_PARAM = "login={}&password={}&submit=%D0%92%D0%BE%D0%B9%D1%82%D0%B8".format(login, password)

project_folder = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

"""
engine = create_engine(
    'mysql+pymysql://root:{}@{}/bico'.format(DB_PASSWORD, DB_HOST),
    echo=True
)
"""
