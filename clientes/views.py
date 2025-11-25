from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.db import connection
from .forms import ClienteForm

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0].lower() for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def registro_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            try:
                # Using Raw SQL for Insert
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO CLIENTE (CODCLIENTE, IDTIPODOC, NOMCLIENTE, APELLCLIENTE, NDOCUMENTO)
                        VALUES (%s, %s, %s, %s, %s)
                    """, [
                        form.cleaned_data['cod_cliente'], # Assuming form handles ID generation or input
                        form.cleaned_data['id_tipo_doc'].id_tipo_doc,
                        form.cleaned_data['nom_cliente'],
                        form.cleaned_data['apell_cliente'],
                        form.cleaned_data['n_documento']
                    ])
                messages.success(request, 'Cliente guardado exitosamente')
                return redirect('registro_cliente')
            except Exception as e:
                messages.error(request, f'Error al guardar: {str(e)}')
    else:
        form = ClienteForm()
            
    return render(request, 'clientes/registro_cliente.html', {'form': form})

def eliminar_cliente(request, cod_cliente):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM CLIENTE WHERE CODCLIENTE = %s", [cod_cliente])
            messages.success(request, 'Cliente eliminado exitosamente')
        except Exception as e:
            messages.error(request, f'Error al eliminar: {str(e)}')
    return redirect('registro_cliente')

# --- GESTION CASO ---

def gestion_caso(request):
    # Fetch Especializaciones using Raw SQL
    with connection.cursor() as cursor:
        cursor.execute("SELECT CODESPECIALIZACION, NOMESPECIALIZACION FROM ESPECIALIZACION")
        especializaciones = dictfetchall(cursor)
        
    return render(request, 'clientes/gestion_caso.html', {
        'especializaciones': especializaciones
    })

def buscar_cliente_api(request):
    nombre = request.GET.get('nombre', '').strip()
    apellido = request.GET.get('apellido', '').strip()
    
    if not nombre and not apellido:
        return JsonResponse([], safe=False)
    
    sql = "SELECT CODCLIENTE, NOMCLIENTE, APELLCLIENTE, NDOCUMENTO FROM CLIENTE WHERE 1=1"
    params = []
    
    if nombre:
        sql += " AND UPPER(NOMCLIENTE) LIKE UPPER(%s)"
        params.append(f'%{nombre}%')
    if apellido:
        sql += " AND UPPER(APELLCLIENTE) LIKE UPPER(%s)"
        params.append(f'%{apellido}%')
        
    sql += " FETCH FIRST 10 ROWS ONLY"
    
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        clientes = dictfetchall(cursor)
    
    return JsonResponse(clientes, safe=False)

def listar_casos_api(request):
    cliente_id = request.GET.get('cliente_id')
    if not cliente_id:
        return JsonResponse([], safe=False)
    
    # Join with Especializacion to get name
    sql = """
        SELECT c.NOCASO, c.FECHAINICIO, c.FECHAFIN, c.VALOR, e.NOMESPECIALIZACION as ESPECIALIZACION
        FROM CASO c
        JOIN ESPECIALIZACION e ON c.CODESPECIALIZACION = e.CODESPECIALIZACION
        WHERE c.CODCLIENTE = %s
        ORDER BY c.FECHAINICIO DESC
    """
    
    with connection.cursor() as cursor:
        cursor.execute(sql, [cliente_id])
        casos = dictfetchall(cursor)
        
    return JsonResponse(casos, safe=False)

def crear_caso(request):
    if request.method == 'POST':
        try:
            cod_cliente = request.POST.get('cod_cliente')
            cod_especializacion = request.POST.get('cod_especializacion')
            fecha_inicio = request.POST.get('fecha_inicio')
            valor = request.POST.get('valor')
            
            with connection.cursor() as cursor:
                # Calculate next ID manually
                cursor.execute("SELECT NVL(MAX(NOCASO), 0) + 1 FROM CASO")
                next_id = cursor.fetchone()[0]
                
                cursor.execute("""
                    INSERT INTO CASO (NOCASO, CODCLIENTE, CODESPECIALIZACION, FECHAINICIO, VALOR)
                    VALUES (%s, %s, %s, TO_DATE(%s, 'YYYY-MM-DD'), %s)
                """, [next_id, cod_cliente, cod_especializacion, fecha_inicio, valor])
                
            messages.success(request, f'Caso #{next_id} creado exitosamente')
        except Exception as e:
            messages.error(request, f'Error al crear caso: {str(e)}')
            
    return redirect('gestion_caso')

# --- GESTION EXPEDIENTE ---

def gestion_expediente(request):
    caso_id = request.GET.get('caso_id')
    context = {}
    
    if caso_id:
        try:
            with connection.cursor() as cursor:
                # Get Case Info
                cursor.execute("""
                    SELECT c.NOCASO, c.FECHAFIN, c.CODESPECIALIZACION, 
                           cl.NOMCLIENTE, cl.APELLCLIENTE, 
                           e.NOMESPECIALIZACION
                    FROM CASO c
                    JOIN CLIENTE cl ON c.CODCLIENTE = cl.CODCLIENTE
                    JOIN ESPECIALIZACION e ON c.CODESPECIALIZACION = e.CODESPECIALIZACION
                    WHERE c.NOCASO = %s
                """, [caso_id])
                caso = dictfetchall(cursor)
                
                if not caso:
                    messages.error(request, 'Caso no encontrado')
                    return render(request, 'clientes/gestion_expediente.html', context)
                
                context['caso'] = caso[0]
                caso_data = caso[0]
                
                # Get Expediente History with Stage Names
                # We join Expediente -> EspeciaEtapa -> EtapaProcesal
                # Note: PASOETAPA stores ID_ESPECIA_ETAPA
                sql_exp = """
                    SELECT ex.CONSECEXPE, ex.NINSTANCIA, ex.FECHAETAPA, 
                           l.NOMLUGAR, 
                           a.NOMBRE || ' ' || a.APELLIDO as ABOGADO_NOMBRE,
                           ep.NOMETAPA as ETAPA_NOMBRE,
                           ep.ORDEN as ETAPA_ORDEN,
                           d.UBICADOC
                    FROM EXPEDIENTE ex
                    JOIN LUGAR l ON ex.CODLUGAR = l.CODLUGAR
                    LEFT JOIN ABOGADO a ON ex.CEDULA = a.CEDULA
                    LEFT JOIN ESPECIA_ETAPA ee ON ex.PASOETAPA = ee.ID_ESPECIA_ETAPA
                    LEFT JOIN ETAPAPROCESAL ep ON ee.CODETAPA = ep.CODETAPA
                    LEFT JOIN DOCUMENTO d ON ex.ID_EXPEDIENTE = d.ID_EXPEDIENTE
                    WHERE ex.NOCASO = %s
                    ORDER BY ex.CONSECEXPE
                """
                cursor.execute(sql_exp, [caso_id])
                expedientes = dictfetchall(cursor)
                context['expedientes'] = expedientes
                
                # Determine Next Stage
                current_max_order = 0
                for exp in expedientes:
                    if exp['etapa_orden'] and exp['etapa_orden'] > current_max_order:
                        current_max_order = exp['etapa_orden']
                
                next_order = current_max_order + 1
                
                # Get Available Next Stages
                sql_next = """
                    SELECT ee.ID_ESPECIA_ETAPA, ep.NOMETAPA, ee.NINSTANCIA
                    FROM ESPECIA_ETAPA ee
                    JOIN ETAPAPROCESAL ep ON ee.CODETAPA = ep.CODETAPA
                    WHERE ee.CODESPECIALIZACION = %s
                    AND ep.ORDEN = %s
                    ORDER BY ee.NINSTANCIA, ep.NOMETAPA
                """
                cursor.execute(sql_next, [caso_data['codespecializacion'], next_order])
                etapas_disponibles = dictfetchall(cursor)
                context['etapas_disponibles'] = etapas_disponibles
                
                # Load Lists for Modal
                cursor.execute("SELECT CEDULA, NOMBRE, APELLIDO FROM ABOGADO")
                context['abogados'] = dictfetchall(cursor)
                
                cursor.execute("SELECT CODLUGAR, NOMLUGAR FROM LUGAR")
                context['lugares'] = dictfetchall(cursor)
                
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            
    return render(request, 'clientes/gestion_expediente.html', context)

def crear_etapa(request):
    if request.method == 'POST':
        try:
            caso_id = request.POST.get('caso_id')
            id_especia_etapa = request.POST.get('id_especia_etapa')
            cedula = request.POST.get('cedula')
            cod_lugar = request.POST.get('cod_lugar')
            fecha_etapa = request.POST.get('fecha_etapa')
            desc_suceso = request.POST.get('desc_suceso')
            
            with connection.cursor() as cursor:
                # Get Case Info for Specialization
                cursor.execute("SELECT CODESPECIALIZACION FROM CASO WHERE NOCASO = %s", [caso_id])
                row = cursor.fetchone()
                if not row:
                    raise Exception("Caso no encontrado")
                cod_especializacion = row[0]
                
                # Get EspeciaEtapa Info
                cursor.execute("SELECT NINSTANCIA FROM ESPECIA_ETAPA WHERE ID_ESPECIA_ETAPA = %s", [id_especia_etapa])
                row = cursor.fetchone()
                if not row:
                    raise Exception("Etapa no valida")
                n_instancia = row[0]
                
                # Calculate Next Consec
                cursor.execute("SELECT NVL(MAX(CONSECEXPE), 0) + 1 FROM EXPEDIENTE WHERE NOCASO = %s", [caso_id])
                next_consec = cursor.fetchone()[0]
                
                # Insert Expediente (Using RETURNING INTO equivalent or just separate Insert)
                # Oracle supports RETURNING ID INTO :out_param, but Django cursor might be simpler with standard insert and fetch back if needed.
                # Since we have surrogate ID_EXPEDIENTE, we let DB handle it.
                # But we need the ID for Documento/Suceso.
                # We can use `cursor.execute("INSERT ... RETURNING ID_EXPEDIENTE INTO :id", ...)` with `cursor.var`.
                
                id_expediente_var = cursor.var(int)
                cursor.execute("""
                    INSERT INTO EXPEDIENTE (NOCASO, CODESPECIALIZACION, NINSTANCIA, CONSECEXPE, CEDULA, CODLUGAR, FECHAETAPA, PASOETAPA)
                    VALUES (%s, %s, %s, %s, %s, %s, TO_DATE(%s, 'YYYY-MM-DD'), %s)
                    RETURNING ID_EXPEDIENTE INTO :id_exp
                """, [caso_id, cod_especializacion, n_instancia, next_consec, cedula, cod_lugar, fecha_etapa, id_especia_etapa, id_expediente_var])
                
                id_expediente = id_expediente_var.getvalue()[0]
                
                # Insert Documento
                if request.FILES.get('documento'):
                    cursor.execute("""
                        INSERT INTO DOCUMENTO (ID_EXPEDIENTE, CONDOC, UBICADOC)
                        VALUES (%s, 1, %s)
                    """, [id_expediente, request.FILES['documento'].name])
                
                # Insert Suceso
                if desc_suceso:
                    cursor.execute("""
                        INSERT INTO SUCESO (ID_EXPEDIENTE, CONSUCESO, DESCSUCESO)
                        VALUES (%s, 1, %s)
                    """, [id_expediente, desc_suceso])
                
            messages.success(request, 'Etapa registrada exitosamente')
            
        except Exception as e:
            messages.error(request, f'Error al registrar etapa: {str(e)}')
            
    return redirect(f'/clientes/gestion_expediente/?caso_id={caso_id}')
