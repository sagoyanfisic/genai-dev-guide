from typing import List, Optional
from decimal import Decimal
from app.domain.entities import Product
from app.infrastructure.database import ProductRepository
from app.infrastructure.external_services import GeminiAIService

class ProductService:
    def __init__(
        self,
        product_repo: ProductRepository,
        ai_service: GeminiAIService
    ):
        self.product_repo = product_repo
        self.ai_service = ai_service

    def create_product(
        self, 
        name: str, 
        price: Decimal, 
        category: str, 
        brand: str,
        stock_quantity: int = 0,
        basic_info: Optional[str] = None,
        auto_generate_description: bool = True
    ) -> Product:
        """Crear un nuevo producto, opcionalmente con descripción generada por AI"""
        
        existing_product = self.product_repo.find_by_name(name)
        if existing_product:
            raise Exception(f"Product '{name}' already exists")
        
        description = ""
        if auto_generate_description:
            try:
                description = self.ai_service.generate_product_description(
                    name=name,
                    category=category,
                    brand=brand,
                    basic_info=basic_info
                )
            except Exception as e:
                description = basic_info or f"{brand} {name} - {category}"
        else:
            description = basic_info or f"{brand} {name} - {category}"
        
        product = Product(
            name=name,
            description=description,
            price=price,
            category=category,
            brand=brand,
            stock_quantity=stock_quantity,
            is_active=True
        )
        
        if not product.is_valid():
            raise Exception("Product data is invalid")
        
        return self.product_repo.save(product)

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Obtener producto por ID"""
        return self.product_repo.find_by_id(product_id)

    def get_all_products(self) -> List[Product]:
        """Obtener todos los productos activos"""
        return self.product_repo.get_all_active()

    def get_products_by_category(self, category: str) -> List[Product]:
        """Obtener productos por categoría"""
        return self.product_repo.get_by_category(category)

    def search_products(self, search_term: str) -> List[Product]:
        """Buscar productos por nombre o descripción"""
        return self.product_repo.search_by_name_or_description(search_term)

    def update_product(
        self, 
        product_id: int, 
        name: Optional[str] = None,
        price: Optional[Decimal] = None,
        category: Optional[str] = None,
        brand: Optional[str] = None,
        stock_quantity: Optional[int] = None,
        description: Optional[str] = None
    ) -> Product:
        """Actualizar un producto existente"""
        
        product = self.product_repo.find_by_id(product_id)
        if not product:
            raise Exception(f"Product with ID {product_id} not found")
        
        if name is not None:
            product.name = name
        if price is not None:
            product.price = price
        if category is not None:
            product.category = category
        if brand is not None:
            product.brand = brand
        if stock_quantity is not None:
            product.update_stock(stock_quantity)
        if description is not None:
            product.description = description
        
        if not product.is_valid():
            raise Exception("Updated product data is invalid")
        
        return self.product_repo.save(product)

    def update_stock(self, product_id: int, new_stock: int) -> Product:
        """Actualizar stock de un producto"""
        product = self.product_repo.find_by_id(product_id)
        if not product:
            raise Exception(f"Product with ID {product_id} not found")
        
        product.update_stock(new_stock)
        return self.product_repo.save(product)

    def deactivate_product(self, product_id: int) -> Product:
        """Desactivar un producto (soft delete)"""
        product = self.product_repo.find_by_id(product_id)
        if not product:
            raise Exception(f"Product with ID {product_id} not found")
        
        product.deactivate()
        return self.product_repo.save(product)

    def activate_product(self, product_id: int) -> Product:
        """Activar un producto"""
        product = self.product_repo.find_by_id(product_id)
        if not product:
            raise Exception(f"Product with ID {product_id} not found")
        
        product.activate()
        return self.product_repo.save(product)

    def delete_product(self, product_id: int) -> bool:
        """Eliminar permanentemente un producto"""
        return self.product_repo.delete(product_id)

    def improve_product_description(self, product_id: int) -> Product:
        """Mejorar la descripción de un producto usando AI"""
        product = self.product_repo.find_by_id(product_id)
        if not product:
            raise Exception(f"Product with ID {product_id} not found")
        
        if not product.description:
            raise Exception("Product has no description to improve")
        
        try:
            improved_description = self.ai_service.improve_product_description(product.description)
            product.description = improved_description
            return self.product_repo.save(product)
        except Exception as e:
            raise Exception(f"Failed to improve description: {str(e)}")

    def get_category_suggestions(self, category: str, count: int = 5) -> str:
        """Obtener sugerencias de productos para una categoría usando AI"""
        return self.ai_service.generate_product_suggestions(category, count)

    def get_available_products(self) -> List[Product]:
        """Obtener solo productos disponibles (activos y con stock)"""
        all_products = self.product_repo.get_all_active()
        return [product for product in all_products if product.is_available()]