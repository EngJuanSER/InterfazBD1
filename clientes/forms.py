from django import forms
from .models import Cliente, TipoDocumento


class ClienteForm(forms.ModelForm):
    """
    Formulario para el registro de clientes
    """
    class Meta:
        model = Cliente
        fields = ['nombre_cliente', 'apellido_cliente', 'id_tipo_doc', 'n_documento_cliente', 
                  'direccion_notificacion', 'fecha_nacimiento', 'observaciones']
        widgets = {
            'nombre_cliente': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '100',
                'placeholder': 'Nombre del cliente'
            }),
            'apellido_cliente': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '100',
                'placeholder': 'Apellido del cliente'
            }),
            'id_tipo_doc': forms.Select(attrs={
                'class': 'form-select'
            }),
            'n_documento_cliente': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '15',
                'placeholder': 'Número de documento'
            }),
            'direccion_notificacion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Dirección de notificación'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones adicionales'
            }),
        }
        labels = {
            'nombre_cliente': 'Nombre',
            'apellido_cliente': 'Apellido',
            'id_tipo_doc': 'Tipo Documento',
            'n_documento_cliente': 'Número Documento',
            'direccion_notificacion': 'Dirección de Notificación',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'observaciones': 'Observaciones',
        }
    
    def clean_n_documento_cliente(self):
        """
        Validar que el número de documento no exista (solo para nuevos registros)
        """
        documento = self.cleaned_data.get('n_documento_cliente')
        if documento:
            documento = documento.strip()
            if not documento:
                raise forms.ValidationError('El número de documento no puede estar vacío.')
            
            # Solo validar si es un nuevo registro (no una edición)
            if self.instance.pk:
                # Es una edición, verificar si cambió el documento
                if self.instance.n_documento_cliente != documento:
                    if Cliente.objects.filter(n_documento_cliente=documento).exists():
                        raise forms.ValidationError(
                            f'Ya existe un cliente con el documento "{documento}".'
                        )
            else:
                # Es un nuevo registro, verificar que no exista
                if Cliente.objects.filter(n_documento_cliente=documento).exists():
                    raise forms.ValidationError(
                        f'Ya existe un cliente con el documento "{documento}".'
                    )
        return documento
    
    def clean(self):
        """
        Validaciones adicionales del formulario completo
        """
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre_cliente')
        apellido = cleaned_data.get('apellido_cliente')
        
        # Validar que nombre y apellido no sean solo espacios
        if nombre and not nombre.strip():
            self.add_error('nombre_cliente', 'El nombre no puede estar vacío.')
        
        if apellido and not apellido.strip():
            self.add_error('apellido_cliente', 'El apellido no puede estar vacío.')
        
        return cleaned_data
