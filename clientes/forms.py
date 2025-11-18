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
    
    def clean_codCliente(self):
        """
        Validar que el código de cliente no exista (solo para nuevos registros)
        """
        codigo = self.cleaned_data.get('codCliente')
        if codigo:
            # Solo validar si es un nuevo registro (no una edición)
            if self.instance.pk:
                # Es una edición, el código es el mismo del registro actual
                return codigo
            else:
                # Es un nuevo registro, verificar que no exista
                if Cliente.objects.filter(codCliente=codigo).exists():
                    raise forms.ValidationError(
                        f'Ya existe un cliente con el código "{codigo}". Por favor use otro código.'
                    )
        return codigo
    
    def clean_nDocumento(self):
        """
        Validar el número de documento
        """
        documento = self.cleaned_data.get('nDocumento')
        if documento:
            # Eliminar espacios en blanco
            documento = documento.strip()
            if not documento:
                raise forms.ValidationError('El número de documento no puede estar vacío.')
        return documento
    
    def clean(self):
        """
        Validaciones adicionales del formulario completo
        """
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nomCliente')
        apellido = cleaned_data.get('apellCliente')
        
        # Validar que nombre y apellido no sean solo espacios
        if nombre and not nombre.strip():
            self.add_error('nomCliente', 'El nombre no puede estar vacío.')
        
        if apellido and not apellido.strip():
            self.add_error('apellCliente', 'El apellido no puede estar vacío.')
        
        return cleaned_data
