from flask import Blueprint, jsonify, request, g
from src.models.invoices import Invoices
from src.models.clients import Clients
from src.models.users import Users, Role 
from src.utils.auth import token_required, role_required

invoices_bp = Blueprint('invoices_v1', __name__, url_prefix='/api/v1')

@invoices_bp.route('/invoices', methods=['GET'])
@token_required
@role_required(Role.ADMIN, Role.SELLER)
def get_invoices():
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=3, type=int)
    
    invoices, total_invoices = Invoices.get_paginated(
        page=page, per_page=per_page
    )
    
    total_pages = (total_invoices + per_page - 1) // per_page
    
    return jsonify({
        'data': [{
            'id': invoice.id,
            'client_id': invoice.client_id,
            'user_id': invoice.user_id,
            'date': invoice.date.isoformat(),
            'total': invoice.total,
            'completed': invoice.completed,
            'active': invoice.active
        } for invoice in invoices],
        'meta': {
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'total_invoices': total_invoices,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
    }), 200

@invoices_bp.route('/invoices/<int:invoice_id>', methods=['GET'])
@token_required
@role_required(Role.ADMIN, Role.SELLER)
def get_invoice_by_id(invoice_id):
    invoice = Invoices.get_by_id(invoice_id)

    if invoice:
       return jsonify({
           'id': invoice.id,
           'client_id': invoice.client_id,
           'user_id': invoice.user_id,
           'date': invoice.date.isoformat(),
           'total': invoice.total,
           'completed': invoice.completed,
           'active': invoice.active
        })
    else:
        return jsonify({
            'error': 'Invoice not found'
        }), 404
        
@invoices_bp.route('/invoices/client/<int:client_id>', methods=['GET'])
@token_required
@role_required(Role.ADMIN, Role.SELLER)
def get_invoices_by_client_id(client_id):
    invoices = Invoices.get_by_client_id(client_id)

    if invoices:
        return jsonify([{
            'id': invoice.id,
            'client_id': invoice.client_id,
            'user_id': invoice.user_id,
            'date': invoice.date.isoformat(),
            'total': invoice.total,
            'completed': invoice.completed,
            'active': invoice.active
        } for invoice in invoices])
    else:
        return jsonify({
            'error': 'No invoices found for the specified client'
        }), 404
        
@invoices_bp.route('/invoices', methods=['POST'])
@token_required
@role_required(Role.ADMIN, Role.SELLER)
def create_invoice():
    data = request.get_json(silent=True) or {}
    
    client_id = data.get('client_id')
    user_id = data.get('user_id')

    errors = {}

    if not client_id:
        errors['client_id'] = 'client_id is required'

    if not user_id:
        errors['user_id'] = 'user_id is required'
    
    if client_id:
        client = Clients.get_by_id(client_id)

        if not client:
            errors['client_id'] = 'client_id does not exist'
        elif client.active != 1:
            errors['client_id'] = 'client must be active'
    
    if user_id:
        user = Users.get_by_id(user_id)

        if not user:
            errors['user_id'] = 'user_id does not exist'
        elif user.active != 1:
            errors['user_id'] = 'user must be active'
        elif user.role != Role.SELLER:
            errors['user_id'] = 'user must have SELLER role'
        elif g.current_user.role == Role.SELLER and user_id != g.current_user.id:
            errors['user_id'] = 'SELLER can only create invoices with their own user_id'
    
    if errors:
        return jsonify({
            'success': False,
            'message': 'Errors in data validation',
            'validation-errors': errors
        }), 400
        
    invoice = Invoices(client_id=client_id, user_id=user_id)
    invoice.save()
    return jsonify({
        'id': invoice.id,   
        'client_id': invoice.client_id,
        'user_id': invoice.user_id,
        'date': invoice.date.isoformat(),
        'total': invoice.total,
        'completed': invoice.completed,
        'active': invoice.active
    }), 201
