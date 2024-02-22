from core.models import MatrixField
from django.db import migrations, models


class Migration(migrations.Migration):


    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Matrix',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matrix_field', MatrixField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
