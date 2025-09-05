"""
Templates de prompts para servicios de AI como constantes
Separamos los prompts de la lógica de negocio
"""

# Product Description Prompts
PRODUCT_DESCRIPTION_BASE_PROMPT = """Genera una descripción atractiva y detallada para un producto de e-commerce.

Información del producto:
- Nombre: {name}
- Categoría: {category}
- Marca: {brand}
{additional_info}

Instrucciones:
1. Crea una descripción comercial atractiva (2-3 párrafos)
2. Destaca las características principales y beneficios
3. Usa un tono profesional pero accesible
4. Incluye posibles usos o aplicaciones
5. NO menciones precios ni disponibilidad

Descripción:"""

# Product Suggestions Prompts
PRODUCT_SUGGESTIONS_PROMPT = """Genera una lista de {count} productos populares para la categoría: {category}

Para cada producto incluye:
- Nombre del producto
- Marca sugerida (puede ser ficticia pero realista)
- Breve descripción (1 línea)

Formato:
1. [Nombre] - [Marca] - [Descripción breve]
2. [Nombre] - [Marca] - [Descripción breve]
...

Lista de productos:"""

# Description Improvement Prompts
IMPROVE_DESCRIPTION_PROMPT = """Mejora la siguiente descripción de producto para hacerla más atractiva y completa:

Descripción actual:
{current_description}

Instrucciones para mejorar:
1. Mantén la información existente
2. Hazla más persuasiva y comercial
3. Agrega detalles relevantes si es apropiado
4. Mejora la estructura y fluidez
5. Asegúrate de que suene profesional

Descripción mejorada:"""

# Helper functions for formatting prompts
def format_product_description_prompt(name: str, category: str, brand: str, basic_info: str = None) -> str:
    """Format product description prompt with parameters"""
    additional_info = f"- Información adicional: {basic_info}" if basic_info else ""
    return PRODUCT_DESCRIPTION_BASE_PROMPT.format(
        name=name,
        category=category,
        brand=brand,
        additional_info=additional_info
    )

def format_product_suggestions_prompt(category: str, count: int = 5) -> str:
    """Format product suggestions prompt with parameters"""
    return PRODUCT_SUGGESTIONS_PROMPT.format(
        category=category,
        count=count
    )

def format_improve_description_prompt(current_description: str) -> str:
    """Format improve description prompt with parameters"""
    return IMPROVE_DESCRIPTION_PROMPT.format(
        current_description=current_description
    )