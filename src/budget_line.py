import logging
from src.budget import Budget

module_logger = logging.getLogger('main.budget_line')

class Budget_line():
    name = ''
    id = 1

    def __init__(self, id = 1, budget_line_name='None', budget_id=None):
        self.id = id
        self.name = budget_line_name
        self.budget_id = budget_id
        self.logger = logging.getLogger( 'main.budget_line.Budget_line' )


    @property
    def get_id(self):
        return self.id


    @property
    def get_name(self):
        return self.name


    @classmethod
    def create_table_budget_line( cls, my_db, table_name ):
        """Create new 'budget_line' table"""
        cls.my_db = my_db
        cls.table_name = table_name

        cls.sql = "CREATE TABLE IF NOT EXISTS {} (`id` int(11) NOT NULL AUTO_INCREMENT," \
                  "  `name` varchar(512) NOT NULL, " \
                  "  `budget_id` int(11) NOT NULL," \
                  "  PRIMARY KEY (`id`)," \
                  "  KEY `budget_id`(`id`)" \
                  ") ENGINE = InnoDB DEFAULT CHARSET = utf8 COLLATE = utf8_croatian_ci".format( cls.table_name )

        my_db.create_table( cls.sql )

