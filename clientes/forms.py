from django import forms
from .models import Cliente, TipoDocumento


class ClienteForm(forms.ModelForm):
    """
    Formulario para el registro de clientes
    """
    class Meta:
        model = Cliente
        fields = ['nom_cliente', 'apell_cliente', 'id_tipo_doc', 'n_documento']
        widgets = {
            'nom_cliente': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '30',
                'placeholder': 'Nombre del cliente'
            }),
            'apell_cliente': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '30',
                'placeholder': 'Apellido del cliente'
            }),
            'id_tipo_doc': forms.Select(attrs={
                'class': 'form-select'
            }),
            'n_documento': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '15',
                'placeholder': 'Número de documento'
            }),
        }
        labels = {
            'nom_cliente': 'Nombre',
            'apell_cliente': 'Apellido',
            'id_tipo_doc': 'Tipo Documento',
            'n_documento': 'Número Documento',
        }
    
    def clean_n_documento(self):
        """
        Validar que el número de documento no exista (solo para nuevos registros)
        """
        documento = self.cleaned_data.get('n_documento')
        if documento:
            documento = documento.strip()
            if not documento:
                raise forms.ValidationError('El número de documento no puede estar vacío.')
            
            # Solo validar si es un nuevo registro (no una edición)
            if self.instance.pk:
                # Es una edición, verificar si cambió el documento
                if self.instance.n_documento != documento:
                    if Cliente.objects.filter(n_documento=documento).exists():
                        raise forms.ValidationError(
                            f'Ya existe un cliente con el documento "{documento}".'
                        )
            else:
                # Es un nuevo registro, verificar que no exista
                if Cliente.objects.filter(n_documento=documento).exists():
                    raise forms.ValidationError(
                        f'Ya existe un cliente con el documento "{documento}".'
                    )
        return documento
    
    def clean(self):
        """
        Validaciones adicionales del formulario completo
        """
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nom_cliente')
        apellido = cleaned_data.get('apell_cliente')
        
        # Validar que nombre y apellido no sean solo espacios
        if nombre and not nombre.strip():
            self.add_error('nom_cliente', 'El nombre no puede estar vacío.')
        
        if apellido and not apellido.strip():
            self.add_error('apell_cliente', 'El apellido no puede estar vacío.')
        
        return cleaned_data
