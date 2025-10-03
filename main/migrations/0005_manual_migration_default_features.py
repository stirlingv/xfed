from django.db import migrations

def create_default_features(apps, schema_editor):
    Feature = apps.get_model('main', 'Feature')
    Feature.objects.get_or_create(
        icon='fa-gem', title='Taxes', description='Expert tax preparation and planning for individuals and businesses.'
    )
    Feature.objects.get_or_create(
        icon='fa-paper-plane', title='Data Science', description='Data-driven insights to optimize your financial decisions.'
    )
    Feature.objects.get_or_create(
        icon='fa-rocket', title='Information Technology', description='Secure and efficient IT solutions for your tax data.'
    )
    Feature.objects.get_or_create(
        icon='fa-signal', title='Veterans Affairs', description='Specialized support for veterans and their families.'
    )

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_feature_description_alter_feature_icon_and_more'),
    ]

    operations = [
        migrations.RunPython(create_default_features),
    ]