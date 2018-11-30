from datetime import datetime
import logging
import src.my_sql as my_sql

module_logger = logging.getLogger('main.budget')

class Budget():
    __singleton = None
    __start_year = 2018
    __end_year = 2050

    def __new__(cls, *args, **kwargs):
        """
        Singleton: Just one instance of Budget is possible at a time
        """

        if not cls.__singleton:
            cls.__singleton = super().__new__(Budget)
        return cls.__singleton


    def __init__(self, id=1, year=datetime.now().year ,comment='Some text'):
        """
        Initialize main parameters
        """
        self.logger = logging.getLogger('main.budget.Budget')
        self.id = id

        try:
            self.year = int(year)
        except Exception:
            self.year = Budget.__start_year
            self.logger.warning('\n Can not be casted to int: {} --> {}'.format(repr(year), self.year))
        finally:
            if self.year not in range(Budget.__start_year, Budget.__end_year):
                self.year = Budget.__start_year
                self.logger.warning('\n Out of range: {} --> {}'.format(repr(year), self.year))

        self.comment = comment

    def get_id(self):
        return self.id


    @classmethod
    def create_table_budget( cls, my_db, table_name ):
        """Create new 'budget' table"""
        cls.my_db = my_db
        cls.table_name = table_name
        my_db.create_table( my_sql.create_table_budget(cls.table_name) )




if __name__ == '__main__':
    pass

