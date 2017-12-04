from flask import session

def is_account_a_business(): 
    if 'account_type' in session and \
        session['account_type'] == 'business': 
        return True 
    else: 
        return False
