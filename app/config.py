import os

db_host = os.environ.get('DB_HOST', default='localhost')
db_name = os.environ.get('DB_NAME', default='garagesale')
db_user = os.environ.get('DB_USERNAME', default='yukarim')
db_password = os.environ.get('DB_PASSWORD', default='')
db_port = os.environ.get('DB_PORT', default='5432')

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = f"postgres://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
# SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
# postgres://xzredxgrtfcbxi:1e7fd7655b720dc2af2a118e7fcab3b3e43ebe015edc7a08705300d9dfd88497@ec2-3-211-245-154.compute-1.amazonaws.com:5432/dc2pjbqe16jaj3