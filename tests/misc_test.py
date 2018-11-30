import pytest
import src.misc as misc


@pytest.mark.parametrize("answer, expected_answer",
                         [('', True),
                          ('   ', True),
                          ('yes', True),
                          ('Yes', True),
                          ('YES', True),
                          ('Y', True),
                          ('no', False),
                          ('No', False),
                          ('NO', False),
                          ('N', False)])
def test_confirm(monkeypatch, answer, expected_answer):
    monkeypatch.setattr('builtins.input', lambda x: answer)
    assert misc.confirm() == expected_answer