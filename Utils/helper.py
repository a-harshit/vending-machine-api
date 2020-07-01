'''
    Contains helper methods used in different modules
'''

def check_currency(note):
    acceptable_notes = [10, 20, 50, 100]
    return note in acceptable_notes