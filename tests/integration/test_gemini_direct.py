#!/usr/bin/env python3
"""
Script simple para probar la integración directa con Gemini
"""
import asyncio
import os
from app.infrastructure.external_services import GeminiAIService

async def test_gemini_direct():
    print("🧪 Probando integración directa con Gemini...")
    
    # Verificar API key
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ GOOGLE_API_KEY no está configurada")
        return
    
    print(f"✅ API Key configurada: {api_key[:10]}...")
    
    try:
        # Crear servicio
        service = GeminiAIService()
        print("✅ Servicio GeminiAI creado exitosamente")
        
        # Test 1: Generar descripción de producto
        print("\n📝 Test 1: Generando descripción de producto...")
        description = await service.generate_product_description(
            name="iPhone 15 Pro",
            category="Smartphones",
            brand="Apple",
            basic_info="Smartphone premium con chip A17 Pro"
        )
        print("✅ Descripción generada:")
        print(f"📄 {description[:200]}...")
        
        # Test 2: Generar sugerencias
        print("\n💡 Test 2: Generando sugerencias de productos...")
        suggestions = await service.generate_product_suggestions("Laptops", 3)
        print("✅ Sugerencias generadas:")
        print(f"📄 {suggestions}")
        
        # Test 3: Mejorar descripción
        print("\n✨ Test 3: Mejorando descripción...")
        improved = await service.improve_product_description("Laptop básica para trabajo")
        print("✅ Descripción mejorada:")
        print(f"📄 {improved}")
        
        print("\n🎉 Todos los tests pasaron exitosamente!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_gemini_direct())