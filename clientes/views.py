"""
Vistas para el Sistema de Gestion Legal
Usando SQL RAW para cumplir con los requerimientos de la sustentacion
"""
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.db import connection
from datetime import date
import json
from django.core.files.storage import FileSystemStorage
from django.views.decorators.http import require_GET


def dictfetchall(cursor):
    """Convierte el resultado del cursor en una lista de diccionarios"""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def dictfetchone(cursor):
    """Convierte una fila del cursor en un diccionario"""
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()
    if row:
        return dict(zip(columns, row))
    return None



# =============================================================================
# REGISTRO DE CLIENTES
# =============================================================================

def registro_cliente(request):
    """Vista principal para el registro de clientes usando SQL RAW"""
    with connection.cursor() as cursor:
        # Obtener tipos de documento - devolver como tuplas para el template
        cursor.execute("SELECT IDTIPODOC, DESCTIPODOC FROM TIPODOCUMENTO ORDER BY DESCTIPODOC")
        tipos_documento = cursor.fetchall()  # Lista de tuplas (id, descripcion)
    
    return render(request, 'clientes/registro_cliente.html', {
        'tipos_documento': tipos_documento
    })


def buscar_cliente(request):
    """Buscar cliente por codigo usando SQL RAW"""
    codcliente = request.GET.get('codigo', '').strip().upper()
    
    if not codcliente:
        return JsonResponse({'encontrado': False, 'mensaje': 'Codigo vacio'})
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT c.CODCLIENTE, c.IDTIPODOC, c.NOMCLIENTE, c.APELLCLIENTE, c.NDOCUMENTO,
                   t.DESCTIPODOC
            FROM CLIENTE c
            LEFT JOIN TIPODOCUMENTO t ON c.IDTIPODOC = t.IDTIPODOC
            WHERE c.CODCLIENTE = :codcliente
        """, {'codcliente': codcliente})
        row = cursor.fetchone()
    
    if row:
        return JsonResponse({
            'encontrado': True,
            'cliente': {
                'codcliente': row[0],
                'idtipodoc': row[1] or '',
                'nomcliente': row[2] or '',
                'apellcliente': row[3] or '',
                'ndocumento': row[4] or '',
                'desctipodoc': row[5] or ''
            }
        })
    else:
        return JsonResponse({'encontrado': False, 'mensaje': 'Cliente no encontrado. Puede registrarlo.'})


def guardar_cliente(request):
    """Guardar o actualizar cliente usando SQL RAW"""
    if request.method != 'POST':
        return JsonResponse({'exito': False, 'mensaje': 'Metodo no permitido'})
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'exito': False, 'mensaje': 'Datos invalidos'})
    
    codcliente = data.get('codcliente', '').strip().upper()
    idtipodoc = data.get('idtipodoc', '').strip()
    nomcliente = data.get('nomcliente', '').strip()
    apellcliente = data.get('apellcliente', '').strip()
    ndocumento = data.get('ndocumento', '').strip()
    
    if not codcliente or not nomcliente or not apellcliente:
        return JsonResponse({'exito': False, 'mensaje': 'Codigo, nombre y apellido son obligatorios'})
    
    try:
        with connection.cursor() as cursor:
            # Verificar si el cliente ya existe
            cursor.execute("SELECT COUNT(*) FROM CLIENTE WHERE CODCLIENTE = :codcliente", {'codcliente': codcliente})
            existe = cursor.fetchone()[0] > 0
            
            if existe:
                # Actualizar
                cursor.execute("""
                    UPDATE CLIENTE 
                    SET IDTIPODOC = :idtipodoc, NOMCLIENTE = :nomcliente, 
                        APELLCLIENTE = :apellcliente, NDOCUMENTO = :ndocumento
                    WHERE CODCLIENTE = :codcliente
                """, {
                    'codcliente': codcliente,
                    'idtipodoc': idtipodoc or None,
                    'nomcliente': nomcliente,
                    'apellcliente': apellcliente,
                    'ndocumento': ndocumento or None
                })
                mensaje = f'Cliente {codcliente} actualizado exitosamente'
            else:
                # Insertar nuevo
                cursor.execute("""
                    INSERT INTO CLIENTE (CODCLIENTE, IDTIPODOC, NOMCLIENTE, APELLCLIENTE, NDOCUMENTO)
                    VALUES (:codcliente, :idtipodoc, :nomcliente, :apellcliente, :ndocumento)
                """, {
                    'codcliente': codcliente,
                    'idtipodoc': idtipodoc or None,
                    'nomcliente': nomcliente,
                    'apellcliente': apellcliente,
                    'ndocumento': ndocumento or None
                })
                mensaje = f'Cliente {codcliente} creado exitosamente'
        
        return JsonResponse({'exito': True, 'mensaje': mensaje})
    except Exception as e:
        return JsonResponse({'exito': False, 'mensaje': str(e)})


def eliminar_cliente(request):
    """Eliminar cliente usando SQL RAW"""
    if request.method != 'POST':
        return JsonResponse({'exito': False, 'mensaje': 'Metodo no permitido'})
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'exito': False, 'mensaje': 'Datos invalidos'})
    
    codcliente = data.get('codcliente', '').strip().upper()
    
    if not codcliente:
        return JsonResponse({'exito': False, 'mensaje': 'Codigo de cliente requerido'})
    
    try:
        with connection.cursor() as cursor:
            # Verificar si tiene casos asociados
            cursor.execute("SELECT COUNT(*) FROM CASO WHERE CODCLIENTE = :codcliente", {'codcliente': codcliente})
            count = cursor.fetchone()[0]
            if count > 0:
                return JsonResponse({'exito': False, 'mensaje': 'No se puede eliminar: el cliente tiene casos asociados'})
            
            cursor.execute("DELETE FROM CLIENTE WHERE CODCLIENTE = :codcliente", {'codcliente': codcliente})
            if cursor.rowcount == 0:
                return JsonResponse({'exito': False, 'mensaje': 'Cliente no encontrado'})
        
        return JsonResponse({'exito': True, 'mensaje': f'Cliente {codcliente} eliminado exitosamente'})
    except Exception as e:
        return JsonResponse({'exito': False, 'mensaje': str(e)})


# =============================================================================
# GESTION DE CASOS
# =============================================================================

def gestion_caso(request):
    """Vista principal para la gestion de casos"""
    with connection.cursor() as cursor:
        # Obtener especializaciones (tipos de caso) como tuplas
        cursor.execute("SELECT CODESPECIALIZACION, NOMESPECIALIZACION FROM ESPECIALIZACION ORDER BY NOMESPECIALIZACION")
        especializaciones = cursor.fetchall()
    
    return render(request, 'clientes/gestion_caso.html', {
        'especializaciones': especializaciones
    })


def buscar_cliente_caso(request):
    """Buscar cliente por nombre y apellido o por codigo para gestion de caso"""
    codigo = request.GET.get('codigo', '').strip().upper()
    nombre = request.GET.get('nombre', '').strip().upper()
    apellido = request.GET.get('apellido', '').strip().upper()
    
    with connection.cursor() as cursor:
        if nombre and apellido:
            # Buscar por nombre y apellido
            cursor.execute("""
                SELECT c.CODCLIENTE, c.NOMCLIENTE, c.APELLCLIENTE, c.NDOCUMENTO,
                       t.DESCTIPODOC
                FROM CLIENTE c
                LEFT JOIN TIPODOCUMENTO t ON c.IDTIPODOC = t.IDTIPODOC
                WHERE UPPER(c.NOMCLIENTE) LIKE :nombre AND UPPER(c.APELLCLIENTE) LIKE :apellido
            """, {'nombre': '%' + nombre + '%', 'apellido': '%' + apellido + '%'})
        elif codigo:
            # Buscar por codigo
            cursor.execute("""
                SELECT c.CODCLIENTE, c.NOMCLIENTE, c.APELLCLIENTE, c.NDOCUMENTO,
                       t.DESCTIPODOC
                FROM CLIENTE c
                LEFT JOIN TIPODOCUMENTO t ON c.IDTIPODOC = t.IDTIPODOC
                WHERE c.CODCLIENTE = :codigo
            """, {'codigo': codigo})
        else:
            return JsonResponse({'encontrado': False, 'mensaje': 'Ingrese nombre/apellido o codigo'})
        
        row = cursor.fetchone()
    
    if row:
        return JsonResponse({
            'encontrado': True,
            'cliente': {
                'codcliente': row[0],
                'nomcliente': row[1] or '',
                'apellcliente': row[2] or '',
                'ndocumento': row[3] or '',
                'desctipodoc': row[4] or ''
            }
        })
    else:
        return JsonResponse({'encontrado': False, 'mensaje': 'Cliente no encontrado'})


def obtener_casos_cliente(request):
    """Obtener casos de un cliente"""
    codcliente = request.GET.get('codcliente', '').strip().upper()
    
    if not codcliente:
        return JsonResponse({'casos': []})
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT c.NOCASO, c.CODESPECIALIZACION, e.NOMESPECIALIZACION,
                   TO_CHAR(c.FECHAINICIO, 'YYYY-MM-DD') as FECHAINICIO,
                   TO_CHAR(c.FECHAFIN, 'YYYY-MM-DD') as FECHAFIN,
                   c.VALOR
            FROM CASO c
            JOIN ESPECIALIZACION e ON c.CODESPECIALIZACION = e.CODESPECIALIZACION
            WHERE c.CODCLIENTE = :codcliente
            ORDER BY c.FECHAINICIO DESC
        """, {'codcliente': codcliente})
        rows = cursor.fetchall()
    
    casos = []
    for row in rows:
        estado = 'CERRADO' if row[4] else 'ACTIVO'  # FECHAFIN
        casos.append({
            'idcaso': row[0],  # NOCASO
            'tipocaso': row[2],  # NOMESPECIALIZACION
            'fechainicio': row[3] or '',
            'estadocaso': estado,
            'desccaso': f'Valor: {row[5]}' if row[5] else ''  # VALOR
        })
    
    return JsonResponse({'casos': casos})


def obtener_detalle_caso(request):
    """Obtener detalle de un caso especifico"""
    nocaso = request.GET.get('nocaso', '').strip()
    
    if not nocaso:
        return JsonResponse({'encontrado': False, 'mensaje': 'Numero de caso requerido'})
    
    try:
        nocaso = int(nocaso)
    except ValueError:
        return JsonResponse({'encontrado': False, 'mensaje': 'Numero de caso invalido'})
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT c.NOCASO, c.CODCLIENTE, c.CODESPECIALIZACION, e.NOMESPECIALIZACION,
                   TO_CHAR(c.FECHAINICIO, 'YYYY-MM-DD') as FECHAINICIO,
                   TO_CHAR(c.FECHAFIN, 'YYYY-MM-DD') as FECHAFIN,
                   c.VALOR
            FROM CASO c
            JOIN ESPECIALIZACION e ON c.CODESPECIALIZACION = e.CODESPECIALIZACION
            WHERE c.NOCASO = :nocaso
        """, {'nocaso': nocaso})
        row = cursor.fetchone()
    
    if row:
        return JsonResponse({
            'encontrado': True,
            'caso': {
                'nocaso': row[0],
                'codcliente': row[1],
                'codespecializacion': row[2],
                'especializacion': row[3],
                'fechainicio': row[4] or '',
                'fechafin': row[5] or '',
                'valor': row[6] or ''
            }
        })
    else:
        return JsonResponse({'encontrado': False, 'mensaje': 'Caso no encontrado'})


def obtener_siguiente_nocaso(request):
    """Obtener el siguiente numero de caso disponible"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT NVL(MAX(NOCASO), 0) + 1 FROM CASO")
        siguiente = cursor.fetchone()[0]
    
    return JsonResponse({'success': True, 'nocaso': siguiente})


def crear_caso(request):
    """Crear un nuevo caso"""
    if request.method != 'POST':
        return JsonResponse({'exito': False, 'mensaje': 'Metodo no permitido'})
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'exito': False, 'mensaje': 'Datos invalidos'})
    
    codcliente = data.get('codcliente', '').strip().upper()
    codespecializacion = data.get('idtipocaso', '').strip()  # En el form se llama idtipocaso
    fechainicio = data.get('fechainicio', '').strip()
    valor = data.get('desccaso', '').strip()  # Usamos desccaso como valor
    
    if not codcliente:
        return JsonResponse({'exito': False, 'mensaje': 'Cliente requerido'})
    
    if not codespecializacion:
        return JsonResponse({'exito': False, 'mensaje': 'Especializacion requerida'})
    
    if not fechainicio:
        fechainicio = date.today().strftime('%Y-%m-%d')
    
    if not valor:
        valor = '0'
    
    try:
        with connection.cursor() as cursor:
            # Obtener siguiente numero de caso
            cursor.execute("SELECT NVL(MAX(NOCASO), 0) + 1 FROM CASO")
            nocaso = cursor.fetchone()[0]
            
            cursor.execute("""
                INSERT INTO CASO (NOCASO, CODCLIENTE, CODESPECIALIZACION, FECHAINICIO, FECHAFIN, VALOR)
                VALUES (:nocaso, :codcliente, :codespecializacion, TO_DATE(:fechainicio, 'YYYY-MM-DD'), NULL, :valor)
            """, {
                'nocaso': nocaso,
                'codcliente': codcliente,
                'codespecializacion': codespecializacion,
                'fechainicio': fechainicio,
                'valor': valor
            })
        
        return JsonResponse({'exito': True, 'nocaso': nocaso, 'mensaje': f'Caso {nocaso} creado exitosamente'})
    except Exception as e:
        return JsonResponse({'exito': False, 'mensaje': str(e)})


# =============================================================================
# GESTION DE EXPEDIENTES
# =============================================================================

def gestion_expediente(request):
    """Vista principal para la gestion de expedientes"""
    with connection.cursor() as cursor:
        # Obtener ciudades (lugares de tipo Corte que son ciudades principales)
        cursor.execute("""
            SELECT CODLUGAR, NOMLUGAR 
            FROM LUGAR 
            WHERE LUG_CODLUGAR IS NULL
            ORDER BY NOMLUGAR
        """)
        ciudades = dictfetchall(cursor)
        
        # Obtener impugnaciones
        cursor.execute("SELECT IDIMPUGNA, NOMIMPUGNA FROM IMPUGNACION ORDER BY NOMIMPUGNA")
        impugnaciones = dictfetchall(cursor)
    
    return render(request, 'clientes/gestion_expediente.html', {
        'ciudades': ciudades,
        'impugnaciones': impugnaciones
    })


def obtener_caso_expediente(request):
    """Obtener datos de un caso para gestion de expediente"""
    nocaso = request.GET.get('idcaso', '').strip()  # El template usa idcaso
    
    if not nocaso:
        return JsonResponse({'encontrado': False, 'mensaje': 'Numero de caso requerido'})
    
    try:
        nocaso = int(nocaso)
    except ValueError:
        return JsonResponse({'encontrado': False, 'mensaje': 'Numero de caso invalido'})
    
    with connection.cursor() as cursor:
        # Obtener datos del caso
        cursor.execute("""
            SELECT c.NOCASO, c.CODCLIENTE, c.CODESPECIALIZACION, e.NOMESPECIALIZACION,
                   TO_CHAR(c.FECHAINICIO, 'YYYY-MM-DD') as FECHAINICIO,
                   TO_CHAR(c.FECHAFIN, 'YYYY-MM-DD') as FECHAFIN,
                   c.VALOR,
                   cl.NOMCLIENTE, cl.APELLCLIENTE
            FROM CASO c
            JOIN ESPECIALIZACION e ON c.CODESPECIALIZACION = e.CODESPECIALIZACION
            JOIN CLIENTE cl ON c.CODCLIENTE = cl.CODCLIENTE
            WHERE c.NOCASO = :nocaso
        """, {'nocaso': nocaso})
        row = cursor.fetchone()
        
        if not row:
            return JsonResponse({'encontrado': False, 'mensaje': 'Caso no encontrado'})
    
    return JsonResponse({
        'encontrado': True,
        'caso': {
            'nocaso': row[0],
            'codcliente': row[1],
            'codespecializacion': row[2],
            'especializacion': row[3],
            'fechainicio': row[4] or '',
            'fechafin': row[5],  # Puede ser None/NULL
            'valor': row[6] or '',
            'cliente': (row[7] or '') + ' ' + (row[8] or ''),
            'tipocaso': row[3] or ''
        }
    })


def obtener_expedientes_caso(request):
    """Obtener solo los expedientes de un caso (para cargar tabla)"""
    nocaso = request.GET.get('idcaso', '').strip()
    
    if not nocaso:
        return JsonResponse({'expedientes': []})
    
    try:
        nocaso = int(nocaso)
    except ValueError:
        return JsonResponse({'expedientes': []})
    
    with connection.cursor() as cursor:
        # Obtener expedientes con sus datos relacionados
        # Usamos composite keys y obtenemos nombre de etapa via ESPECIA_ETAPA
        cursor.execute("""
            SELECT ex.CODESPECIALIZACION,
                   ex.NOCASO,
                   ex.NINSTANCIA,
                   ex.CONSECEXPE,
                   TO_CHAR(ex.FECHAETAPA, 'YYYY-MM-DD') as FECHAETAPA,
                   a.NOMBRE || ' ' || a.APELLIDO as ABOGADO_NOMBRE,
                   l.NOMLUGAR,
                   ep.NOMETAPA,
                   ex.CEDULA,
                   ex.CODLUGAR
            FROM EXPEDIENTE ex
            LEFT JOIN ABOGADO a ON ex.CEDULA = a.CEDULA
            LEFT JOIN LUGAR l ON ex.CODLUGAR = l.CODLUGAR
            LEFT JOIN ESPECIA_ETAPA ee ON ex.CODESPECIALIZACION = ee.CODESPECIALIZACION 
                                      AND ex.NINSTANCIA = ee.NINSTANCIA
            LEFT JOIN ETAPAPROCESAL ep ON ee.CODETAPA = ep.CODETAPA
            WHERE ex.NOCASO = :nocaso
            ORDER BY ex.CONSECEXPE
        """, {'nocaso': nocaso})
        
        rows = cursor.fetchall()
    
    # Convertir a lista de diccionarios manualmente
    expedientes = []
    for row in rows:
        expedientes.append({
            'codespecializacion': row[0],
            'nocaso': row[1],
            'ninstancia': row[2],
            'consecexpe': row[3],
            'fechaapertura': row[4] or '',
            'abogado': row[5] or 'Sin asignar',
            'entidad': row[6] or '',
            'estadoexpediente': row[7] or f'Instancia {row[2]}',
            'cedula': row[8] or '',
            'codlugar': row[9] or ''
        })
    
    return JsonResponse({'expedientes': expedientes})



def obtener_abogados_especializacion(request):
    """Obtener abogados con una especializacion especifica"""
    codespecializacion = request.GET.get('codespecializacion', '').strip()
    
    if not codespecializacion:
        return JsonResponse({'success': False, 'error': 'Especializacion requerida'})
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT a.CEDULA, a.NOMBRE, a.APELLIDO, a.NTARJETAPROFESIONAL
            FROM ABOGADO a
            JOIN FK_ABOGADO_ESPECIAL ae ON a.CEDULA = ae.CEDULA
            WHERE ae.CODESPECIALIZACION = :codespecializacion
            ORDER BY a.APELLIDO, a.NOMBRE
        """, {'codespecializacion': codespecializacion})
        abogados = dictfetchall(cursor)
    
    return JsonResponse({'success': True, 'abogados': abogados})


def obtener_entidades_ciudad(request):
    """Obtener entidades (juzgados, tribunales) de una ciudad"""
    codciudad = request.GET.get('codciudad', '').strip()
    
    if not codciudad:
        return JsonResponse({'success': False, 'error': 'Ciudad requerida'})
    
    with connection.cursor() as cursor:
        # Obtener todas las entidades que pertenecen a la jerarquia de la ciudad
        cursor.execute("""
            SELECT l.CODLUGAR, l.NOMLUGAR, t.DESCTIPOLUGAR
            FROM LUGAR l
            JOIN TIPOLUGAR t ON l.IDTIPOLUGAR = t.IDTIPOLUGAR
            WHERE l.LUG_CODLUGAR = :codciudad
               OR l.LUG_CODLUGAR IN (SELECT CODLUGAR FROM LUGAR WHERE LUG_CODLUGAR = :codciudad)
            ORDER BY t.IDTIPOLUGAR DESC, l.NOMLUGAR
        """, {'codciudad': codciudad})
        entidades = dictfetchall(cursor)
    
    return JsonResponse({'success': True, 'entidades': entidades})


def obtener_primera_etapa(request):
    """Obtener la primera etapa para una especializacion"""
    codespecializacion = request.GET.get('codespecializacion', '').strip()
    
    if not codespecializacion:
        return JsonResponse({'success': False, 'error': 'Especializacion requerida'})
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ep.CODETAPA, ep.NOMETAPA, ep.ORDEN
            FROM ETAPAPROCESAL ep
            JOIN ESPECIA_ETAPA ee ON ep.CODETAPA = ee.CODETAPA
            WHERE ee.CODESPECIALIZACION = :codespecializacion
            ORDER BY ep.ORDEN
            FETCH FIRST 1 ROWS ONLY
        """, {'codespecializacion': codespecializacion})
        etapa = dictfetchone(cursor)
    
    if etapa:
        return JsonResponse({'success': True, 'etapa': etapa})
    else:
        return JsonResponse({'success': False, 'error': 'No hay etapas configuradas para esta especializacion'})


def obtener_siguiente_etapa(request):
    """Obtener la siguiente etapa para un expediente"""
    return JsonResponse({'success': False, 'error': 'Funcionalidad no disponible en este esquema'})


def obtener_proximo_consecutivo(request):
    """Obtener el siguiente consecutivo de expediente para un caso"""
    nocaso = request.GET.get('nocaso')
    codespecializacion = request.GET.get('codespecializacion')
    ninstancia = request.GET.get('ninstancia', '1')
    
    if not nocaso or not codespecializacion:
        return JsonResponse({'success': False, 'error': 'Parametros incompletos'})
        
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT NVL(MAX(CONSECEXPE), 0) + 1 
            FROM EXPEDIENTE 
            WHERE NOCASO = :nocaso 
              AND CODESPECIALIZACION = :codespecializacion
              AND NINSTANCIA = :ninstancia
        """, {
            'nocaso': nocaso, 
            'codespecializacion': codespecializacion,
            'ninstancia': ninstancia
        })
        consecutivo = cursor.fetchone()[0]
        
    return JsonResponse({'success': True, 'consecutivo': consecutivo})


@require_GET
def impugnaciones_validas(request):
    """Devuelve impugnaciones válidas para una especialización e instancia, según ESPECIA_ETAPA"""
    codespecializacion = request.GET.get('codespecializacion', '').strip()
    ninstancia = request.GET.get('ninstancia', '').strip()
    
    if not codespecializacion or not ninstancia:
        return JsonResponse({'success': False, 'error': 'Faltan parámetros'})
    
    with connection.cursor() as cursor:
        # Buscar impugnaciones válidas para la especialización e instancia
        cursor.execute("""
            SELECT DISTINCT i.IDIMPUGNA, i.NOMIMPUGNA
            FROM ESPECIA_ETAPA ee
            JOIN IMPUGNACION i ON ee.IDIMPUGNA = i.IDIMPUGNA
            WHERE ee.CODESPECIALIZACION = :codespecializacion
              AND ee.NINSTANCIA = :ninstancia
              AND ee.IDIMPUGNA IS NOT NULL
            ORDER BY i.NOMIMPUGNA
        """, {'codespecializacion': codespecializacion, 'ninstancia': ninstancia})
        impugnaciones = dictfetchall(cursor)
    
    return JsonResponse({'success': True, 'impugnaciones': impugnaciones})


def crear_expediente(request):
    """Crear un nuevo expediente usando composite primary keys"""
    if request.method != 'POST':
        return JsonResponse({'exito': False, 'mensaje': 'Metodo no permitido'})
    
    # Manejar JSON o Multipart
    if request.content_type == 'application/json':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'exito': False, 'mensaje': 'Datos invalidos'})
        documentos_files = []
    else:
        data = request.POST
        documentos_files = request.FILES.getlist('documento1')
    
    nocaso = data.get('nocaso', '').strip()
    cedula = data.get('cedula', '').strip() or None
    codlugar = data.get('codlugar', '').strip()
    fechaetapa = data.get('fechaetapa', '').strip()
    descsuceso = data.get('descsuceso', '').strip()
    
    if not nocaso or not codlugar:
        return JsonResponse({'exito': False, 'mensaje': 'Campos requeridos: caso y entidad'})
    
    try:
        nocaso = int(nocaso)
    except ValueError:
        return JsonResponse({'exito': False, 'mensaje': 'Numero de caso invalido'})
    
    if not fechaetapa:
        fechaetapa = date.today().strftime('%Y-%m-%d')
    
    try:
        with connection.cursor() as cursor:
            # Obtener especializacion del caso
            cursor.execute("""
                SELECT CODESPECIALIZACION FROM CASO WHERE NOCASO = :nocaso
            """, {'nocaso': nocaso})
            row = cursor.fetchone()
            
            if not row:
                return JsonResponse({'exito': False, 'mensaje': 'Caso no encontrado'})
            
            codespecializacion = row[0]
            
            # NINSTANCIA = 1 por defecto (Primera Instancia)
            ninstancia = 1
            
            # Obtener siguiente consecutivo de expediente
            cursor.execute("""
                SELECT NVL(MAX(CONSECEXPE), 0) + 1 
                FROM EXPEDIENTE 
                WHERE NOCASO = :nocaso 
                  AND CODESPECIALIZACION = :codespecializacion
                  AND NINSTANCIA = :ninstancia
            """, {'nocaso': nocaso, 'codespecializacion': codespecializacion, 'ninstancia': ninstancia})
            consecexpe = cursor.fetchone()[0]
            
            # Insertar expediente
            cursor.execute("""
                INSERT INTO EXPEDIENTE (NOCASO, CODESPECIALIZACION, NINSTANCIA, CONSECEXPE, CEDULA, CODLUGAR, FECHAETAPA)
                VALUES (:nocaso, :codespecializacion, :ninstancia, :consecexpe, :cedula, :codlugar, TO_DATE(:fechaetapa, 'YYYY-MM-DD'))
            """, {
                'nocaso': nocaso,
                'codespecializacion': codespecializacion,
                'ninstancia': ninstancia,
                'consecexpe': consecexpe,
                'cedula': cedula,
                'codlugar': codlugar,
                'fechaetapa': fechaetapa
            })
            
            # Guardar Suceso si existe (usando composite PK)
            if descsuceso:
                cursor.execute("""
                    SELECT NVL(MAX(CONSUCESO), 0) + 1 
                    FROM SUCESO 
                    WHERE CODESPECIALIZACION = :codespecializacion
                      AND NOCASO = :nocaso
                      AND NINSTANCIA = :ninstancia
                      AND CONSECEXPE = :consecexpe
                """, {
                    'codespecializacion': codespecializacion,
                    'nocaso': nocaso,
                    'ninstancia': ninstancia,
                    'consecexpe': consecexpe
                })
                consuceso = cursor.fetchone()[0]
                cursor.execute("""
                    INSERT INTO SUCESO (CODESPECIALIZACION, NOCASO, NINSTANCIA, CONSECEXPE, CONSUCESO, DESCSUCESO)
                    VALUES (:codespecializacion, :nocaso, :ninstancia, :consecexpe, :consuceso, :descsuceso)
                """, {
                    'codespecializacion': codespecializacion,
                    'nocaso': nocaso,
                    'ninstancia': ninstancia,
                    'consecexpe': consecexpe,
                    'consuceso': consuceso,
                    'descsuceso': descsuceso
                })
            
            # Guardar múltiples Documentos si existen (usando composite PK)
            if documentos_files:
                fs = FileSystemStorage()
                cursor.execute("""
                    SELECT NVL(MAX(CONDOC), 0) 
                    FROM DOCUMENTO 
                    WHERE CODESPECIALIZACION = :codespecializacion
                      AND NOCASO = :nocaso
                      AND NINSTANCIA = :ninstancia
                      AND CONSECEXPE = :consecexpe
                """, {
                    'codespecializacion': codespecializacion,
                    'nocaso': nocaso,
                    'ninstancia': ninstancia,
                    'consecexpe': consecexpe
                })
                condoc = cursor.fetchone()[0] or 0
                
                for archivo in documentos_files:
                    condoc += 1
                    # Shorten filename to fit in UBICADOC (VARCHAR2(50))
                    # Path: docs/C{nocaso}/{filename}
                    # Max path prefix: docs/C12345/ (12 chars) -> leaves 38 chars for filename
                    
                    ext = archivo.name.split('.')[-1]
                    name_only = archivo.name.rsplit('.', 1)[0]
                    
                    # Truncate name if too long (keep extension)
                    max_name_len = 30 # Safe limit
                    if len(name_only) > max_name_len:
                        name_only = name_only[:max_name_len]
                    
                    short_name = f"{name_only}.{ext}"
                    
                    # Use shorter directory structure
                    save_path = f'docs/C{nocaso}/{short_name}'
                    
                    # Check total length just in case
                    if len(save_path) > 50:
                        # Super truncate if still too long
                        remaining = 50 - len(f'docs/C{nocaso}/') - len(ext) - 1
                        short_name = f"{name_only[:remaining]}.{ext}"
                        save_path = f'docs/C{nocaso}/{short_name}'

                    # Save the file (this may return a different path, but we'll use our controlled one)
                    _ = fs.save(save_path, archivo)
                    
                    cursor.execute("""
                        INSERT INTO DOCUMENTO (CODESPECIALIZACION, NOCASO, NINSTANCIA, CONSECEXPE, CONDOC, NOMDOC, UBICADOC)
                        VALUES (:codespecializacion, :nocaso, :ninstancia, :consecexpe, :condoc, :nomdoc, :ubicadoc)
                    """, {
                        'codespecializacion': codespecializacion,
                        'nocaso': nocaso,
                        'ninstancia': ninstancia,
                        'consecexpe': consecexpe,
                        'condoc': condoc,
                        'nomdoc': short_name,
                        'ubicadoc': save_path  # Use our controlled short path, NOT fs.save() return value
                    })
        
        return JsonResponse({
            'exito': True, 
            'consecexpe': consecexpe, 
            'mensaje': f'Expediente {consecexpe} creado exitosamente'
        })
    except Exception as e:
        return JsonResponse({'exito': False, 'mensaje': str(e)})


def actualizar_expediente(request):
    """Actualizar un expediente existente - Requisito B"""
    if request.method != 'POST':
        return JsonResponse({'exito': False, 'mensaje': 'Metodo no permitido'})
    
    # Recibir composite keys para identificar el expediente
    codespecializacion = request.POST.get('codespecializacion', '').strip()
    nocaso = request.POST.get('nocaso', '').strip()
    ninstancia = request.POST.get('ninstancia', '').strip()
    consecexpe = request.POST.get('consecexpe', '').strip()
    
    # Datos actualizables
    cedula = request.POST.get('cedula', '').strip() or None
    codlugar = request.POST.get('codlugar', '').strip()
    
    if not all([codespecializacion, nocaso, ninstancia, consecexpe]):
        return JsonResponse({'exito': False, 'mensaje': 'Claves compuestas incompletas'})
    
    if not codlugar:
        return JsonResponse({'exito': False, 'mensaje': 'Entidad requerida'})
    
    try:
        with connection.cursor() as cursor:
            # Actualizar expediente (solo campos editables: CEDULA, CODLUGAR)
            cursor.execute("""
                UPDATE EXPEDIENTE 
                SET CEDULA = :cedula, CODLUGAR = :codlugar
                WHERE CODESPECIALIZACION = :codespecializacion
                  AND NOCASO = :nocaso
                  AND NINSTANCIA = :ninstancia
                  AND CONSECEXPE = :consecexpe
            """, {
                'cedula': cedula,
                'codlugar': codlugar,
                'codespecializacion': codespecializacion,
                'nocaso': nocaso,
                'ninstancia': ninstancia,
                'consecexpe': consecexpe
            })

            # Guardar nuevos documentos si existen
            documentos_files = []
            for key in request.FILES:
                if key.startswith('documento'):
                    documentos_files.append(request.FILES[key])

            if documentos_files:
                fs = FileSystemStorage()
                cursor.execute("""
                    SELECT NVL(MAX(CONDOC), 0) 
                    FROM DOCUMENTO 
                    WHERE CODESPECIALIZACION = :codespecializacion
                      AND NOCASO = :nocaso
                      AND NINSTANCIA = :ninstancia
                      AND CONSECEXPE = :consecexpe
                """, {
                    'codespecializacion': codespecializacion,
                    'nocaso': nocaso,
                    'ninstancia': ninstancia,
                    'consecexpe': consecexpe
                })
                condoc = cursor.fetchone()[0] or 0
                
                for archivo in documentos_files:
                    condoc += 1
                    
                    # Shorten filename logic (same as create)
                    ext = archivo.name.split('.')[-1]
                    name_only = archivo.name.rsplit('.', 1)[0]
                    max_name_len = 30
                    if len(name_only) > max_name_len:
                        name_only = name_only[:max_name_len]
                    short_name = f"{name_only}.{ext}"
                    save_path = f'docs/C{nocaso}/{short_name}'
                    if len(save_path) > 50:
                        remaining = 50 - len(f'docs/C{nocaso}/') - len(ext) - 1
                        short_name = f"{name_only[:remaining]}.{ext}"
                        save_path = f'docs/C{nocaso}/{short_name}'

                    # Save the file
                    _ = fs.save(save_path, archivo)
                    
                    cursor.execute("""
                        INSERT INTO DOCUMENTO (CODESPECIALIZACION, NOCASO, NINSTANCIA, CONSECEXPE, CONDOC, NOMDOC, UBICADOC)
                        VALUES (:codespecializacion, :nocaso, :ninstancia, :consecexpe, :condoc, :nomdoc, :ubicadoc)
                    """, {
                        'codespecializacion': codespecializacion,
                        'nocaso': nocaso,
                        'ninstancia': ninstancia,
                        'consecexpe': consecexpe,
                        'condoc': condoc,
                        'nomdoc': short_name,
                        'ubicadoc': save_path  # Use controlled short path
                    })
        
        return JsonResponse({
            'exito': True,
            'mensaje': f'Expediente {consecexpe} actualizado exitosamente'
        })
    except Exception as e:
        return JsonResponse({'exito': False, 'mensaje': str(e)})


def guardar_suceso(request):
    """Guardar un suceso para un expediente"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Metodo no permitido'})
    
    # Recibir composite keys
    codespecializacion = request.POST.get('codespecializacion', '').strip()
    nocaso = request.POST.get('nocaso', '').strip()
    ninstancia = request.POST.get('ninstancia', '').strip()
    consecexpe = request.POST.get('consecexpe', '').strip()
    descsuceso = request.POST.get('descsuceso', '').strip()
    
    if not all([codespecializacion, nocaso, ninstancia, consecexpe, descsuceso]):
        return JsonResponse({'success': False, 'error': 'Datos incompletos'})
    
    try:
        with connection.cursor() as cursor:
            # Obtener siguiente consecutivo
            cursor.execute("""
                SELECT NVL(MAX(CONSUCESO), 0) + 1 
                FROM SUCESO 
                WHERE CODESPECIALIZACION = :codespecializacion
                  AND NOCASO = :nocaso
                  AND NINSTANCIA = :ninstancia
                  AND CONSECEXPE = :consecexpe
            """, {
                'codespecializacion': codespecializacion,
                'nocaso': nocaso,
                'ninstancia': ninstancia,
                'consecexpe': consecexpe
            })
            consuceso = cursor.fetchone()[0]
            
            cursor.execute("""
                INSERT INTO SUCESO (CODESPECIALIZACION, NOCASO, NINSTANCIA, CONSECEXPE, CONSUCESO, DESCSUCESO)
                VALUES (:codespecializacion, :nocaso, :ninstancia, :consecexpe, :consuceso, :descsuceso)
            """, {
                'codespecializacion': codespecializacion,
                'nocaso': nocaso,
                'ninstancia': ninstancia,
                'consecexpe': consecexpe,
                'consuceso': consuceso,
                'descsuceso': descsuceso
            })
        
        return JsonResponse({'success': True, 'mensaje': 'Suceso guardado exitosamente'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def guardar_resultado(request):
    """Guardar un resultado para un expediente"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Metodo no permitido'})
    
    # Recibir composite keys
    codespecializacion = request.POST.get('codespecializacion', '').strip()
    nocaso = request.POST.get('nocaso', '').strip()
    ninstancia = request.POST.get('ninstancia', '').strip()
    consecexpe = request.POST.get('consecexpe', '').strip()
    descresul = request.POST.get('descresul', '').strip()
    
    if not all([codespecializacion, nocaso, ninstancia, consecexpe, descresul]):
        return JsonResponse({'success': False, 'error': 'Datos incompletos'})
    
    try:
        with connection.cursor() as cursor:
            # Obtener siguiente consecutivo (CONSECRESUL)
            cursor.execute("""
                SELECT NVL(MAX(CONSECRESUL), 0) + 1 
                FROM RESULTADO 
                WHERE CODESPECIALIZACION = :codespecializacion
                  AND NOCASO = :nocaso
                  AND NINSTANCIA = :ninstancia
                  AND CONSECEXPE = :consecexpe
            """, {
                'codespecializacion': codespecializacion,
                'nocaso': nocaso,
                'ninstancia': ninstancia,
                'consecexpe': consecexpe
            })
            conresul = cursor.fetchone()[0]
            
            cursor.execute("""
                INSERT INTO RESULTADO (CODESPECIALIZACION, NOCASO, NINSTANCIA, CONSECEXPE, CONSECRESUL, DESCRESUL)
                VALUES (:codespecializacion, :nocaso, :ninstancia, :consecexpe, :conresul, :descresul)
            """, {
                'codespecializacion': codespecializacion,
                'nocaso': nocaso,
                'ninstancia': ninstancia,
                'consecexpe': consecexpe,
                'conresul': conresul,
                'descresul': descresul
            })
        
        return JsonResponse({'success': True, 'mensaje': 'Resultado guardado exitosamente'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def obtener_expediente_detalle(request):
    """Obtener detalle completo de un expediente usando composite primary keys"""
    codespecializacion = request.GET.get('codespecializacion', '').strip()
    nocaso = request.GET.get('nocaso', '').strip()
    ninstancia = request.GET.get('ninstancia', '').strip()
    consecexpe = request.GET.get('consecexpe', '').strip()
    
    if not all([codespecializacion, nocaso, ninstancia, consecexpe]):
        return JsonResponse({'success': False, 'error': 'Datos incompletos'})
    
    with connection.cursor() as cursor:
        # Datos del expediente
        cursor.execute("""
            SELECT ex.*, 
                   a.NOMBRE || ' ' || a.APELLIDO as ABOGADO_NOMBRE,
                   l.NOMLUGAR,
                   ep.NOMETAPA
            FROM EXPEDIENTE ex
            LEFT JOIN ABOGADO a ON ex.CEDULA = a.CEDULA
            LEFT JOIN LUGAR l ON ex.CODLUGAR = l.CODLUGAR
            LEFT JOIN ESPECIA_ETAPA ee ON ex.CODESPECIALIZACION = ee.CODESPECIALIZACION 
                                      AND ex.NINSTANCIA = ee.NINSTANCIA
            LEFT JOIN ETAPAPROCESAL ep ON ee.CODETAPA = ep.CODETAPA
            WHERE ex.CODESPECIALIZACION = :codespecializacion
              AND ex.NOCASO = :nocaso
              AND ex.NINSTANCIA = :ninstancia
              AND ex.CONSECEXPE = :consecexpe
        """, {
            'codespecializacion': codespecializacion,
            'nocaso': nocaso,
            'ninstancia': ninstancia,
            'consecexpe': consecexpe
        })
        expediente = dictfetchone(cursor)
        
        if not expediente:
            return JsonResponse({'success': False, 'error': 'Expediente no encontrado'})
        
        # Sucesos (usando composite PK)
        cursor.execute("""
            SELECT * FROM SUCESO 
            WHERE CODESPECIALIZACION = :codespecializacion
              AND NOCASO = :nocaso
              AND NINSTANCIA = :ninstancia
              AND CONSECEXPE = :consecexpe
            ORDER BY CONSUCESO
        """, {
            'codespecializacion': codespecializacion,
            'nocaso': nocaso,
            'ninstancia': ninstancia,
            'consecexpe': consecexpe
        })
        sucesos = dictfetchall(cursor)
        
        # Resultados (usando composite PK)
        cursor.execute("""
            SELECT * FROM RESULTADO 
            WHERE CODESPECIALIZACION = :codespecializacion
              AND NOCASO = :nocaso
              AND NINSTANCIA = :ninstancia
              AND CONSECEXPE = :consecexpe
            ORDER BY CONSECRESUL
        """, {
            'codespecializacion': codespecializacion,
            'nocaso': nocaso,
            'ninstancia': ninstancia,
            'consecexpe': consecexpe
        })
        resultados = dictfetchall(cursor)
        
        # Documentos (usando composite PK)
        cursor.execute("""
            SELECT * FROM DOCUMENTO 
            WHERE CODESPECIALIZACION = :codespecializacion
              AND NOCASO = :nocaso
              AND NINSTANCIA = :ninstancia
              AND CONSECEXPE = :consecexpe
            ORDER BY CONDOC
        """, {
            'codespecializacion': codespecializacion,
            'nocaso': nocaso,
            'ninstancia': ninstancia,
            'consecexpe': consecexpe
        })
        documentos = dictfetchall(cursor)
    
    return JsonResponse({
        'success': True,
        'expediente': expediente,
        'sucesos': sucesos,
        'resultados': resultados,
        'documentos': documentos
    })


def imprimir_caso(request):
    """Obtener datos completos del caso para impresion (maestro-detalle)"""
    nocaso = request.GET.get('nocaso', '').strip()
    
    if not nocaso:
        return JsonResponse({'success': False, 'error': 'Numero de caso requerido'})
    
    with connection.cursor() as cursor:
        # Datos del caso
        cursor.execute("""
            SELECT c.NOCASO, c.FECHAINICIO, c.FECHAFIN, c.VALOR,
                   e.NOMESPECIALIZACION, 
                   cl.NOMCLIENTE, cl.APELLCLIENTE, cl.NDOCUMENTO, t.DESCTIPODOC
            FROM CASO c
            JOIN ESPECIALIZACION e ON c.CODESPECIALIZACION = e.CODESPECIALIZACION
            JOIN CLIENTE cl ON c.CODCLIENTE = cl.CODCLIENTE
            LEFT JOIN TIPODOCUMENTO t ON cl.IDTIPODOC = t.IDTIPODOC
            WHERE c.NOCASO = :nocaso
        """, {'nocaso': nocaso})
        caso = dictfetchone(cursor)
        
        if not caso:
            return JsonResponse({'success': False, 'error': 'Caso no encontrado'})
        
        # Expedientes con detalles
        cursor.execute("""
            SELECT ex.CODESPECIALIZACION, ex.NOCASO, ex.NINSTANCIA, ex.CONSECEXPE,
                   TO_CHAR(ex.FECHAETAPA, 'YYYY-MM-DD') as FECHAETAPA,
                   a.NOMBRE || ' ' || a.APELLIDO as ABOGADO_NOMBRE,
                   l.NOMLUGAR,
                   ep.NOMETAPA
            FROM EXPEDIENTE ex
            LEFT JOIN ABOGADO a ON ex.CEDULA = a.CEDULA
            LEFT JOIN LUGAR l ON ex.CODLUGAR = l.CODLUGAR
            LEFT JOIN ESPECIA_ETAPA ee ON ex.CODESPECIALIZACION = ee.CODESPECIALIZACION 
                                      AND ex.NINSTANCIA = ee.NINSTANCIA
            LEFT JOIN ETAPAPROCESAL ep ON ee.CODETAPA = ep.CODETAPA
            WHERE ex.NOCASO = :nocaso
            ORDER BY ex.CONSECEXPE
        """, {'nocaso': nocaso})
        expedientes = dictfetchall(cursor)
        
        # Para cada expediente, obtener sucesos y resultados
        # OPTIMIZACION: Traer todos los sucesos y resultados del caso en una sola consulta por tipo
        # para evitar N+1 queries (Requerimiento 4.6)
        
        # Sucesos del caso
        cursor.execute("""
            SELECT CODESPECIALIZACION, NOCASO, NINSTANCIA, CONSECEXPE, CONSUCESO, DESCSUCESO 
            FROM SUCESO 
            WHERE NOCASO = :nocaso
            ORDER BY CODESPECIALIZACION, NINSTANCIA, CONSECEXPE, CONSUCESO
        """, {'nocaso': nocaso})
        all_sucesos = dictfetchall(cursor)

        # Resultados del caso
        cursor.execute("""
            SELECT CODESPECIALIZACION, NOCASO, NINSTANCIA, CONSECEXPE, CONSECRESUL, DESCRESUL 
            FROM RESULTADO 
            WHERE NOCASO = :nocaso
            ORDER BY CODESPECIALIZACION, NINSTANCIA, CONSECEXPE, CONSECRESUL
        """, {'nocaso': nocaso})
        all_resultados = dictfetchall(cursor)
        
        # Mapear a expedientes en memoria
        for exp in expedientes:
            exp['sucesos'] = [s for s in all_sucesos if 
                              s['CODESPECIALIZACION'] == exp['CODESPECIALIZACION'] and
                              s['NINSTANCIA'] == exp['NINSTANCIA'] and
                              s['CONSECEXPE'] == exp['CONSECEXPE']]
            exp['resultados'] = [r for r in all_resultados if 
                                 r['CODESPECIALIZACION'] == exp['CODESPECIALIZACION'] and
                                 r['NINSTANCIA'] == exp['NINSTANCIA'] and
                                 r['CONSECEXPE'] == exp['CONSECEXPE']]
    
    return render(request, 'clientes/imprimir_caso.html', {
        'caso': caso,
        'expedientes': expedientes
    })
