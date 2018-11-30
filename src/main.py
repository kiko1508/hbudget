import logging
from tkinter import *
from src.budget import Budget
from src.budget_line import Budget_line
import src.create_logger as logger
from src.my_db import MyDB
import src.my_sql as my_sql
import src.ini_file as ini
import src.misc as misc


if __name__ == '__main__':

    # create logger with 'application'
    DEFAULT_LOGGER_FILE = 'budget.log'
    DEFAULT_INI_FILE = 'budget.ini'

    logger = logger.create_logger(DEFAULT_LOGGER_FILE)
    logger.info('Application started ...')

    my_window = Tk()

    # check if .ini file exists, if not, create one
    if not ini.is_there_ini_file(DEFAULT_INI_FILE):
        ini.create_ini_file(DEFAULT_INI_FILE)
        logger.info('Application initialisation file created ...')

    db_name = ini.read_ini_file(DEFAULT_INI_FILE)
    logger.info('Budget application initialisation finished ...')

    year = 2018
    comment = 'new budget'

    logger.info('Preparing to create instance of Budget ...')

    # connect to database
    my_db = MyDB()
    my_db.connect_to_my_db( None )

    #check if database already exists
    if not my_db.check_if_db_already_exists( db_name ):
        logger.warning('There is no database {} ...'.format(db_name))
        #if database does not exist, create one?
        if misc.confirm('Create NEW database? [Yes]/No :'):
            # if 'yes' type in database name
            db_name = MyDB.input_db_name(db_name)
            logger.info('Creating database {} ...'.format(db_name))
            #create database
            my_db.create_db(db_name)
        else:
            exit()
    else:
        logger.warning('There is already database {} ...'.format(db_name))

    # use database
    my_db.use_db(db_name)

    # table 'budget'

    table_name = 'budget'
    id = 1
    if not my_db.check_if_table_already_exists_in_my_db( db_name, table_name):
        logger.warning('There is no table {} in the database {} ...'.format( table_name, db_name))
        logger.info( 'Creating table {} ...'.format( table_name))
        Budget.create_table_budget( my_db, table_name)
        id = my_db.insert_new_row( table_name, ['year', 'comment'], (year, comment))
        logger.info( 'New row with id = {} added in table {} ...'.format( id, table_name))
        budget = Budget(id, year, comment)
    else:
        logger.info('There is already table {} in database {} ...'.format( table_name, db_name))
        cursor = my_db.check_if_row_already_exists_in_my_db( table_name, ['year'], (year,))
        if cursor:
            logger.warning('There is already row in table {} for year {} ...'.format( table_name, year))
            row = cursor.fetchone()
            id, year, comment = row
            budget = Budget(id, year, comment)
        else:
            logger.warning('There is no row in table {} for year {} ...'.format(table_name, year))
            id = my_db.insert_new_row( table_name, ['year', 'comment'], (year, comment))
            budget = Budget(id, year, comment)

    logger.info('Instance of Budget with id = {} created ...'.format( budget.id))


# table 'budget_line'

    table_name = 'budget_line'
    name = 'New budget line'

    budget_line = []

    if not my_db.check_if_table_already_exists_in_my_db( db_name, table_name ):
        logger.warning( 'There is no table {} in the database {} ...'.format( table_name, db_name ) )
        logger.info( 'Creating table {} ...'.format( table_name ) )
        Budget_line.create_table_budget_line( my_db, table_name )
        id = my_db.insert_new_row( table_name, ['name', 'budget_id'], (name, budget.get_id()) )
        logger.info( 'New row with id = {} added in table {} ...'.format( id, table_name ) )
        budget_line.append(Budget_line( id, name, budget.get_id() ))
        logger.info('Instance of Budget_line with id = {} and name = {} ...'.format( id, name ) )
    else:
        logger.info( 'There is already table {} in database {} ...'.format( table_name, db_name ) )
        cursor = my_db.check_if_row_already_exists_in_my_db( table_name, [id], (id,) )
        if cursor:
            logger.warning( 'There is already row in table {} for name {} ...'.format( table_name, name ) )
            rows = cursor.fetchall()
            for row in rows:
                id, name, budget_id = row
                budget_line.append(Budget_line(id, name, budget_id))
                logger.info( 'Instance of Budget_line with id = {} and name = {} ...'.format( id, name ) )
        else:
            logger.warning( 'There is no row in table {} for Budget for year {} ...'.format( table_name, budget.year ) )
            id = my_db.insert_new_row( table_name, ['name', 'budget_id'], (name, budget.get_id()) )
            budget_line.append(Budget_line( id, name, budget.get_id() ))
            logger.info('Instance of Budget_line with id = {} and name = {} ...'.format( id, name ) )


    my_db.close_connection_to_my_db( db_name )
    logger.info('Application finished!')
    logger.debug( '{}'.format('-'*80) )

    my_window.mainloop()