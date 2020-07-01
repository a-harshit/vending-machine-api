'''
    Define Routes for different modules
'''

from flask import Blueprint
from flask_restful import Api
from Modules.ProductsInfo.controller import Controller as ProductsInfo
from Modules.BuyProducts.controller import Controller as BuyProducts
from Modules.Admin.controller import Controller as Admin
from Modules.Cash.controller import Controller as Cash

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Routes
api.add_resource(ProductsInfo, '/products', endpoint='get_products', methods=['GET'])
api.add_resource(ProductsInfo, '/products', endpoint='update_product_stock', methods=['PUT'])
api.add_resource(BuyProducts, '/buy', endpoint='buy_product', methods=['POST', 'DELETE'])
api.add_resource(Cash, '/collect', endpoint='collect_cash', methods=['GET'])
api.add_resource(Admin, '/transactions', endpoint='get_transactions', methods=['GET'])
api.add_resource(Admin, '/user', endpoint='user', methods=['POST'])
