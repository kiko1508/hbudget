import pytest
from src.budget import Budget


def test_budget_year_there_is_no_parameters():
    a = Budget()
    assert a.year == 2018
    del a


def test_budget_there_is_just_first_named_parameter():
    a = Budget(year = 2018)
    assert a.year == 2018
    del a


def test_budget_year_there_is_just_other_named_parameter_given( ):
    a = Budget(comment='Some text')
    assert a.year == 2018
    del a


@pytest.mark.parametrize("year", [
    0,
    2016,
    2018,
    2060,
    -2018,
    '2018',
    '-2018',
    'abc',
    20.18,
    -20.18,
    [2016],
    ['2018'],
    [2020],
    (2018,),
    ('2018',),
    {'year': 2016},
    {'year': 2018},
    {'year': '2018'}
])
def test_budget_year_may_be_not_an_integer_out_of_range(year):
    a = Budget(year)
    assert a.year == 2018
    del a


