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
        # Obtener el código del cliente
        codigo_cliente = request.POST.get('codCliente', '').strip()
        
        # Intentar obtener el cliente existente
        try:
            cliente_existente = Cliente.objects.get(codCliente=codigo_cliente)
            # Si existe, usar el formulario en modo edición
            form = ClienteForm(request.POST, instance=cliente_existente)
            es_actualizacion = True
        except Cliente.DoesNotExist:
            # Si no existe, crear uno nuevo
            form = ClienteForm(request.POST)
            es_actualizacion = False
        
        if form.is_valid():
            try:
                form.save()
                if es_actualizacion:
                    messages.success(request, f'✓ Cliente "{codigo_cliente}" actualizado exitosamente')
                else:
                    messages.success(request, f'✓ Cliente "{codigo_cliente}" guardado exitosamente')
                return redirect('registro_cliente')
            except IntegrityError as e:
                error_msg = str(e).lower()
                if 'unique constraint' in error_msg or 'pk_cliente' in error_msg:
                    messages.error(request, f'❌ Error: Ya existe un cliente con el código "{form.cleaned_data["codCliente"]}"')
                    form.add_error('codCliente', 'Este código ya está registrado')
                elif 'fk_cliente_tipodoc' in error_msg:
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
    Vista AJAX para buscar un cliente por código
    """
    codigo = request.GET.get('codigo', '').strip()
    
    if not codigo:
        return JsonResponse({'existe': False, 'error': 'Código vacío'})
    
    try:
        cliente = Cliente.objects.get(codCliente=codigo)
        data = {
            'existe': True,
            'nomCliente': cliente.nomCliente,
            'apellCliente': cliente.apellCliente,
            'idTipoDoc': cliente.idTipoDoc.idTipoDoc,
            'nDocumento': cliente.nDocumento,
        }
    except Cliente.DoesNotExist:
        data = {'existe': False, 'mensaje': 'Cliente no encontrado'}
    except Exception as e:
        data = {'existe': False, 'error': str(e)}
    
    return JsonResponse(data)


def eliminar_cliente(request):
    """
    Vista AJAX para eliminar un cliente por código
    """
    if request.method == 'POST':
        codigo = request.POST.get('codigo', '').strip()
        
        if not codigo:
            return JsonResponse({'success': False, 'error': 'Código vacío'})
        
        try:
            cliente = Cliente.objects.get(codCliente=codigo)
            nombre_completo = f"{cliente.nomCliente} {cliente.apellCliente}"
            cliente.delete()
            return JsonResponse({
                'success': True, 
                'mensaje': f'Cliente "{codigo}" - {nombre_completo} eliminado exitosamente'
            })
        except Cliente.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Cliente no encontrado'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Error al eliminar: {str(e)}'})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

