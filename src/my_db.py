import logging
import pymysql.cursors
import src.my_sql as my_sql
import src.misc as misc

module_logger = logging.getLogger('main.my_db')

class MyDB():

    connection = None

    def __init__(self):
        self.logger = logging.getLogger( 'main.my_db.MyDB' )


    def connect_to_my_db(self, host='localhost', user='budget', password='budget', db=None, cursorclass=pymysql.cursors.Cursor ):
        """
        Returns connection to database or raises an exception.
        """
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.cursorclass =  cursorclass
        try:
            self.connection = pymysql.connect(  host=self.host,
                                                user=self.user,
                                                password=self.password,
                                                db=self.db,
                                                cursorclass=self.cursorclass )

            self.logger.info( 'Connected to database {} ...'.format( self.db ))
            return self.connection
        except pymysql.err.InternalError:
            self.logger.exception('Unable to make a connection to the database {} ... Please provide database!'.format( self.db ))
        except pymysql.err.OperationalError:
            self.logger.exception('Unable to make a connection to the database {} ... Please provide your credentials!'.format( self.db ))
        except Exception:
            self.logger.exception('General error making connection to database {} ...'.format( self.db ))


    def close_connection_to_my_db(self, db_name):
        """
        Close connection to database.
        """
        self.db_name = db_name
        try:
            self.connection.close()
            self.logger.info( 'Closed connection to database {} ...'.format( self.db_name ) )
        except pymysql.err.InternalError:
            self.logger.exception('Unable to close connection to the database {} ... Please provide database!'.format( self.db_name ))
        except pymysql.err.OperationalError:
            self.logger.exception('Unable to close connection to the database {} ... Please provide your credentials!'.format( self.db_name ))
        except Exception:
            self.logger.exception('General error closing connection to database {} ...'.format( self.db_name ))


    def check_if_db_already_exists(self, db_name):
        """
        Is there alredy database created?
        """
        self.db_name = db_name

        try:
            with self.connection.cursor() as cursor:
                cursor.rowcount = 0
                cursor.execute(my_sql.select_db(), (self.db_name))
                return cursor.rowcount
        except Exception as e:
            self.logger.exception('Exception occurred: {}'.format(e))


    @classmethod
    def input_db_name(cls, default_value):
        cls.default = default_value
        while (True):
            cls.db_name = input( 'Database name [ {} ] : '.format(cls.default)).strip()
            if cls.db_name == '':
                return cls.default
            parsed_db_name = my_sql.check_db_name(cls.db_name, cls.default)
            if parsed_db_name != cls.db_name:
                print("Database name [ {} ] containes characters that are not allowed... "
                      "Those characters have been replaced with '_' ...".format(cls.db_name))
                if misc.confirm('Database name [ {} ] OK? [Yes]/No :'.format(parsed_db_name)):
                    return parsed_db_name
            else:
                return cls.db_name


    def check_if_table_already_exists_in_my_db(self, db_name, table_name):
        """
        Is there alredy table created?
        """
        self.db_name = db_name
        self.table_name = table_name
        try:
            with self.connection.cursor() as cursor:
                cursor.rowcount = 0
                cursor.execute( my_sql.select_table(), (self.db_name, self.table_name))
                return cursor.rowcount
        except Exception as e:
            self.logger.exception( 'Exception occurred: {}'.format( e ) )


    def check_if_row_already_exists_in_my_db(self, table_name, conditions, params):
        """
        Is there already defined row for given year?
        """
        self.table_name = table_name
        self.conditions = conditions
        self.params = params
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(my_sql.select_row(self.table_name, self.conditions), self.params)
                if cursor.rowcount:
                    return cursor
        except Exception as e:
            self.logger.exception( 'Exception occurred: {}'.format( e ) )


    def create_db(self, db_name):
        """Create new database"""
        self.db_name = db_name

        try:
            with self.connection.cursor() as cursor:
                cursor.execute( my_sql.create_db(db_name) )
                self.connection.commit()
        except Exception as e:
            self.logger.exception( 'Exception occurred: {}'.format( e ) )


    def use_db( self, db_name ):
        """Select database"""
        self.db_name = db_name
        try:
            with self.connection.cursor() as cursor:
                cursor.execute( my_sql.use_db(self.db_name) )
                self.connection.commit()
                self.logger.info( 'Selected database {} ...'.format( self.db_name ) )
        except Exception as e:
            self.logger.exception( 'Exception occurred: {}'.format( e ) )


    def create_table(self, sql):
        """Create new table"""

        self.sql = sql
        try:
            with self.connection.cursor() as cursor:
                cursor.execute( self.sql )
                self.connection.commit()
        except Exception as e:
            self.logger.exception( 'Exception occurred: {}'.format( e ) )


    def insert_new_row(self, table_name,  fields, params):
        """Insert new row in table """
        self.table_name = table_name
        self.fields = fields
        self.params = params
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                cursor.execute(my_sql.insert_row(self.table_name, self.fields), (self.params))
                self.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            self.logger.exception( 'Exception occurred: {}'.format( e ) )
