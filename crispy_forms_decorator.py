from crispy_forms.layout import Layout, Fieldset, Field
from crispy_forms.helper import FormHelper


__all__ = ['CrispyFormMixin', 'crispy']
__version__ = '0.1.0'


PASSED_PARAMS = [
    'form_method', 'form_action', 'form_id', 'form_class',
    'form_group_wrapper_class',
    'form_tag', 'form_error_title',
    'formset_error_title',
    'form_style',
    'include_media'
]


class CrispyFormMixin(object):
    _crispy_handler = None  # type: FormHelper

    def __init__(self, *args, **kwargs):
        super(CrispyFormMixin, self).__init__(*args, **kwargs)

        if not hasattr(self, 'helper'):
            if self._crispy_handler is not None:
                self.helper = self._crispy_handler
            else:
                self.helper = FormHelper()

        if self.helper.layout is None:
            self.helper.layout = self.get_layout()

    def get_layout(self):
        fieldsets = self.get_fieldsets()

        if not fieldsets:
            return Layout(*[self.normalize_field(f)
                            for f in self.fields.keys()])
        else:
            bits = []
            for fieldset in fieldsets:
                if isinstance(fieldset, Fieldset):
                    bits.append(fieldset)
                if isinstance(fieldset, tuple):
                    legend, fields = fieldset
                    fieldset = Fieldset(legend, *[
                        self.normalize_field(f)
                        for f in fields
                    ])
                    bits.append(fieldset)
            return Layout(*bits)

    def get_fieldsets(self):
        return []

    def normalize_field(self, field):
        field_handler_name = 'render_{}_field'.format(field)
        field_handler = getattr(self, field_handler_name, None)
        if field_handler is not None:
            return field_handler()
        return field if isinstance(field, Field) else Field(field)


def crispy(*args, **kwargs):
    form_cls = None

    if len(args) == 1 and callable(args[0]):
        form_cls = args[0]

    try:
        crispy_helper = kwargs['helper']
        assert isinstance(crispy_helper, FormHelper)
    except (KeyError, AssertionError):
        crispy_helper = FormHelper()

    extra_inputs = kwargs.pop('extra_inputs', None)

    if extra_inputs:
        for ei in extra_inputs:
            crispy_helper.add_input(ei)

    for k in PASSED_PARAMS:
        if k not in kwargs:
            continue
        setattr(crispy_helper, k, kwargs[k])

    def inner(form_cls):
        if not issubclass(form_cls, CrispyFormMixin):
            form_cls.__bases__ = (CrispyFormMixin, ) + form_cls.__bases__
        form_cls._crispy_handler = crispy_helper
        return form_cls

    return inner(form_cls) if form_cls else inner
