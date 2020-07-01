'''
    Module to handle admin based operations
'''

from json import loads, dumps
from flask_restful import Resource
from flask_responses import json_response
from flask import request

from Modules.Admin.model import Model

class Controller(Resource):
    '''
        Class to handle admin based operations
    '''

    def __init__(self):
        self._model = Model()

    def get(self):
        '''
            Method to return the transaction history
        '''
        try:
            auth = request.headers.get('Authorisation')
            if not auth or auth != 'dGVzdDphZG1pbg==':
                return json_response({'success': False, 'data': [], 'msg': 'Not authorised to access this resource.'})

            success, transactions = self._model.get_transactions()

            if not success:
                return json_response({'success': False, 'data': [], 'msg': 'Something went wrong'})
            
            return json_response({'success': True, 'data': transactions})
        except ValueError as error:
            print(str(error))
            return json_response({'success': False, 'msg': 'Something went wrong'})
    
    def post(self):
        '''
            Method to return the transaction history
        '''
        try:
            data = loads(request.data)
            if data['password'] == 'admin':
                return json_response({'success': True, 'data': []})
            else:
                return json_response({'success': False, 'msg': 'Wrong password entered'})
        except ValueError as error:
            print(str(error))
            return json_response({'success': False, 'msg': 'Something went wrong'})
