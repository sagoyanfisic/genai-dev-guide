from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from typing import List, Optional
from decimal import Decimal
from app.models.product import Product as ProductModel
from app.domain.entities import Product

class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, product: Product) -> Product:
        if product.id:
            db_product = self.session.get(ProductModel, product.id)
            if db_product:
                db_product.name = product.name
                db_product.description = product.description
                db_product.price = product.price
                db_product.category = product.category
                db_product.brand = product.brand
                db_product.stock_quantity = product.stock_quantity
                db_product.is_active = product.is_active
            else:
                raise Exception(f"Product with id {product.id} not found")
        else:
            db_product = ProductModel(
                name=product.name,
                description=product.description,
                price=product.price,
                category=product.category,
                brand=product.brand,
                stock_quantity=product.stock_quantity,
                is_active=product.is_active
            )
            self.session.add(db_product)
        
        self.session.commit()
        self.session.refresh(db_product)
        
        product.id = db_product.id
        product.created_at = db_product.created_at
        product.updated_at = db_product.updated_at
        
        return product

    def find_by_id(self, product_id: int) -> Optional[Product]:
        db_product = self.session.get(ProductModel, product_id)
        
        if not db_product:
            return None
        
        return Product(
            id=db_product.id,
            name=db_product.name,
            description=db_product.description,
            price=db_product.price,
            category=db_product.category,
            brand=db_product.brand,
            stock_quantity=db_product.stock_quantity,
            is_active=db_product.is_active,
            created_at=db_product.created_at,
            updated_at=db_product.updated_at
        )

    def find_by_name(self, name: str) -> Optional[Product]:
        result = self.session.execute(
            select(ProductModel).where(ProductModel.name == name)
        )
        db_product = result.scalar_one_or_none()
        
        if not db_product:
            return None
        
        return Product(
            id=db_product.id,
            name=db_product.name,
            description=db_product.description,
            price=db_product.price,
            category=db_product.category,
            brand=db_product.brand,
            stock_quantity=db_product.stock_quantity,
            is_active=db_product.is_active,
            created_at=db_product.created_at,
            updated_at=db_product.updated_at
        )

    def get_all_active(self) -> List[Product]:
        result = self.session.execute(
            select(ProductModel).where(ProductModel.is_active == True)
        )
        db_products = result.scalars().all()
        
        return [self._map_to_domain(product) for product in db_products]

    def get_by_category(self, category: str) -> List[Product]:
        result = self.session.execute(
            select(ProductModel).where(
                and_(ProductModel.category == category, ProductModel.is_active == True)
            )
        )
        db_products = result.scalars().all()
        
        return [self._map_to_domain(product) for product in db_products]

    def search_by_name_or_description(self, search_term: str) -> List[Product]:
        search_pattern = f"%{search_term}%"
        result = self.session.execute(
            select(ProductModel).where(
                and_(
                    ProductModel.is_active == True,
                    (ProductModel.name.ilike(search_pattern) | 
                     ProductModel.description.ilike(search_pattern))
                )
            )
        )
        db_products = result.scalars().all()
        
        return [self._map_to_domain(product) for product in db_products]

    def delete(self, product_id: int) -> bool:
        db_product = self.session.get(ProductModel, product_id)
        if db_product:
            self.session.delete(db_product)
            self.session.commit()
            return True
        return False


    def _map_to_domain(self, db_product: ProductModel) -> Product:
        return Product(
            id=db_product.id,
            name=db_product.name,
            description=db_product.description,
            price=db_product.price,
            category=db_product.category,
            brand=db_product.brand,
            stock_quantity=db_product.stock_quantity,
            is_active=db_product.is_active,
            created_at=db_product.created_at,
            updated_at=db_product.updated_at
        )