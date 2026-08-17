"""initial migration - create all tables

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[Sequence[str], None] = None
depends_on: Union[Sequence[str], None] = None


def upgrade() -> None:
    # Create enums first
    sa.Enum('DRAFT', 'ORDERED', 'PARTIALLY_RECEIVED', 'RECEIVED', 'CANCELLED', name='purchaseorderstatus').create(op.get_bind())
    sa.Enum('PENDING', 'DISPATCHED', 'IN_TRANSIT', 'OUT_FOR_DELIVERY', 'DELIVERED', 'DELAYED', 'CANCELLED', name='shipmentstatus').create(op.get_bind())
    sa.Enum('CASH', 'UPI', 'CARD', 'BANK_TRANSFER', 'ONLINE', name='paymentmethod').create(op.get_bind())
    sa.Enum('PENDING', 'AUTHORIZED', 'PAID', 'PARTIALLY_PAID', 'FAILED', 'CANCELLED', 'REFUNDED', 'PARTIALLY_REFUNDED', name='paymentstatus').create(op.get_bind())
    sa.Enum('DAMAGED', 'WRONG_ITEM', 'CUSTOMER_CHANGED_MIND', 'DEFECTIVE', 'OTHER', name='returnreason').create(op.get_bind())
    sa.Enum('RESELLABLE', 'DAMAGED', name='returncondition').create(op.get_bind())

    # Users and roles
    op.create_table('permissions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String()),
        sa.Column('resource', sa.String()),
        sa.Column('action', sa.String()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    op.create_table('roles',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String()),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    op.create_table('users',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('full_name', sa.String()),
        sa.Column('phone', sa.String()),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

    op.create_table('user_roles',
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('role_id', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('user_id', 'role_id'),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'])
    )

    op.create_table('role_permissions',
        sa.Column('role_id', sa.String(), nullable=False),
        sa.Column('permission_id', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('role_id', 'permission_id'),
        sa.ForeignKeyConstraint(['permission_id'], ['permissions.id']),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'])
    )

    # Product catalog
    op.create_table('brands',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String()),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    op.create_table('categories',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String()),
        sa.Column('parent_id', sa.String()),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.ForeignKeyConstraint(['parent_id'], ['categories.id'])
    )

    op.create_table('colors',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('hex_code', sa.String()),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    op.create_table('collections',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('season', sa.String()),
        sa.Column('year', sa.String()),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    op.create_table('designs',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String()),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    op.create_table('fabrics',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String()),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    op.create_table('suppliers',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('contact_person', sa.String()),
        sa.Column('phone', sa.String()),
        sa.Column('email', sa.String()),
        sa.Column('address', sa.Text()),
        sa.Column('city', sa.String()),
        sa.Column('state', sa.String()),
        sa.Column('postal_code', sa.String()),
        sa.Column('gstin', sa.String()),
        sa.Column('notes', sa.Text()),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Saree products
    op.create_table('sarees',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('sku', sa.String(), nullable=False),
        sa.Column('barcode', sa.String()),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('brand_id', sa.String()),
        sa.Column('category_id', sa.String()),
        sa.Column('fabric_id', sa.String()),
        sa.Column('color_id', sa.String()),
        sa.Column('design_id', sa.String()),
        sa.Column('collection_id', sa.String()),
        sa.Column('supplier_id', sa.String()),
        sa.Column('occasion', sa.String()),
        sa.Column('season', sa.String()),
        sa.Column('weave', sa.String()),
        sa.Column('pattern', sa.String()),
        sa.Column('border', sa.String()),
        sa.Column('blouse_included', sa.Boolean(), nullable=True),
        sa.Column('length', sa.Numeric(precision=5, scale=2)),
        sa.Column('weight', sa.Numeric(precision=5, scale=2)),
        sa.Column('origin', sa.String()),
        sa.Column('handloom', sa.Boolean(), nullable=True),
        sa.Column('purchase_price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('selling_price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('mrp', sa.Numeric(precision=10, scale=2)),
        sa.Column('discount_percent', sa.Numeric(precision=5, scale=2)),
        sa.Column('tax_percent', sa.Numeric(precision=5, scale=2)),
        sa.Column('description', sa.Text()),
        sa.Column('reorder_level', sa.Integer()),
        sa.Column('current_stock', sa.Integer()),
        sa.Column('status', sa.String()),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['brand_id'], ['brands.id']),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id']),
        sa.ForeignKeyConstraint(['color_id'], ['colors.id']),
        sa.ForeignKeyConstraint(['collection_id'], ['collections.id']),
        sa.ForeignKeyConstraint(['design_id'], ['designs.id']),
        sa.ForeignKeyConstraint(['fabric_id'], ['fabrics.id']),
        sa.ForeignKeyConstraint(['supplier_id'], ['suppliers.id'])
    )
    op.create_index(op.f('ix_sarees_barcode'), 'sarees', ['barcode'], unique=True)
    op.create_index(op.f('ix_sarees_sku'), 'sarees', ['sku'], unique=True)

    op.create_table('saree_images',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('saree_id', sa.String(), nullable=False),
        sa.Column('image_url', sa.String(), nullable=False),
        sa.Column('is_primary', sa.Boolean(), nullable=True),
        sa.Column('display_order', sa.Integer()),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['saree_id'], ['sarees.id'])
    )

    # Inventory
    op.create_table('inventory',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('saree_id', sa.String(), nullable=False),
        sa.Column('quantity', sa.Integer()),
        sa.Column('reserved_quantity', sa.Integer()),
        sa.Column('location', sa.String()),
        sa.Column('last_counted_at', sa.DateTime()),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['saree_id'], ['sarees.id'])
    )

    op.create_table('stock_transactions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('saree_id', sa.String(), nullable=False),
        sa.Column('transaction_type', sa.String(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('previous_quantity', sa.Integer()),
        sa.Column('new_quantity', sa.Integer()),
        sa.Column('reference_type', sa.String()),
        sa.Column('reference_id', sa.String()),
        sa.Column('notes', sa.Text()),
        sa.Column('performed_by', sa.String()),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['performed_by'], ['users.id']),
        sa.ForeignKeyConstraint(['saree_id'], ['sarees.id'])
    )
    op.create_index(op.f('ix_stock_transactions_created_at'), 'stock_transactions', ['created_at'], unique=False)

    op.create_table('stock_adjustments',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('saree_id', sa.String(), nullable=False),
        sa.Column('adjustment_type', sa.String(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('reason', sa.String(), nullable=False),
        sa.Column('notes', sa.Text()),
        sa.Column('performed_by', sa.String()),
        sa.Column('approved_by', sa.String()),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['approved_by'], ['users.id']),
        sa.ForeignKeyConstraint(['performed_by'], ['users.id']),
        sa.ForeignKeyConstraint(['saree_id'], ['sarees.id'])
    )

    # Purchasing
    op.create_table('purchase_orders',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('order_number', sa.String(), nullable=False),
        sa.Column('supplier_id', sa.String(), nullable=False),
        sa.Column('status', postgresql.ENUM(name='purchaseorderstatus', create_type=False), nullable=True),
        sa.Column('order_date', sa.DateTime(), nullable=True),
        sa.Column('expected_delivery_date', sa.DateTime()),
        sa.Column('total_amount', sa.Numeric(precision=12, scale=2)),
        sa.Column('notes', sa.Text()),
        sa.Column('created_by', sa.String()),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('order_number'),
        sa.ForeignKeyConstraint(['created_by'], ['users.id']),
        sa.ForeignKeyConstraint(['supplier_id'], ['suppliers.id'])
    )

    op.create_table('shipments',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('purchase_order_id', sa.String()),
        sa.Column('supplier_id', sa.String()),
        sa.Column('tracking_number', sa.String()),
        sa.Column('carrier', sa.String()),
        sa.Column('status', postgresql.ENUM(name='shipmentstatus', create_type=False), nullable=True),
        sa.Column('expected_delivery', sa.DateTime()),
        sa.Column('actual_delivery', sa.DateTime()),
        sa.Column('notes', sa.Text()),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['purchase_order_id'], ['purchase_orders.id']),
        sa.ForeignKeyConstraint(['supplier_id'], ['suppliers.id'])
    )

    op.create_table('purchase_items',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('purchase_order_id', sa.String(), nullable=False),
        sa.Column('saree_id', sa.String(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('unit_price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('total_price', sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column('received_quantity', sa.Integer()),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['purchase_order_id'], ['purchase_orders.id']),
        sa.ForeignKeyConstraint(['saree_id'], ['sarees.id'])
    )

    op.create_table('receivings',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('purchase_order_id', sa.String(), nullable=False),
        sa.Column('receiving_number', sa.String(), nullable=False),
        sa.Column('received_date', sa.DateTime(), nullable=True),
        sa.Column('received_by', sa.String()),
        sa.Column('notes', sa.Text()),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('purchase_order_id'),
        sa.UniqueConstraint('receiving_number'),
        sa.ForeignKeyConstraint(['purchase_order_id'], ['purchase_orders.id']),
        sa.ForeignKeyConstraint(['received_by'], ['users.id'])
    )

    op.create_table('receiving_items',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('receiving_id', sa.String(), nullable=False),
        sa.Column('purchase_item_id', sa.String(), nullable=False),
        sa.Column('quantity_received', sa.Integer(), nullable=False),
        sa.Column('condition', sa.String()),
        sa.Column('notes', sa.Text()),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['purchase_item_id'], ['purchase_items.id']),
        sa.ForeignKeyConstraint(['receiving_id'], ['receivings.id'])
    )

    # Customers
    op.create_table('customers',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('phone', sa.String()),
        sa.Column('email', sa.String()),
        sa.Column('address', sa.Text()),
        sa.Column('city', sa.String()),
        sa.Column('state', sa.String()),
        sa.Column('postal_code', sa.String()),
        sa.Column('notes', sa.Text()),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_customers_phone'), 'customers', ['phone'], unique=False)

    op.create_table('customer_addresses',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('customer_id', sa.String(), nullable=False),
        sa.Column('address_type', sa.String()),
        sa.Column('address_line1', sa.String(), nullable=False),
        sa.Column('address_line2', sa.String()),
        sa.Column('city', sa.String(), nullable=False),
        sa.Column('state', sa.String(), nullable=False),
        sa.Column('postal_code', sa.String(), nullable=False),
        sa.Column('is_default', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['customer_id'], ['customers.id'])
    )

    # Sales
    op.create_table('sales',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('invoice_number', sa.String(), nullable=False),
        sa.Column('customer_id', sa.String()),
        sa.Column('cashier_id', sa.String()),
        sa.Column('status', sa.String()),
        sa.Column('is_held', sa.Boolean(), nullable=True),
        sa.Column('subtotal', sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column('discount_amount', sa.Numeric(precision=12, scale=2)),
        sa.Column('tax_amount', sa.Numeric(precision=12, scale=2)),
        sa.Column('total_amount', sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column('amount_paid', sa.Numeric(precision=12, scale=2)),
        sa.Column('balance_due', sa.Numeric(precision=12, scale=2)),
        sa.Column('notes', sa.Text()),
        sa.Column('sale_date', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('invoice_number'),
        sa.ForeignKeyConstraint(['cashier_id'], ['users.id']),
        sa.ForeignKeyConstraint(['customer_id'], ['customers.id'])
    )
    op.create_index(op.f('ix_sales_sale_date'), 'sales', ['sale_date'], unique=False)

    op.create_table('returns',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('return_number', sa.String(), nullable=False),
        sa.Column('sale_id', sa.String(), nullable=False),
        sa.Column('customer_id', sa.String()),
        sa.Column('total_refund_amount', sa.Numeric(precision=12, scale=2)),
        sa.Column('refund_status', sa.String()),
        sa.Column('reason', postgresql.ENUM(name='returnreason', create_type=False)),
        sa.Column('notes', sa.Text()),
        sa.Column('return_date', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('return_number'),
        sa.ForeignKeyConstraint(['customer_id'], ['customers.id']),
        sa.ForeignKeyConstraint(['sale_id'], ['sales.id'])
    )

    op.create_table('sale_items',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('sale_id', sa.String(), nullable=False),
        sa.Column('saree_id', sa.String(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('unit_price', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('discount_percent', sa.Numeric(precision=5, scale=2)),
        sa.Column('tax_percent', sa.Numeric(precision=5, scale=2)),
        sa.Column('subtotal', sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column('discount_amount', sa.Numeric(precision=12, scale=2)),
        sa.Column('tax_amount', sa.Numeric(precision=12, scale=2)),
        sa.Column('total', sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['sale_id'], ['sales.id']),
        sa.ForeignKeyConstraint(['saree_id'], ['sarees.id'])
    )

    op.create_table('return_items',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('return_id', sa.String(), nullable=False),
        sa.Column('sale_item_id', sa.String(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('condition', postgresql.ENUM(name='returncondition', create_type=False), nullable=False),
        sa.Column('refund_amount', sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column('notes', sa.Text()),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['return_id'], ['returns.id']),
        sa.ForeignKeyConstraint(['sale_item_id'], ['sale_items.id'])
    )

    op.create_table('payments',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('sale_id', sa.String(), nullable=False),
        sa.Column('payment_method', postgresql.ENUM(name='paymentmethod', create_type=False), nullable=False),
        sa.Column('amount', sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column('status', postgresql.ENUM(name='paymentstatus', create_type=False), nullable=True),
        sa.Column('transaction_id', sa.String()),
        sa.Column('reference_id', sa.String()),
        sa.Column('provider', sa.String()),
        sa.Column('notes', sa.Text()),
        sa.Column('metadata_', sa.String()),
        sa.Column('paid_at', sa.DateTime()),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['sale_id'], ['sales.id'])
    )

    # Finance
    op.create_table('cash_registers',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('expenses',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('expense_number', sa.String(), nullable=False),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('amount', sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('payment_method', sa.String()),
        sa.Column('vendor', sa.String()),
        sa.Column('notes', sa.Text()),
        sa.Column('expense_date', sa.DateTime(), nullable=True),
        sa.Column('created_by', sa.String()),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('expense_number'),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'])
    )

    op.create_table('cash_transactions',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('register_id', sa.String(), nullable=False),
        sa.Column('transaction_type', sa.String(), nullable=False),
        sa.Column('amount', sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('reference_type', sa.String()),
        sa.Column('reference_id', sa.String()),
        sa.Column('performed_by', sa.String()),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['performed_by'], ['users.id']),
        sa.ForeignKeyConstraint(['register_id'], ['cash_registers.id'])
    )
    op.create_index(op.f('ix_cash_transactions_created_at'), 'cash_transactions', ['created_at'], unique=False)

    op.create_table('audit_logs',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String()),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('resource', sa.String()),
        sa.Column('resource_id', sa.String()),
        sa.Column('ip_address', sa.String()),
        sa.Column('user_agent', sa.String()),
        sa.Column('before_values', sa.Text()),
        sa.Column('after_values', sa.Text()),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'])
    )
    op.create_index(op.f('ix_audit_logs_created_at'), 'audit_logs', ['created_at'], unique=False)

    op.create_table('notifications',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('type', sa.String()),
        sa.Column('is_read', sa.Boolean(), nullable=True),
        sa.Column('recipient_user_id', sa.String()),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['recipient_user_id'], ['users.id'])
    )

    op.create_table('application_settings',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('key', sa.String(), nullable=False),
        sa.Column('value', sa.Text(), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('is_public', sa.Boolean(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('key')
    )

    op.create_table('backup_records',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('backup_path', sa.String(), nullable=False),
        sa.Column('backup_size', sa.Numeric(precision=15, scale=2)),
        sa.Column('status', sa.String()),
        sa.Column('notes', sa.Text()),
        sa.Column('created_by', sa.String()),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'])
    )
    op.create_index(op.f('ix_backup_records_created_at'), 'backup_records', ['created_at'], unique=False)


def downgrade() -> None:
    # Drop all tables in reverse order
    op.drop_table('backup_records')
    op.drop_table('application_settings')
    op.drop_table('notifications')
    op.drop_table('audit_logs')
    op.drop_table('cash_transactions')
    op.drop_table('expenses')
    op.drop_table('cash_registers')
    op.drop_table('payments')
    op.drop_table('return_items')
    op.drop_table('sale_items')
    op.drop_table('returns')
    op.drop_table('sales')
    op.drop_table('customer_addresses')
    op.drop_table('customers')
    op.drop_table('receiving_items')
    op.drop_table('receivings')
    op.drop_table('purchase_items')
    op.drop_table('shipments')
    op.drop_table('purchase_orders')
    op.drop_table('stock_adjustments')
    op.drop_table('stock_transactions')
    op.drop_table('inventory')
    op.drop_table('saree_images')
    op.drop_table('sarees')
    op.drop_table('suppliers')
    op.drop_table('fabrics')
    op.drop_table('designs')
    op.drop_table('collections')
    op.drop_table('colors')
    op.drop_table('categories')
    op.drop_table('brands')
    op.drop_table('role_permissions')
    op.drop_table('user_roles')
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('permissions')

    # Drop enums
    sa.Enum(name='returncondition').drop(op.get_bind())
    sa.Enum(name='returnreason').drop(op.get_bind())
    sa.Enum(name='paymentstatus').drop(op.get_bind())
    sa.Enum(name='paymentmethod').drop(op.get_bind())
    sa.Enum(name='shipmentstatus').drop(op.get_bind())
    sa.Enum(name='purchaseorderstatus').drop(op.get_bind())
