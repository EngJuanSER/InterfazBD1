from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Cliente, TipoDocumento
from .forms import ClienteForm


def registro_cliente(request):
    """
    Vista principal para el registro de clientes
    """
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Cliente guardado exitosamente')
                return redirect('registro_cliente')
            except Exception as e:
                messages.error(request, f'Error al guardar: {str(e)}')
        else:
            messages.error(request, 'Por favor corrija los errores en el formulario')
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

