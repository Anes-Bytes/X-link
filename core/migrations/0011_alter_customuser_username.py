# Generated manually to fix username unique constraint

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_template_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
