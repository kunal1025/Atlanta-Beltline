import os, pymysql, sys
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

_connection = None

def get_connection():
    global _connection
    try:
        if not _connection:
            _connection = pymysql.connect(host=os.getenv('HOST'),
                                            user=os.getenv('USERNAME'),
                                            password=os.getenv('PASSWORD'),
                                            db=os.getenv('DB'),
                                            charset='utf8mb4',
                                            cursorclass=pymysql.cursors.DictCursor)
    except Exception as e:
            print(e)
            sys.exit(0)
    return _connection

# List of stuff accessible to importers of this module. Just in case
__all__ = [ 'getConnection' ]