import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from app import create_app
from app.models import SaleItem, User
from test_data import SELLER_TOKEN, BUYER_TOKEN
class GarageSaleTestCase(unittest.TestCase):
    """
    python -m unittest discover -s .
    """
    def setup_db(app, database_path, db):
        app.config["SQLALCHEMY_DATABASE_URI"] = database_path
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.app = app
        db.init_app(app)
        db.create_all()

    def setUp(self) -> None:
        self.app = create_app()
        self.client = self.app.test_client
       
        self.seller_headers = [('Content-Type', 'application/json'),
                                ('Authorization', f'Bearer {SELLER_TOKEN}')]
        self.buyer_headers = [('Content-Type', 'application/json'),
                                ('Authorization', f'Bearer {BUYER_TOKEN}')]
        
    def tearDown(self) -> None:
        pass

    """ TEST: @app.route('/saleitems', methods=['GET']) """
    # def test_get_saleitems(self):
    #     res = self.client().get('/saleitems', headers=self.seller_headers)
    #     print(res)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(len(data['saleitems']), 12)
    #     self.assertEqual(data['total_saleitems'], 12)

    """ TEST: @app.route('/saleitems', methods=['GET']) """
    # def test_get_saleitems_401(self):
    #     res = self.client().get('/saleitems')
    #     print(res)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 401)

    """ TEST: @app.route('/saleitems/<int:item_id>', methods=['GET']) """
    # def test_get_saleitem(self):
    #     res = self.client().get('/saleitems/8', headers=self.seller_headers)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(data['item']['name'], 'Painting')
    #     self.assertEqual(len(data['buyers']), 1)

    """ TEST: @app.route('/saleitems/<int:item_id>', methods=['GET']) """
    # def test_get_saleitem_404(self):
    #     res = self.client().get('/saleitems/100', headers=self.seller_headers)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404) 

    """ TEST: @app.route('/users', methods=['GET']) """
    # def test_get_users(self):
    #     res = self.client().get('/users', headers=self.seller_headers)
    #     print(res)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(len(data['users']), 2)
    #     self.assertEqual(data['total_users'], 2)

    """ TEST: @app.route('/users', methods=['GET']) """
    # def test_get_users_401(self):
    #     res = self.client().get('/users')
    #     print(res)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 401)  

    """ TEST: @app.route('/users/<int:user_id>', methods=['GET']) """
    def test_get_user(self):
        res = self.client().get('/users/1', headers=self.seller_headers)
        print(res)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['items']), 0)
        self.assertEqual(data['user']['nickname'], 'yukapon') 

    """ TEST: @app.route('/users/<int:user_id>', methods=['GET']) """
    def test_get_user_404(self):
        res = self.client().get('/users/77', headers=self.seller_headers)
        print(res)
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
        self.assertGreater(len(data['saleitems']), 0)
        self.assertGreater(data['total_saleitems'], 0)

    """ TEST: @app.route('/saleitems/<int:item_id>', methods=['PATCH']) """
    def test_patch_saleitem(self):
        patch_data = {
            "price": "100"
        }
        res = self.client().patch('/saleitems/8', json=patch_data, headers=self.seller_headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['updated'], 8)

    """ TEST: @app.route('/saleitems/<int:item_id>', methods=['PATCH']) """
    def test_patch_saleitem_error(self):
        patch_data = {
            "price": "100"
        }
        res = self.client().patch('/saleitems/88', json=patch_data, headers=self.seller_headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    """ TEST: @app.route('/saleitems/<int:item_id>', methods=['DELETE']) """
    def test_delete_saleitem_error(self):
        res = self.client().delete('/saleitems/91', headers=self.seller_headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)        

    """ TEST: @app.route('/saleitems/<int:item_id>', methods=['DELETE']) """
    # def test_delete_saleitem(self):
    #     res = self.client().delete('/saleitems/11', headers=self.seller_headers)

    #     data = json.loads(res.data)
    #     self.assertEqual(res.status_code, 200)

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
        res = self.client().post('/users', json=post_data, headers=self.buyer_headers)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)

    """ TEST: @app.route('/users/<int:user_id>', methods=['PATCH']) """
    def test_patch_user(self):
        patch_data = {
            "nickname": "tester1+",
        }
        res = self.client().patch('/users/0', json=patch_data, headers=self.seller_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['user']['nickname'], 'tester1+')  

    """ TEST: @app.route('/users/<int:user_id>', methods=['PATCH']) """
    def test_patch_user_error(self):
        patch_data = {
            "nickname": "tester1+",
        }
        res = self.client().patch('/users/200', json=patch_data, headers=self.seller_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    """ TEST: @app.route('/users/<int:user_id>', methods=['DELETE']) """
    # def test_delete_user(self):
    #     res = self.client().delete('/users/2', headers=self.seller_headers)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data['success'], True)

    """ TEST: @app.route('/users/<int:user_id>', methods=['DELETE']) """
    def test_delete_user_error(self):
        res = self.client().delete('/users/92', headers=self.seller_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)


