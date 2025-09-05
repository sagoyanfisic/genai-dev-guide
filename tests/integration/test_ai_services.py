#!/usr/bin/env python3
"""
Script para probar ambas integraciones de AI: Gemini Direct y Vertex AI
"""
import asyncio
import os
from app.infrastructure.external_services import GeminiAIService

async def test_ai_service():
    """Prueba el servicio AI configurado (Gemini Direct o Vertex AI)"""
    
    print("🧪 Probando servicio AI configurado...")
    
    # Mostrar configuración actual
    use_vertex_ai = os.getenv('USE_VERTEX_AI', 'false').lower() == 'true'
    service_type = "Vertex AI" if use_vertex_ai else "Gemini Direct"
    print(f"📋 Servicio configurado: {service_type}")
    
    if use_vertex_ai:
        project_id = os.getenv('VERTEX_AI_PROJECT_ID') or os.getenv('GCP_PROJECT_ID')
        location = os.getenv('VERTEX_AI_LOCATION', 'us-central1')
        print(f"📋 Project ID: {project_id}")
        print(f"📋 Location: {location}")
        
        if not project_id:
            print("❌ VERTEX_AI_PROJECT_ID o GCP_PROJECT_ID no está configurado")
            return
    else:
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("❌ GOOGLE_API_KEY no está configurada")
            return
        print(f"✅ API Key configurada: {api_key[:10]}...")
    
    try:
        # Crear servicio
        service = GeminiAIService()
        print("✅ Servicio AI creado exitosamente")
        
        # Mostrar información del servicio
        service_info = service.get_service_info()
        print(f"📊 Información del servicio:")
        for key, value in service_info.items():
            print(f"   {key}: {value}")
        
        # Test 1: Generar descripción de producto
        print("\n📝 Test 1: Generando descripción de producto...")
        description = await service.generate_product_description(
            name="MacBook Pro M3",
            category="Laptops",
            brand="Apple",
            basic_info="Laptop profesional con chip M3 y pantalla Retina"
        )
        print("✅ Descripción generada:")
        print(f"📄 {description[:300]}...")
        
        # Test 2: Generar sugerencias
        print("\n💡 Test 2: Generando sugerencias de productos...")
        suggestions = await service.generate_product_suggestions("Smartphones", 3)
        print("✅ Sugerencias generadas:")
        print(f"📄 {suggestions}")
        
        # Test 3: Mejorar descripción
        print("\n✨ Test 3: Mejorando descripción...")
        improved = await service.improve_product_description(
            "Teléfono inteligente con cámara y batería"
        )
        print("✅ Descripción mejorada:")
        print(f"📄 {improved}")
        
        print(f"\n🎉 Todos los tests con {service_type} pasaron exitosamente!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

async def test_configuration_switch():
    """Prueba cambiar entre configuraciones"""
    
    print("\n🔄 Probando cambio de configuración...")
    
    # Test con Gemini Direct
    print("\n--- Probando Gemini Direct ---")
    os.environ['USE_VERTEX_AI'] = 'false'
    await test_ai_service()
    
    # Test con Vertex AI (solo si está configurado)
    project_id = os.getenv('VERTEX_AI_PROJECT_ID') or os.getenv('GCP_PROJECT_ID')
    if project_id:
        print("\n--- Probando Vertex AI ---")
        os.environ['USE_VERTEX_AI'] = 'true'
        await test_ai_service()
    else:
        print("\n⚠️  Saltando test de Vertex AI (no configurado)")

if __name__ == "__main__":
    # Cargar variables de entorno
    from dotenv import load_dotenv
    load_dotenv()
    
    # Ejecutar tests
    asyncio.run(test_ai_service())
    
    # Test opcional de cambio de configuración
    if input("\n¿Probar cambio de configuración? (y/N): ").lower() == 'y':
        asyncio.run(test_configuration_switch())