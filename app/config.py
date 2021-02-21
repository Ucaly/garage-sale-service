import os

db_host = os.environ.get('DB_HOST', default='localhost')
db_name = os.environ.get('DB_NAME', default='garagesale')
db_user = os.environ.get('DB_USERNAME', default='yukarim')
db_password = os.environ.get('DB_PASSWORD', default='')
db_port = os.environ.get('DB_PORT', default='5432')

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = f"postgres://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
# SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
# postgres://qtxxzogixqgzwi:943b318d5f3791e023f1d94feb3106c9f3d74326607b54f41e87ac986d72bf20@ec2-35-171-57-132.compute-1.amazonaws.com:5432/d1qsj0rc1oltoe