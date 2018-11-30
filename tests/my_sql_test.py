import pytest
import src.my_sql as my_sql

@pytest.mark.parametrize("db_name, expected_db_name",
                         [('abc', 'abc'),
                          # uppercase
                          ('ABC', 'abc'),
                          # mixed case
                          ('aBcdEf', 'abcdef'),
                          # consecutive leading, separating and trailing spaces
                          ('   abc   def  ', 'abc_def'),
                          # consecutive allowed characters
                          ('aaabccc', 'aaabccc'),
                          # consecutive not allowed leading characters
                          ('22abc', 'abc'),
                          # consecutive not allowed characters
                          ('abc22abc', 'abc_abc'),
                          # consecutive not allowed trailing characters
                          ('ab12345', 'ab_'),
                          # consecutive not allowed leading and trailing characters
                          ('234523aa--bb$^12^%$#', 'aa_bb_'),
                          # all chars are not allowed
                          ('$^#', 'budget'),
                          # db_name longer then 65 chars
                          ('a123456789012345678901234567890123456789012345678901234567890abcdef', 'a_abc'),
                          ])
def test_check_db_name(db_name, expected_db_name):
    default_value = 'budget'
    assert my_sql.check_db_name(db_name, default_value) == expected_db_name


@pytest.mark.parametrize("table_name, list_of_fields, expected_sql",
                         [('budget', ('`year`', '`comment`'), "INSERT INTO budget ( `year`, `comment` ) VALUES ( %s,%s );"),
                          ('budget_line', ('`name`', '`budget_id`'), "INSERT INTO budget_line ( `name`, `budget_id` ) VALUES ( %s,%s );")
                          ])
def test_insert_row( table_name, list_of_fields, expected_sql ):
    assert my_sql.insert_row( table_name, list_of_fields ) == expected_sql
