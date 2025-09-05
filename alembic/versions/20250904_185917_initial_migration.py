"""Initial migration - Create products table

Revision ID: 20250904_185917
Revises: 
Create Date: 2025-09-04 18:59:17.837629

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20250904_185917'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create products table
    op.create_table('products',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('price', sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=False),
        sa.Column('brand', sa.String(length=100), nullable=False),
        sa.Column('stock_quantity', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # Create indexes
    op.create_index('ix_products_category', 'products', ['category'], unique=False)
    op.create_index('ix_products_is_active', 'products', ['is_active'], unique=False)
    op.create_index('ix_products_brand', 'products', ['brand'], unique=False)


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_products_brand', table_name='products')
    op.drop_index('ix_products_is_active', table_name='products')
    op.drop_index('ix_products_category', table_name='products')
    
    # Drop table
    op.drop_table('products')
