
def confirm(prompt=''):
    while (True):
        ans = input(prompt).upper().strip()
        if ans in ('', 'Y', 'YES'):
            return True
        elif ans in ('N', 'NO'):
            return False

