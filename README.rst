######################
crispy-forms-decorator
######################

A syntax sugar for `django-crispy-forms <https://github.com/django-crispy-forms/django-crispy-forms>`_ that allows simplifying form creation with ``@crispy`` decorator


What is it?
###########

It's a small decorator who trying to make dealing with ``django-crispy-forms`` smooth. What does it mean: the
decorator just implicitly creates a ``helper`` instance and allow to interact with it outside of class methods.

Look at the approach that recommended by official documentation:

.. code:: python

    from crispy_forms.helper import FormHelper
    from crispy_forms.layout import Submit

    class ExampleForm(forms.Form):
        [...]
        def __init__(self, *args, **kwargs):
            super(ExampleForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_id = 'id-exampleForm'
            self.helper.form_class = 'blueForms'
            self.helper.form_method = 'post'
            self.helper.form_action = 'submit_survey'

            self.helper.add_input(Submit('submit', 'Submit'))

And how we can shrink the code by using a simple decorator:

.. code:: python

    from crispy_forms.layout import Submit
    from crispy_forms_decorator import crispy

    @crispy(form_id='id-exampleForm',
            form_class ='blueForms',
            form_method='post',
            form_action='submit_survey',
            extra_inputs=[
                Submit('submit', 'Submit')
            ])
    class ExampleForm(forms.Form):
        # [...]

For me, it's quite cool :)


Installing
##########


.. code:: bash

    $ pip install crispy-forms-decorator


Usage
#####

Basics
======

In the simplest case, you can just decorate your form class without any arguments.

.. code:: python

    from django import forms
    from crispy_forms_decorator import crispy

    @crispy
    class ExampleForm(forms.Form):
        name = forms.CharField(label='Your name')

That's all. Also, an object is created when ``crispy`` calling, also could be a decorator:

.. code:: python

    @crispy()
    class ExampleForm(forms.Form):
        # ...

it would work as expected.


Arguments
=========

You free to customize your class via passing some keyword arguments to a decorator like that:

.. code:: python

    @crispy(ham='spam', spam='egg')
    class ExampleForm(forms.Form):
        # ...


Note, all of them are optional.

``helper``
  Actually, the decorator takes carry about ``helper`` creation, but
  you might want to use the same one in some classes (but for what? :thinking:)

.. code:: python

    existing_helper = FormHelper()

    @crispy(helper=existing_helper)
    class ExampleForm(forms.Form):
        # ...


``extra_inputs``
  Allows adding some fields to layout outside of any class method.

.. code:: python

    @crispy(extra_inputs=[
        Submit('submit', 'Register'),
        HTML('or'),
        Button('reset', 'Cancel'),
    ])
    class ExampleForm(forms.Form):
        # ...

Other methods are taken from the ``django-crispy-form`` sources. Here are:

* ``form_method``
* ``form_action``
* ``form_id``
* ``form_class``
* ``form_group_wrapper_class``
* ``form_tag``
* ``form_error_title``
* ``formset_error_title``
* ``form_style``
* ``include_media``


Fieldsets
=========

If you should use fieldsets, also no need override the class constructor.

.. code:: python
    from crispy_forms.layout import Fieldset

    @crispy
    class Form(forms.Form):
        first_name = forms.CharField(label='First name')
        last_name = forms.CharField(label='Last name')
        phone = forms.CharField()
        email = forms.EmailField()

        def get_fieldsets(self):
            return (
                ('Personal data', ['first_name', 'last_name']),
                Fieldset('Contacts', 'phone', 'email')
            )

The ``get_fieldsets()`` method should return a list or a tuple of fieldsets,
where each of one should be:

* A 2-tuple of ``('Legend', ['list', 'of', 'fields', 'in', 'the', 'fieldset'])``. If you not need in a fieldset legend, you can pass ``None`` in a first item in the tuple. Each field can be either string or a ``Field`` instance from the ``crispy_forms.layout`` module.
* A ``Fieldset("list", "of", "fields")`` object from the ``crispy_forms.layout`` module


Custom field rendering
======================

You can define a ``render_FIELDNAME_field()`` method (like a clean_* methods approach came from Django) to make
crispy render the field as you want

.. code:: python

    @crispy
    class Form(forms.Form):
        first_name = forms.CharField(label='First name')

        def render_first_name_field(self):
            return HTML('Oops, where is our first name?')

