from utils.coll import Config

login = Config.get('AUTH.login')
password = Config.get('AUTH.password')
DATA_PARAM = "login={}&password={}&submit=%D0%92%D0%BE%D0%B9%D1%82%D0%B8".format(login, password)

"""
engine = create_engine(
    'mysql+pymysql://root:{}@{}/bico'.format(DB_PASSWORD, DB_HOST),
    echo=True
)
"""
