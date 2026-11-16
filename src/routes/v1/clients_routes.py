from flask import Blueprint, jsonify, request
from src.models.clients import Clients, DocumentType 
from src.utils.auth import token_required, role_required
from src.models.users import Role

clients_bp = Blueprint('clients_v1', __name__, url_prefix='/api/v1')

@clients_bp.route('/clients', methods=['GET'])
@token_required
@role_required(Role.ADMIN, Role.SELLER)
def get_clients():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=3, type=int)

    clients, total_clients = Clients.get_paginated(
        page=page, per_page=per_page
    )

    total_pages = (total_clients + per_page - 1) // per_page

    return jsonify({
        'data': [{
            'id': client.id,
            'name': client.name,
            'email': client.email,
            'phone': client.phone,
            'address': client.address,
            'active': client.active,
            'document_type': client.document_type.value,
            'document_number': client.document_number
        } for client in clients],
        'meta': {
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'total_clients': total_clients,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
    }), 200
    
@clients_bp.route('/clients/<int:client_id>', methods=['GET'])
@token_required
@role_required(Role.ADMIN, Role.SELLER)   
def get_client_by_id(client_id):
    client = Clients.get_by_id(client_id)

    if client:
        return jsonify({
            'id': client.id,
            'name': client.name,
            'email': client.email,
            'phone': client.phone,
            'address': client.address,
            'active': client.active,
            'document_type': client.document_type.value,
            'document_number': client.document_number
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Client not found'
        }), 404
        
@clients_bp.route('/clients', methods=['POST'])
@token_required
@role_required(Role.ADMIN)           
def create_client():
    data = request.get_json()
    
    errors = {}
    if not data.get('document_type'):
        errors['document_type'] = 'document_type is required'
        
    elif data.get('document_type') not in ['CC', 'NIT', 'CE']:
        errors['document_type'] = 'document_type must be one of: CC, NIT, CE'
        
    document_number = data.get('document_number')
        
    if not document_number:
        errors['document_number'] = 'document_number is required'
    
    else:
        existing_client = Clients.get_by_document_number(document_number)
        if existing_client:
            errors['document_number'] = 'document_number must be unique'    
       
    if not data.get('name'):
        errors['name'] = 'name is required'  
        
    email = data.get('email')
    if not email:
        errors['email'] = 'email is required'
        
    if email and '@' not in email:
        errors['email'] = 'email is not valid' 
        
    phone = data.get('phone')
    if not phone:
        errors['phone'] = 'phone is required'
        
    address = data.get('address')
    if not address:
        errors['address'] = 'address is required'

    if errors:
        return jsonify({
            'success': False, 
            'message': 'Errors in data validation',
            'validation-errors': errors
            }), 400

    client = Clients(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        address=data['address'],
        document_type=DocumentType(data['document_type']),
        document_number=data['document_number']
    )

    client.save()

    return jsonify({
        'id': client.id,
        'name': client.name,
        'email': client.email,
        'phone': client.phone,
        'address': client.address,
        'active': client.active,
        'document_type': client.document_type.value,
        'document_number': client.document_number
    }), 201
    
@clients_bp.route('/clients/<int:client_id>', methods=['PUT'])
@token_required
@role_required(Role.ADMIN)           
def update_client(client_id):
    client = Clients.get_by_id(client_id)

    if not client:
        return jsonify({
            'success': False,
            'message': 'Client not found'
        }), 404

    data = request.get_json()
    errors = {}
    
    if 'document_type' in data and data['document_type'] not in ['CC', 'NIT', 'CE']:
        errors['document_type'] = 'document_type must be one of: CC, NIT, CE'
        
    if 'document_number' in data:
        if not data['document_number']:
            errors['document_number'] = 'document_number is required'
        elif data['document_number'] != client.document_number:
            existing_client = Clients.get_by_document_number(data['document_number'])
            if existing_client:
                errors['document_number'] = 'document_number must be unique'
    
    if 'name' in data and not data['name']:
        errors['name'] = 'name is required'
        
    if 'email' in data:
        if not data['email']:
            errors['email'] = 'email is required'
        elif '@' not in data['email']:
            errors['email'] = 'email is not valid'
            
    if 'phone' in data and not data['phone']:
        errors['phone'] = 'phone is required'
        
    if 'address' in data and not data['address']:
        errors['address'] = 'address is required'
        
    active = data.get('active')

    if active is not None and (type(active) is not int or active not in [0, 1]):
        errors['active'] = 'active must be 0 or 1'
    
    if errors:
        return jsonify({
        'success': False,
        'message': 'Errors in data validation',
        'validation-errors': errors
        }), 400      
    
    client.name = data.get('name', client.name)
    client.email = data.get('email', client.email)
    client.phone = data.get('phone', client.phone)
    client.address = data.get('address', client.address)
    client.active = data.get('active', client.active)
    client.document_type = DocumentType(data.get('document_type', client.document_type.value))
    client.document_number = data.get('document_number', client.document_number)

    client.update()

    return jsonify({
        'id': client.id,
        'name': client.name,
        'email': client.email,
        'phone': client.phone,
        'address': client.address,
        'active': client.active,
        'document_type': client.document_type.value,
        'document_number': client.document_number
    }), 200

