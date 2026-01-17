from wagtail.contrib.forms.forms import FormBuilder

class PlaceholderFormBuilder(FormBuilder):
    def get_formfield(self, field):
        formfield = super().get_formfield(field)
        if field.help_text:
            formfield.widget.attrs['placeholder'] = field.help_text
            formfield.help_text = ''
        formfield.widget.attrs['class'] = 'onovo-input'
        return formfield
