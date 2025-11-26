"""
Vista de debug temporal para verificar datos
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection

def debug_data(request):
    """Vista temporal para verificar datos en las tablas"""
    
    resultados = {}
    
    with connection.cursor() as cursor:
        # Contar abogados
        cursor.execute("SELECT COUNT(*) FROM ABOGADO")
        resultados['total_abogados'] = cursor.fetchone()[0]
        
        # Listar abogados
        cursor.execute("SELECT CEDULA, NOMBRE, APELLIDO FROM ABOGADO")
        resultados['abogados'] = [{'cedula': r[0], 'nombre': r[1], 'apellido': r[2]} for r in cursor.fetchall()]
        
        # Contar FK_ABOGADO_ESPECIAL
        cursor.execute("SELECT COUNT(*) FROM FK_ABOGADO_ESPECIAL")
        resultados['total_abogado_especial'] = cursor.fetchone()[0]
        
        # Listar relaciones abogado-especializacion
        cursor.execute("""
            SELECT ae.CEDULA, a.NOMBRE, a.APELLIDO, ae.CODESPECIALIZACION, e.NOMESPECIALIZACION
            FROM FK_ABOGADO_ESPECIAL ae
            JOIN ABOGADO a ON ae.CEDULA = a.CEDULA
            JOIN ESPECIALIZACION e ON ae.CODESPECIALIZACION = e.CODESPECIALIZACION
        """)
        resultados['relaciones_abogado_especial'] = [
            {'cedula': r[0], 'nombre': r[1], 'apellido': r[2], 'cod_esp': r[3], 'nombre_esp': r[4]} 
            for r in cursor.fetchall()
        ]
        
        # Contar expedientes
        cursor.execute("SELECT COUNT(*) FROM EXPEDIENTE")
        resultados['total_expedientes'] = cursor.fetchone()[0]
        
        # Listar expedientes
        cursor.execute("""
            SELECT NOCASO, CONSECEXPE, CODESPECIALIZACION, NINSTANCIA
            FROM EXPEDIENTE
            ORDER BY NOCASO, CONSECEXPE
        """)
        resultados['expedientes'] = [
            {'nocaso': r[0], 'consec': r[1], 'especializ': r[2], 'instancia': r[3]} 
            for r in cursor.fetchall()
        ]
        
        # Casos
        cursor.execute("SELECT NOCASO, CODCLIENTE, CODESPECIALIZACION FROM CASO")
        resultados['casos'] = [{'nocaso': r[0], 'cliente': r[1], 'especializ': r[2]} for r in cursor.fetchall()]
    
    return JsonResponse(resultados, json_dumps_params={'indent': 2})
