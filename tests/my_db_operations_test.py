from _datetime import datetime
import pymysql
import pytest
from src.my_db import MyDB

YEAR = datetime.now().year
OTHER_YEAR = datetime.now().year + 2
DB_NAME = 'home_budget'
OTHER_DB_NAME = 'other_db'
TABLE_NAME = 'budget'
OTHER_TABLE_NAME = 'other_table'


@pytest.fixture(scope='module')
def my_connect_to_my_db(request):
    a = MyDB()
    a.connect_to_my_db( db = DB_NAME )
    print('\n---------Opening db connection')
    def my_close_my_db():
        a.close_connection_to_my_db( DB_NAME )
        print('\n--------Closing db connection')
    request.addfinalizer(my_close_my_db)
    return a

def test_table_already_exists_in_my_db(my_connect_to_my_db):
    """
    There is alredy defined table in database?
    """
    assert my_connect_to_my_db.check_if_table_already_exists_in_my_db( DB_NAME, TABLE_NAME ) == True


@pytest.mark.xfail(raises=Exception)
def test_table_does_not_already_exist_in_my_db(my_connect_to_my_db):
    """
    There is not alredy defined table in database?
    """
    rowcount = my_connect_to_my_db.check_if_table_already_exists_in_my_db( DB_NAME, OTHER_TABLE_NAME )


def test_row_already_exists_in_my_db(my_connect_to_my_db):
    """
    Is there alredy defined row for  table in database?
    """
    cursor = my_connect_to_my_db.check_if_row_already_exists_in_my_db( TABLE_NAME, ['year'], (YEAR,) )
    assert isinstance( cursor, pymysql.cursors.Cursor )


@pytest.mark.xfail( raises=pymysql.err.InternalError )
def test_row_does_not_already_exist_in_my_db(my_connect_to_my_db):
    cursor = my_connect_to_my_db.check_if_row_already_exists_in_my_db(TABLE_NAME, ['year'], (OTHER_YEAR,) )


