import string


def check_db_name(db_name, default_value):
    """
    check db name, that should contain only lowercase letters a-z, be shorter then 65 characters, and all
     (consecutive) not allowed characters should be substituted with replacing character
    """
    # allowed characters a-z
    pattern = string.ascii_lowercase
    index = 0
    # change case to lowercase
    db_name = db_name.lower().strip()
    # first char must be letter, skip over
    while db_name[index] not in pattern:
        index += 1
        # if all chars are not in pattern
        if index == len(db_name):
            return default_value

    # skip leading not allowed characters and take 64 characters only
    db_name = db_name[index:index+64]

    replacing_character = '_'
    aux = []

    for char in db_name:
        # if needed, substitute not allowed character with replacing character
        if char not in pattern:
            char = replacing_character

        if len(aux) == 0:
            aux.append(char)
        elif aux[-1] != replacing_character:
            # if last char is not replacing character
            aux.append(char)
        elif char != replacing_character:
            aux.append(char)

    return ''.join(aux)


def select_db():
    return "SELECT schema_name FROM information_schema.SCHEMATA WHERE schema_name = %s;"


def create_db(db_name):
    return "CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET = 'utf8' DEFAULT COLLATE 'utf8_croatian_ci';".format(db_name)


def use_db(db_name):
    return "USE {};".format( db_name )


def select_table():
    return "SELECT table_name FROM information_schema.tables WHERE table_schema = %s AND table_name = %s;"


def create_table_budget(table_name):
    return "CREATE TABLE {} (`id` int( 11 ) NOT NULL AUTO_INCREMENT, " \
                            "`year` int( 4 ) NOT NULL UNIQUE, " \
                            "`comment` varchar( 512 ) COLLATE utf8_croatian_ci DEFAULT NULL," \
                            "PRIMARY KEY( `id`) " \
                            ") ENGINE = InnoDB DEFAULT CHARSET = utf8 COLLATE = utf8_croatian_ci".format( table_name )



def select_row(table_name, conditions):
    sql = "SELECT * FROM {} WHERE ".format( table_name)
    for condition in conditions:
        sql = sql + "{}=%s ".format(condition)
    sql = sql + ";"
    return sql


def insert_row(table_name, list_of_fields):
    sql = "INSERT INTO {}".format(table_name)
    string_of_fields =", ".join(list_of_fields)
    sql = sql + " ( " + string_of_fields + " ) VALUES ( "
    list_of_values = []
    for i in range(len(list_of_fields)):
        list_of_values.append("%s")
    string_of_values = ",".join(list_of_values)
    sql = sql + string_of_values + " );"

    return sql