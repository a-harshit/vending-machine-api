'''
    Module to manage products for the vending machine
'''

from json import loads, dumps
from flask_restful import Resource
from flask_responses import json_response
from flask import request

from Modules.ProductsInfo.model import Model

class Controller(Resource):
    '''
        Class to fetch and update products for the vending machine
    '''

    def __init__(self):
        self._model = Model()

    def get(self):
        '''
            Method to return all the products
        '''
        try:
            success, product_list = self._model.get_products()
            if not success:
                return json_response({'success': False, 'data': [], 'msg': 'Something went wrong'})

            return json_response({'success': True, 'data': product_list})
        except ValueError as error:
            print(str(error))
            return json_response({'success': False, 'data': [], 'msg': 'Can not fetch the products'})

    def put(self):
        '''
            Method to update stock of the product
        '''
        try:
            auth = request.headers.get('Authorisation')
            if not auth or auth != 'dGVzdDphZG1pbg==':
                return json_response({'success': False, 'data': [], 'msg': 'Not authorised to access this resource.'})

            product_dict = loads(request.data)

            product_id = product_dict.get('product_id', None)
            product_quantity = product_dict.get('product_quantity', None)

            if not product_id or not product_quantity:
                return json_response({'success': False, 'msg': 'Product ID or quantity is not valid'})
            
            product_exist = self._model.check_product_exist(product_id)

            if not product_exist:
                return json_response({'success': False, 'msg': 'Product does not exist'})

            success = self._model.update_product_stock(product_dict)
            if not success:
                return json_response({'success': False, 'msg': 'Error Occured. Can not update the quantity.'})
            
            return json_response({'success': True, 'data': product_dict})
        except ValueError as error:
            print(str(error))
            return json_response({'success': False, 'msg': 'Something went wrong'})
