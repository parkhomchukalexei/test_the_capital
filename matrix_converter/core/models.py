from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import fields



class MatrixField(models.Field):
    description = "Matrix field"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255
        kwargs['editable'] = False
        super().__init__(*args, **kwargs)

    def deconstruct(self):
       name, path, args, kwargs = super().deconstruct()
       del kwargs['max_length']
       del kwargs['editable']
       return name, path, args, kwargs

    def to_python(self, value):
        if value is None:
            return value

        if isinstance(value, str):
            try:
                rows = value.strip().split('\n')
                matrix = [list(map(int, row.strip().split('|'))) for row in rows]
                return matrix
            except ValueError:
                raise ValidationError('Invalid matrix format')
        elif isinstance(value, list):
            return value
        else:
            raise ValidationError('Invalid matrix format')

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def db_type(self, connection):
        return 'text'

    def get_prep_value(self, value):
       if value is None:
           return None

       return '\n'.join('|'.join(map(str, row)) for row in value)

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        if not isinstance(value, list):
            raise ValidationError('Value must be a list')
        if not all(isinstance(row, list) for row in value):
            raise ValidationError('Each row must be a list')
        if not all(len(row) == len(value[0]) for row in value):
            raise ValidationError('All rows must have the same length')

    def formfield(self, **kwargs):
        return None

fields.MatrixField = MatrixField

class Matrix(models.Model):

    matrix_field = MatrixField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.date_created} Matrix'