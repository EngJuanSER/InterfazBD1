from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.db import IntegrityError
from .models import Cliente, TipoDocumento
from .forms import ClienteForm


def registro_cliente(request):
    """
    Vista principal para el registro de clientes
    """
    if request.method == 'POST':
        # Obtener el ID del cliente si existe (para actualización)
        cliente_id = request.POST.get('cliente_id', '').strip()
        
        # Intentar obtener el cliente existente por ID
        if cliente_id:
            try:
                cliente_existente = Cliente.objects.get(cliente_id=cliente_id)
                # Si existe, usar el formulario en modo edición
                form = ClienteForm(request.POST, instance=cliente_existente)
                es_actualizacion = True
            except Cliente.DoesNotExist:
                # Si el ID no existe, crear uno nuevo
                form = ClienteForm(request.POST)
                es_actualizacion = False
        else:
            # Si no hay ID, crear uno nuevo
            form = ClienteForm(request.POST)
            es_actualizacion = False
        
        if form.is_valid():
            try:
                cliente = form.save()
                nombre_completo = f"{form.cleaned_data['nombre_cliente']} {form.cleaned_data['apellido_cliente']}"
                if es_actualizacion:
                    messages.success(request, f'✓ Cliente "{nombre_completo}" (ID: {cliente.cliente_id}) actualizado exitosamente')
                else:
                    messages.success(request, f'✓ Cliente "{nombre_completo}" guardado exitosamente con ID: {cliente.cliente_id}')
                return redirect('registro_cliente')
            except IntegrityError as e:
                error_msg = str(e).lower()
                if 'unique constraint' in error_msg or 'ak_documento_unico_cliente' in error_msg:
                    n_documento = request.POST.get('n_documento_cliente', '')
                    messages.error(request, f'❌ Error: Ya existe un cliente con el documento "{n_documento}"')
                    form.add_error('n_documento_cliente', 'Este documento ya está registrado')
                elif 'fk_cliente' in error_msg:
                    messages.error(request, '❌ Error: El tipo de documento seleccionado no es válido')
                else:
                    messages.error(request, f'❌ Error de integridad en la base de datos: {str(e)}')
            except Exception as e:
                messages.error(request, f'❌ Error al guardar: {str(e)}')
        else:
            # Mostrar errores específicos de cada campo
            error_messages = []
            for field, errors in form.errors.items():
                if field == '__all__':
                    error_messages.extend(errors)
                else:
                    field_label = form.fields[field].label or field
                    for error in errors:
                        error_messages.append(f"{field_label}: {error}")
            
            messages.error(request, '❌ Por favor corrija los siguientes errores:')
            for error_msg in error_messages:
                messages.warning(request, f"• {error_msg}")
    else:
        form = ClienteForm()
    
    tipos_documento = TipoDocumento.objects.all()
    return render(request, 'clientes/registro_cliente.html', {
        'form': form,
        'tipos_documento': tipos_documento
    })


def buscar_cliente(request):
    """
    Vista AJAX para buscar un cliente por ID (llave primaria)
    """
    cliente_id = request.GET.get('id', '').strip()
    
    if not cliente_id:
        return JsonResponse({'existe': False, 'error': 'ID vacío'})
    
    try:
        cliente = Cliente.objects.get(cliente_id=cliente_id)
        data = {
            'existe': True,
            'cliente_id': cliente.cliente_id,
            'nombre_cliente': cliente.nombre_cliente,
            'apellido_cliente': cliente.apellido_cliente,
            'id_tipo_doc': cliente.id_tipo_doc.id_tipo_doc,
            'n_documento_cliente': cliente.n_documento_cliente,
            'direccion_notificacion': cliente.direccion_notificacion or '',
            'fecha_nacimiento': cliente.fecha_nacimiento.isoformat() if cliente.fecha_nacimiento else '',
            'observaciones': cliente.observaciones or '',
        }
    except Cliente.DoesNotExist:
        data = {'existe': False, 'mensaje': 'Cliente no encontrado'}
    except Exception as e:
        data = {'existe': False, 'error': str(e)}
    
    return JsonResponse(data)


def eliminar_cliente(request):
    """
    Vista AJAX para eliminar un cliente por ID (llave primaria)
    """
    if request.method == 'POST':
        cliente_id = request.POST.get('id', '').strip()
        
        if not cliente_id:
            return JsonResponse({'success': False, 'error': 'ID vacío'})
        
        try:
            cliente = Cliente.objects.get(cliente_id=cliente_id)
            nombre_completo = f"{cliente.nombre_cliente} {cliente.apellido_cliente}"
            cliente.delete()
            return JsonResponse({
                'success': True, 
                'mensaje': f'Cliente "{nombre_completo}" (ID: {cliente_id}) eliminado exitosamente'
            })
        except Cliente.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Cliente no encontrado'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Error al eliminar: {str(e)}'})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

