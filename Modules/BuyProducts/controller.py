'''
    Module to buy products for the vending machine
'''

from json import loads, dumps
from flask_restful import Resource
from flask_responses import json_response
from flask import request, session

from Modules.BuyProducts.model import Model

from Utils.helper import check_currency

class Controller(Resource):
    '''
        Class to buy products from the vending machine
    '''

    def __init__(self):
        self._model = Model()

    def post(self):
        '''
            Method to buy the product from the vending machine
        '''
        try:
            product_dict = loads(request.data)

            product_id = product_dict.get('product_id', None)
            product_price = product_dict.get('product_price', None)
            note = product_dict.get('note', None)
            
            if not product_id or not note or not product_price:
                return json_response({'success': False, 'final_buy': False, 'msg': 'One or more parameters are invalid/missing'})

            if not check_currency(note):
                return json_response({'success': False, 'final_buy': False, 'msg': 'Invalid note passed'})

            note_amt = int(note) + session.get('note_amt', 0)

            if int(note_amt) >= int(product_price):
                if 'note_amt' in session:
                    session.pop('note_amt', None)
                product_exist, price = self._model.check_product_exist(product_id)
                if not product_exist:
                    return json_response({'success': False, 'final_buy': True, 'msg': 'Invalid buy request. Product does not exist.'})
                
                if price <= product_price:
                    result = self._model.buy_product(product_id, price)
                    if not result:
                        return json_response({'success': False, 'final_buy': True, 'msg': 'Request can not be fulfilled. Try again later.'})

                balance_amt = abs(int(price) - int(note_amt))
                data = {
                    'product_id': product_id,
                    'product_price': price,
                    'balance': balance_amt
                }
                return json_response({'success': True, 'data': data, 'final_buy': True})

            else:
                if 'note_amt' in session:
                    session['note_amt'] = int(session.get('note_amt')) + int(note)
                else:
                    session['note_amt'] = int(note)

                amount_to_add = int(product_price) - (session.get('note_amt'))
                data = {
                    'product_id': product_id,
                    'product_price': product_price,
                    'add_amount': amount_to_add
                }
                return json_response({'success': True, 'data': data, 'final_buy': False})

        except ValueError as error:
            print(str(error))
            return json_response({'success': False, 'data': [], 'msg': 'Can not fetch the products'})


    def delete(self):
        '''
            Method to clear current session
        '''
        try:
            if 'note_amt' in session:
                session.pop('note_amt', None)
            return json_response({'success': True})
        except ValueError as error:
            print(str(error))
            return json_response({'success': False, 'msg': 'Something went wrong'})
