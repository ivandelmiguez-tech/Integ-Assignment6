from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("albums", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="photo",
            name="image",
            field=models.ImageField(upload_to="photos/%Y/%m/"),
        ),
    ]
