import pytest
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Field, Fieldset, Layout
from django.template import Context, Template

from crispy_forms_decorator import CrispyFormMixin


def render(form):
    return Template(
        '{% load crispy_forms_tags %}{% crispy form %}'
    ).render(Context({'form': form}))


@pytest.mark.parametrize(
    argnames='fieldsets',
    argvalues=[
        (
            ('Name', ['name']),
            ('Age', ['age'])
        ),
        (
            ('Name', ['name']),
            Fieldset('Age', 'age'),
        ),
        (
            ('Name', [Field('name')]),
            ('Age', ['age'])
        )
    ],
    ids=[
        'Both fieldsets are given as 2-tuple of strings',
        'One of fieldsets is a Fieldset instance',
        'One of fields in the fieldset is a Field instance',
    ]
)
def test_defined_fieldsets(form_class, fieldsets):
    class Form(CrispyFormMixin, form_class):
        def get_fieldsets(self):
            return fieldsets

    html = render(Form())

    assert all(
        (
            '<legend>Name</legend>' in html,
            '<legend>Age</legend>' in html
        )
    )


@pytest.mark.parametrize(
    argnames='name_field',
    argvalues=[
        'name',
        Field('name'),
        Layout(
            HTML('My field'),
            Field('name'),
        ),
    ],
    ids=[
        'A regular string given',
        'A Field instance given',
        'A set of items (i.e. Layout instance) given',
    ]
)
def test_customized_field_render(form_class, name_field):
    class Form(CrispyFormMixin, form_class):
        def render_name_field(self):
            return name_field

    html = render(Form())

    assert all(
        (
            'id_name' in html,
            'id_age' in html,
        )
    )


def test_mixin_respects_explicitly_given_helper(form_class):
    helper_instance = FormHelper()

    class Form(CrispyFormMixin, form_class):
        helper = helper_instance

    form = Form()

    assert form.helper == helper_instance
