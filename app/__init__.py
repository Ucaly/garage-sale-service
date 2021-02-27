import os
from flask import Flask, abort, json, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS
from .models import WaitingList, db, SaleItem, User
from .auth import AuthError, requires_auth

def create_app(test_config=None):
    app= Flask(__name__)
    app.config.from_mapping(SECRET_KEY=os.environ.get('SECRET_KEY', default='dev'))
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app)

    @app.after_request
    def after_request(response):
        origin = request.headers.get('Origin')
        response.headers.add('Access-Control-Allow-Headers',
        'Content-Type,Authorization,authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
        'GET, PATCH, POST, DELETE, OPTIONS'),
        # response.headers.add('Access-Control-Allow-Origin', origin),
        response.headers.add('Access-Control-Allow-Domain', '*')
        return response

    @app.route('/saleitems', methods=['GET'])
    # @requires_auth('get:saleitems')
    def get_saleitems():
        '''
        GET /saleitems
        All permissions
        '''
        try:
            saleitems = SaleItem.query.filter(SaleItem.status != 2).order_by(SaleItem.added_at)
            formatted_items = [item.format() for item in saleitems]
            return jsonify({
                'success': True,
                'saleitems': formatted_items,
                'total_saleitems': len(formatted_items)
            })
        except Exception as error:
            print(f'Exception {error}')
            abort(422)
    
    @app.route('/saleitems', methods=['POST'])
    @requires_auth('post:saleitems')
    def add_saleitem(payload):
        '''
        POST /saleitems
        Permission required: Seller
        '''
        body = request.get_json()
        name = body.get('name')
        price = body.get('price')
        image = body.get('image')
        description = body.get('description')
        
        if name is None or price is None or image is None:
            abort(400)
        try:
            new_item = SaleItem(
                name=name,
                price=price,
                image=image,
                description=description,
                status=0
            )
            new_item.insert()
            # saleitems = SaleItem.query.filter(SaleItem.status != 2).order_by(SaleItem.added_at)
            saleitems = SaleItem.query.all()
            formatted_items = [item.format() for item in saleitems]
            return jsonify({
                'success': True,
                'saleitems': formatted_items,
                'total_saleitems': len(saleitems)
            })
        except Exception as e:
            print('An exception occured: {}'.format(e))
            abort(422)

    @app.route('/saleitems/<int:item_id>', methods=['GET'])
    @requires_auth('get:saleitem')
    def get_item(payload, item_id):
        if item_id is None:
            abort(400)
        saleitem = SaleItem.query.filter(SaleItem.id == item_id).first_or_404()
        try:
            users = saleitem.users
            buyers = []
            if len(users) > 0:
                for user in users:
                    buyers.append({
                        'name': user.name,
                        'nickname': user.nickname,
                        'email': user.email,
                    })
            return jsonify({
                'success': True,
                'item': saleitem.format(),
                'buyers': buyers,
                'total_buyers': len(buyers)
            })
        except Exception as e:
            print(f'Exception occured: {e}')
            abort(422)
    
    @app.route('/saleitems/<int:item_id>', methods=['PATCH'])
    @requires_auth('patch:saleitem')
    def update_item(payload, item_id):
        if item_id is None:
            abort(404)
        body = request.get_json()
        updated_name = body.get('name')
        updated_price = body.get('price')
        updated_image = body.get('image')
        updated_description = body.get('description')
        updated_status = body.get('status')
        item_to_update = SaleItem.query.filter(SaleItem.id == item_id).first_or_404()
        if updated_name:
            item_to_update.name = updated_name
        if updated_price:
            item_to_update.price = updated_price
        if updated_image:
            item_to_update.image = updated_image
        if updated_description:
            item_to_update.description = updated_description
        if updated_status:
            item_to_update.status = updated_status
        try:
            item_to_update.update()
            return jsonify({
                'success': True,
                'updated': item_id
            })
        except Exception as e:
            print(f'Exception {e}')
            abort(422)
    
    @app.route('/saleitems/<int:item_id>', methods=['DELETE'])
    @requires_auth('delete:saleitem')
    def delete_item(payload, item_id):
        if item_id is None:
            abort(400)
        item_to_delete = SaleItem.query.filter(SaleItem.id == item_id).first_or_404()
        try:
            item_to_delete.delete()
            return jsonify({
                'success': True,
                'deleted': item_id
            })
        except Exception as e:
            print(f'Exception {e}')
            abort(422)
    
    @app.route('/saleitems/<int:item_id>/buy', methods=['POST'])
    @requires_auth('post:saleitem')
    def buy_item(payload, item_id):
        if item_id is None:
            abort(400)
        body = request.get_json()
        user_id = body.get('user_id')
        if user_id is None:
            abort(400)
        item_to_buy = SaleItem.query.filter(SaleItem.id == item_id).first_or_404()
        buyers = item_to_buy.users
        if len(buyers) > 0:
            for buyer in buyers:
                if buyer.id == user_id:
                    abort(422)
        try:
            new_buyer = WaitingList(item_id=item_id, user_id=user_id)
            new_buyer.insert()
            if (item_to_buy.status != 1):
                item_to_buy.status = 1
                item_to_buy.update()
            return jsonify({
                'success': True,
                'updated_saleitem_id':item_id
            })
        except Exception as e:
            print(f'Exception occured: {e}')
            abort(422)

    @app.route('/users', methods=['GET'])
    @requires_auth('get:users')
    def get_users(payload):
        try:
            users = User.query.all()
            formatted_users = [user.format() for user in users]
            return jsonify({
                'success': True,
                'users': formatted_users,
                'total_users': len(users)
            })
        except Exception as e:
            print(f'Exception {e}')
            abort(422)

    @app.route('/users', methods=['POST'])
    @requires_auth('post:users')
    def add_user(payload):
        body = request.get_json()
        name = body.get('name')
        nickname = body.get('nickname')
        email = body.get('email')

        if name is None or nickname is None or email is None:
            abort(400)
        existingUser = User.query.filter(User.email == email).first()
        if (existingUser):
            return jsonify({
                'success': True,
                'user': existingUser.format()
            })
        
        new_user = User(name=name, nickname=nickname, email=email)
        try:
            new_user.insert()
            addedUser = User.query.filter(User.email == email).first()
            return jsonify({
                'success': True,
                'user': addedUser.format()
            })
        except Exception as e:
            print(f'Exception {e}')
            abort(422)

    @app.route('/users/<int:user_id>', methods=['GET'])
    @requires_auth('get:user')
    def get_user(payload, user_id):
        if user_id is None:
            abort(400)
        
        user = User.query.filter(User.id == user_id).first_or_404()
        try:
            items = user.items
            bid_items = []
            if (len(items) > 0):
                for item in items:
                    bid_items.append({
                        'id': item.id,
                        'name': item.name,
                        'price': item.price
                    })
            return jsonify({
                'success': True,
                'user': user.format(),
                'items': bid_items
            })
        except Exception as e:
            print(f'Exceptioin {e}')
            abort(422)

    @app.route('/users/<int:user_id>', methods=['DELETE'])
    @requires_auth('delete:user')
    def delete_user(payload, user_id):
        if user_id is None:
            abort(400)
        user_to_delete = User.query.filter(User.id == user_id).first_or_404()

        try:
            user_to_delete.delete()
            return jsonify({
                'success': True,
                'deleted': user_id
            })
        except Exception as e:
            print(f'Exception {e}')
            abort(422)
    
    @app.route('/users/<int:user_id>', methods=['PATCH'])
    @requires_auth('patch:user')
    def update_user(payload, user_id):
        if user_id is None:
            abort(400)
        
        body = request.get_json()
        updated_name = body.get('name')
        updated_nickname = body.get('nickname')
        updated_email = body.get('email')
        
        user_to_update = User.query.filter(User.id == user_id).first_or_404()
        if updated_name:
            user_to_update.name = updated_name
        if updated_nickname:
            user_to_update.nickname = updated_nickname
        if updated_email:
            user_to_update.email = updated_email
        try:
            user_to_update.update()
            return jsonify({
                'success': True,
                'updated': user_id
            })
        except Exception as e:
            print(f'Exception {e}')
            abort(422)
        
    @app.route('/')
    def index():
        return 'WELCOME TO GARAGESALE'

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
        "success": False, 
        "error": 404,
        "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
        "success": False, 
        "error": 400,
        "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal error"
        }), 500
    
    return app
