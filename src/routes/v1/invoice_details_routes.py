from flask import Blueprint, jsonify, request
from src.models.invoices import Invoices
from src.utils.auth import token_required, role_required
from src.models.invoice_details import InvoiceDetails
from src.models.users import Role
from src.models.products import Products


invoice_details_bp = Blueprint(
    'invoice_details_v1',
    __name__,
    url_prefix='/api/v1'
)


# GET: Consultar los detalles de una factura
@invoice_details_bp.route(
    '/invoices/<int:invoice_id>/details',
    methods=['GET']
)
@token_required
@role_required(Role.ADMIN, Role.SELLER)
def get_invoice_details_by_invoice_id(invoice_id):

    invoice = Invoices.get_by_id(invoice_id)

    if not invoice:
        return jsonify({'error': 'Invoice not found'}), 404

    invoice_details = InvoiceDetails.get_by_invoice(invoice_id)

    return jsonify({
        'invoice_id': invoice.id,
        'total': invoice.total,
        'data': [{
            'id': detail.id,
            'invoice_id': detail.invoice_id,
            'product_id': detail.product_id,
            'quantity': detail.quantity,
            'unit_price': detail.unit_price,
            'subtotal': detail.quantity * detail.unit_price
        } for detail in invoice_details]
    }), 200


# POST: Agregar productos a una factura
@invoice_details_bp.route(
    '/invoices/<int:invoice_id>/details',
    methods=['POST']
)
@token_required
@role_required(Role.ADMIN, Role.SELLER)
def create_invoice_detail(invoice_id):

    # 1. Recibir los datos del Body
    data = request.get_json() or {}
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    # 2. Buscar la factura
    invoice = Invoices.get_by_id(invoice_id)

    if not invoice:
        return jsonify({'error': 'Invoice not found'}), 404

    # 3. Comprobar el estado de la factura
    if invoice.active == 0:
        return jsonify({
            'error': 'Invoice is cancelled and cannot be modified'
        }), 409

    if invoice.completed == True:
        return jsonify({
            'error': 'Invoice is completed and cannot be modified'
        }), 409

    # 4. Validar los datos recibidos
    errors = {}

    if product_id is None:
        errors['product_id'] = 'product_id is required'
        product = None
    else:
        product = Products.get_by_id(product_id)

        if not product:
            errors['product_id'] = 'product_id does not exist'
        elif product.active == 0:
            errors['product_id'] = 'product must be active'

    if quantity is None:
        errors['quantity'] = 'quantity is required'
    elif not isinstance(quantity, (int, float)):
        errors['quantity'] = 'quantity must be a number'
    elif quantity <= 0:
        errors['quantity'] = 'quantity must be greater than 0'

    if errors:
        return jsonify({
            'success': False,
            'message': 'Errors in data validation',
            'validation-errors': errors
        }), 400

    # 5. Comprobar que haya suficiente inventario
    if quantity > product.stock:
        return jsonify({
            'success': False,
            'message': 'Errors in data validation',
            'validation-errors': {
                'quantity': f'not enough stock, available: {product.stock}'
            }
        }), 400

    # 6. Buscar si el producto ya está en la factura
    invoice_detail = InvoiceDetails.get_by_invoice_and_product(
        invoice_id=invoice_id,
        product_id=product_id
    )

    # 7. Crear o actualizar el detalle
    if invoice_detail:
        invoice_detail.quantity += quantity
        unit_price = invoice_detail.unit_price
        status_code = 200

    else:
        unit_price = product.price

        invoice_detail = InvoiceDetails(
            invoice_id=invoice_id,
            product_id=product_id,
            quantity=quantity,
            unit_price=unit_price
        )

        status_code = 201

    # 8. Descontar el inventario
    product.stock -= quantity

    # 9. Actualizar el total de la factura
    invoice.total = round(
        invoice.total + quantity * unit_price,
        2
    )

    # 10. Guardar todos los cambios
    if status_code == 201:
        invoice_detail.save()
    else:
        invoice_detail.update()

    # 11. Responder
    return jsonify({
        'id': invoice_detail.id,
        'invoice_id': invoice_detail.invoice_id,
        'product_id': invoice_detail.product_id,
        'quantity': invoice_detail.quantity,
        'unit_price': invoice_detail.unit_price,
        'subtotal': invoice_detail.quantity * invoice_detail.unit_price
    }), status_code