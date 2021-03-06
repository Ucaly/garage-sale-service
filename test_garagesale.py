import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app import create_app
from app.models import SaleItem, User, setup_db

unittest.TestLoader.sortTestMethodsUsing = None

class GarageSaleTestCase(unittest.TestCase):
    """
    python -m unittest discover -s .
    """
    def setUp(self) -> None:
        db_name = 'garagesale'
        db_user = os.environ.get('DB_USESRNAME')
        db_path = f'postgres://{db_user}:@localhost:5432/{db_name}'
        self.app = create_app({
            'SQLALCHEMY_TRACK_MODIFICATIONS': True,
            'SQLALCHEMY_DATABASE_URI': db_path
        })
        self.client = self.app.test_client
        self.database_name = db_name
        self.database_path = db_path
        setup_db(self.app, self.database_path)
        
        seller_token = os.environ.get('SELLER_TOKEN')
        buyer_token = os.environ.get('BUYER_TOKEN')
        self.seller_headers = [('Content-Type', 'application/json'),
                                ('Authorization', f'Bearer {seller_token}')]
        self.buyer_headers = [('Content-Type', 'application/json'),
                                ('Authorization', f'Bearer {buyer_token}')]    
        
    def tearDown(self) -> None:
        pass

    """ TEST: @app.route('/saleitems', methods=['GET']) """
    def test_get_saleitems(self):
        res = self.client().get('/saleitems')
        print(res)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['saleitems']), 7)
        self.assertEqual(data['total_saleitems'], 7)

    """ TEST: @app.route('/saleitems/<int:item_id>', methods=['GET']) """
    def test_get_saleitem(self):
        res = self.client().get('/saleitems/1', headers=self.buyer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['item']['name'], 'Small plates')
        self.assertEqual(len(data['buyers']),0)

    """ TEST: @app.route('/saleitems/<int:item_id>', methods=['GET']) """
    def test_get_saleitem_404(self):
        res = self.client().get('/saleitems/100', headers=self.buyer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404) 


    """ TEST: @app.route('/saleitems', methods=['POST']) """
    def test_post_saleitems(self):
        post_data = {
            "name": "Test item 1",
            "price": "200",
            "image": "https://picsum.photos/400/600",
            "description": "This is a test item and price is 200"
        }
        res = self.client().post('/saleitems', json=post_data, headers=self.seller_headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['saleitems']), 8)
        self.assertEqual(data['total_saleitems'], 8)

    """ TEST: @app.route('/saleitems/<int:item_id>', methods=['PATCH']) """
    def test_patch_saleitem(self):
        patch_data = {
            "price": "100"
        }
        res = self.client().patch('/saleitems/3', json=patch_data, headers=self.seller_headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['updated'], 3)

    """ TEST: @app.route('/saleitems/<int:item_id>', methods=['PATCH']) """
    def test_patch_saleitem_error(self):
        patch_data = {
            "price": "100"
        }
        res = self.client().patch('/saleitems/88', json=patch_data, headers=self.seller_headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    """ TEST: @app.route('/saleitems', methods=['POST']) """
    def test_post_saleitems_missing_data(self):
        post_data = {
            "name": "Test item 1",
            "image": "https://picsum.photos/400/600",
            "description": "This is a test item and price is 200"
        }
        res = self.client().post('/saleitems', json=post_data, headers=self.seller_headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)

    """ TEST:@app.route('/saleitems/<int:item_id>/buy', methods=['POST']) """
    def test_buy_item(self):
        post_data = {
            "user_id": 1,
        }
        res = self.client().post('/saleitems/2/buy', json=post_data, headers=self.buyer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['updated_saleitem_id'], 2)

    """ TEST:@app.route('/saleitems/<int:item_id>/buy', methods=['POST']) """
    def test_buy_item_missing_userid(self):
        post_data = {"item_id": 5}
        res = self.client().post('/saleitems/3/buy', json=post_data, headers=self.buyer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)

    """ TEST: @app.route('/users', methods=['GET']) """
    def test_get_users(self):
        res = self.client().get('/users', headers=self.seller_headers)
        print(res)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['users']), 3)
        self.assertEqual(data['total_users'], 3)

    """ TEST: @app.route('/saleitems/<int:item_id>', methods=['DELETE']) """
    def test_delete_saleitem_error(self):
        res = self.client().delete('/saleitems/91', headers=self.seller_headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)        

    """ TEST: @app.route('/saleitems/<int:item_id>', methods=['DELETE']) """
    def test_delete_saleitem(self):
        res = self.client().delete('/saleitems/7', headers=self.seller_headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    """ TEST: @app.route('/users', methods=['GET']) """
    def test_get_users_403(self):
        res = self.client().get('/users', headers=self.buyer_headers)
        print(res)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)  

    """ TEST: @app.route('/users/<int:user_id>', methods=['GET']) """
    def test_get_user(self):
        res = self.client().get('/users/2', headers=self.seller_headers)
        print(res)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['items']), 0)
        self.assertEqual(data['user']['name'], 'Aman') 

    """ TEST: @app.route('/users/<int:user_id>', methods=['GET']) """
    def test_get_user_404(self):
        res = self.client().get('/users/77', headers=self.seller_headers)
        print(res)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    """ TEST: @app.route('/users', methods=['POST']) """
    def test_post_users(self):
        post_data = {
            "name": "Test user 1",
            "nickname": "tester1",
            "email": "tester1@mail.com",
        }
        res = self.client().post('/users', json=post_data, headers=self.buyer_headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['user']['nickname'], 'tester1')

    """ TEST: @app.route('/users', methods=['POST']) """
    def test_post_users_missing_data(self):
        post_data = {
            "name": "Test user 1",
            "nickname": "tester1",
        }
        res = self.client().post('/users', json=post_data, headers=self.seller_headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)

    """ TEST: @app.route('/users/<int:user_id>', methods=['PATCH']) """
    def test_patch_user(self):
        patch_data = {
            "nickname": "tester1+",
        }
        res = self.client().patch('/users/2', json=patch_data, headers=self.seller_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated'], 2)  

    """ TEST: @app.route('/users/<int:user_id>', methods=['PATCH']) """
    def test_patch_user_error(self):
        patch_data = {
            "nickname": "tester1+",
        }
        res = self.client().patch('/users/200', json=patch_data, headers=self.seller_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    """ TEST: @app.route('/users/<int:user_id>', methods=['DELETE']) """
    def test_delete_user(self):
        res = self.client().delete('/users/3', headers=self.seller_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    """ TEST: @app.route('/users/<int:user_id>', methods=['DELETE']) """
    def test_delete_user_error(self):
        res = self.client().delete('/users/92', headers=self.seller_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
