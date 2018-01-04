import pytest
from crispy_forms.layout import Button, HTML
from crispy_forms.helper import FormHelper
from crispy_forms_decorator import crispy, CrispyFormMixin


@pytest.mark.parametrize(
    argnames='decorator',
    argvalues=[
        crispy,
        crispy(),
        crispy(form_method='post')
    ],
    ids=[
        '@crispy - without braces',
        '@crispy() - with braces',
        '@crispy(form_action="post") - with braces and keyword arg'
    ]
)
def test_crispy_decorator_adds_a_crispy_form_mixin_base(form_class, decorator):
    assert not issubclass(form_class, CrispyFormMixin)
    assert issubclass(decorator(form_class), CrispyFormMixin)


def test_crispy_decorator_adds_a_helper_instance(form_class):
    assert not hasattr(form_class, '_crispy_handler')
    assert hasattr(crispy(form_class), '_crispy_handler')


def test_crispy_decorator_creates_a_helper_when_instancing_a_form(form_class):
    original_instance = form_class()
    crispy_instance = crispy(form_class)()

    assert not hasattr(original_instance, 'helper')
    assert isinstance(crispy_instance.helper, FormHelper)


def test_helper_instance_is_the_same(form_class):
    crispy_class = crispy(form_class)
    instance_a = crispy_class()
    instance_b = crispy_class()

    assert instance_a is not instance_b
    assert instance_a.helper is instance_b.helper


def test_decorator_respects_explicitly_given_helper(form_class):
    form_helper = FormHelper()

    crispy_class = crispy(helper=form_helper)(form_class)

    assert crispy_class().helper is form_helper


@pytest.mark.parametrize('k, v', [
    ('form_method', 'post'),
    ('form_action', '/cgi-bin/test.pl'),
    ('form_id', 'frm-test'),
    ('form_class', 'my-form-css'),
    ('form_group_wrapper_class', 'group'),
    ('form_tag', 'form'),
    ('form_error_title', 'Wrong!'),
    ('formset_error_title', 'There are errors here'),
    ('include_media', True),
    ('form_style', 'default'),
])
def test_decorator_passes_right_kwargs_to_helper_instance(form_class, k, v):
    form = crispy(**{k: v})(form_class)()

    # Dirty hack :)
    if k == 'form_style':
        assert form.helper.form_style == ''
    else:
        assert getattr(form.helper, k) == v


def test_extra_input(form_class):
    submit = Button
    html = HTML('or <a href="">cancel</a>')

    form = crispy(extra_inputs=[submit, html])(form_class)()

    assert all(
        (
            html in form.helper.inputs,
            submit in form.helper.inputs
        )
    )


def test_decorator_idempotency(form_class):
    assert not issubclass(form_class, CrispyFormMixin)
    assert issubclass(crispy(form_class), CrispyFormMixin)
    assert issubclass(crispy(crispy(form_class)), CrispyFormMixin)
