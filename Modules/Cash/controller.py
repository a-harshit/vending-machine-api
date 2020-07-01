'''
    Module to handle collection of cash
'''

from json import loads, dumps
from flask_restful import Resource
from flask_responses import json_response
from flask import request

from Modules.Cash.model import Model

class Controller(Resource):
    '''
        Class to handle collection of cash
    '''

    def __init__(self):
        self._model = Model()

    def get(self):
        '''
            Method to return available cash to the admin
        '''
        try:
            auth = request.headers.get('Authorisation')
            if not auth or auth != 'dGVzdDphZG1pbg==':
                return json_response({'success': False, 'data': [], 'msg': 'Not authorised to access this resource.'})

            success, collect_cash = self._model.collect_cash()
            if not success:
                return json_response({'success': False, 'data': [], 'msg': 'Can not get the money. Try again later.'})
            data = {
                'amount': int(collect_cash) if collect_cash is not None else 0
            }
            return json_response({'success': True, 'data': data})
        except ValueError as error:
            print(str(error))
            return json_response({'success': False, 'data': [], 'msg': 'Something went wrong'})
