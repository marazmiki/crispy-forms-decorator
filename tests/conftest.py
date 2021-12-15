import django
import pytest
from django import forms
from django.conf import settings


def pytest_configure():
    settings.configure(
        INSTALLED_APPS=['crispy_forms'],
        LOGGING_CONFIG={},
        ROOT_URLCONF=[],
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
            }
        ],
    )
    django.setup()


@pytest.fixture
def form_class():
    "Just a form class used in all (well, almost all) the test cases"
    class Form(forms.Form):
        name = forms.CharField(label='Name')
        age = forms.IntegerField(label='Age')
    return Form
