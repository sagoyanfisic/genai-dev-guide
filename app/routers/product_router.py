from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.core.dependencies import get_product_service
from app.application.product_service import ProductService
from .schemas import (
    ProductCreateRequest, 
    ProductUpdateRequest, 
    StockUpdateRequest,
    CategorySuggestionsResponse,
    ProductResponse,
    StockUpdateResponse,
    MessageResponse
)

router = APIRouter(prefix="/products", tags=["Product Catalog"])

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreateRequest,
    service: ProductService = Depends(get_product_service)
):
    """Crear un nuevo producto con descripción generada por AI"""
    try:
        product = service.create_product(
            name=product_data.name,
            price=product_data.price,
            category=product_data.category,
            brand=product_data.brand,
            stock_quantity=product_data.stock_quantity,
            basic_info=product_data.basic_info,
            auto_generate_description=product_data.auto_generate_description
        )
        
        return ProductResponse.model_validate(product)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/", response_model=list[ProductResponse])
def get_all_products(
    available_only: bool = Query(False, description="Only return available products"),
    service: ProductService = Depends(get_product_service)
):
    """Obtener todos los productos"""
    try:
        if available_only:
            products = service.get_available_products()
        else:
            products = service.get_all_products()
        
        return [ProductResponse.model_validate(product) for product in products]
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.get("/{product_id}", response_model=ProductResponse)
def get_product_by_id(
    product_id: int,
    service: ProductService = Depends(get_product_service)
):
    """Obtener un producto por ID"""
    try:
        product = service.get_product_by_id(product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        
        return ProductResponse.model_validate(product)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdateRequest,
    service: ProductService = Depends(get_product_service)
):
    """Actualizar un producto"""
    try:
        product = service.update_product(
            product_id=product_id,
            name=product_data.name,
            price=product_data.price,
            category=product_data.category,
            brand=product_data.brand,
            stock_quantity=product_data.stock_quantity,
            description=product_data.description
        )
        
        return ProductResponse.model_validate(product)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.patch("/{product_id}/stock", response_model=StockUpdateResponse)
def update_stock(
    product_id: int,
    stock_data: StockUpdateRequest,
    service: ProductService = Depends(get_product_service)
):
    """Actualizar stock de un producto"""
    try:
        product = service.update_stock(product_id, stock_data.new_stock)
        return StockUpdateResponse(
            message="Stock updated successfully", 
            new_stock=product.stock_quantity
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.patch("/{product_id}/deactivate", response_model=MessageResponse)
def deactivate_product(
    product_id: int,
    service: ProductService = Depends(get_product_service)
):
    """Desactivar un producto"""
    try:
        service.deactivate_product(product_id)
        return MessageResponse(message="Product deactivated successfully")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.patch("/{product_id}/activate", response_model=MessageResponse)
def activate_product(
    product_id: int,
    service: ProductService = Depends(get_product_service)
):
    """Activar un producto"""
    try:
        service.activate_product(product_id)
        return MessageResponse(message="Product activated successfully")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.delete("/{product_id}", response_model=MessageResponse, status_code=status.HTTP_200_OK)
def delete_product(
    product_id: int,
    service: ProductService = Depends(get_product_service)
):
    """Eliminar un producto permanentemente"""
    try:
        success = service.delete_product(product_id)
        if success:
            return MessageResponse(message="Product deleted successfully")
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/category/{category}", response_model=list[ProductResponse])
def get_products_by_category(
    category: str,
    service: ProductService = Depends(get_product_service)
):
    """Obtener productos por categoría"""
    try:
        products = service.get_products_by_category(category)
        return [ProductResponse.model_validate(product) for product in products]
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.get("/search/{search_term}", response_model=list[ProductResponse])
def search_products(
    search_term: str,
    service: ProductService = Depends(get_product_service)
):
    """Buscar productos por nombre o descripción"""
    try:
        products = service.search_products(search_term)
        return [ProductResponse.model_validate(product) for product in products]
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@router.post("/{product_id}/improve-description", response_model=ProductResponse)
def improve_product_description(
    product_id: int,
    service: ProductService = Depends(get_product_service)
):
    """Mejorar la descripción de un producto usando AI"""
    try:
        product = service.improve_product_description(product_id)
        return ProductResponse.model_validate(product)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
