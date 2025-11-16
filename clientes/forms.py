from django import forms
from .models import Cliente, TipoDocumento


class ClienteForm(forms.ModelForm):
    """
    Formulario para el registro de clientes
    """
    class Meta:
        model = Cliente
        fields = ['codCliente', 'nomCliente', 'apellCliente', 'idTipoDoc', 'nDocumento']
        widgets = {
            'codCliente': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '5',
                'placeholder': 'Ej: 00001'
            }),
            'nomCliente': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '30',
                'placeholder': 'Nombre del cliente'
            }),
            'apellCliente': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '30',
                'placeholder': 'Apellido del cliente'
            }),
            'idTipoDoc': forms.Select(attrs={
                'class': 'form-select'
            }),
            'nDocumento': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '15',
                'placeholder': 'Número de documento'
            }),
        }
        labels = {
            'codCliente': 'Código Cliente',
            'nomCliente': 'Nombre',
            'apellCliente': 'Apellido',
            'idTipoDoc': 'Tipo Documento',
            'nDocumento': 'Número Documento',
        }
