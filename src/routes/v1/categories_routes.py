from flask import Blueprint, jsonify, request
from src.models.categories import Categories

categories_bp = Blueprint('categories_v1', __name__, url_prefix='/api/v1')

@categories_bp.route('/categories', methods=['GET'])
def get_categories():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=3, type=int)

    categories, total_categories = Categories.get_paginated(
        page=page, per_page=per_page
    )

    total_pages = (total_categories + per_page - 1) // per_page

    return jsonify({
        'data': [{
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'active': category.active
        } for category in categories],
        'meta': {
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'total_categories': total_categories,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
    }), 200
    
@categories_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category_by_id(category_id):
    category = Categories.get_by_id(category_id)

    if category:
        return jsonify({
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'active': category.active
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Category not found'
        }), 404
        
        
@categories_bp.route('/categories', methods=['POST'])
def post_categories():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    errors = {}

    if not name:
        errors['name'] = 'name is required'
    else:
        existing_category = Categories.get_by_name(name)
        if existing_category:
            errors['name'] = 'name must be unique'

    if errors:
        return jsonify({
            'success': False,
            'message': 'Errors in data validation',
            'validation-errors': errors
        }), 400  
        
    new_category = Categories(
        name=name,
        description=description
    )

    Categories.save(new_category)

    return jsonify({
        'id': new_category.id,
        'name': new_category.name,
        'description': new_category.description,
        'active': new_category.active
    }), 201
    
@categories_bp.route('/categories/<int:category_id>', methods=['PUT'])
def put_categories(category_id):
    category = Categories.get_by_id(category_id)

    if not category:
        return jsonify({
            'success': False,
            'message': 'Category not found'
        }), 404

    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    errors = {}

    if name is not None and category.name != name:
        existing_category = Categories.get_by_name(name)
    
        if existing_category:
            errors['name'] = 'name must be unique'
        
    if name is not None:
        category.name = name

    if description is not None:
        category.description = description

    if errors:
        return jsonify({
            'success': False,
            'message': 'Errors in data validation',
            'validation-errors': errors
        }), 400

    Categories.update(category)

    return jsonify({
        'id': category.id,
        'name': category.name,
        'description': category.description,
        'active': category.active
    })
        
        

