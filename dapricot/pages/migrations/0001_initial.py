# Generated by Django 2.2.1 on 2019-06-01 05:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('flatpages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('flatpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='flatpages.FlatPage')),
                ('in_main_menu', models.BooleanField(default=False, help_text='If this is checked, the page will be visible in main menu.', verbose_name='show in main menu')),
            ],
            options={
                'db_table': 'dapricot_pages_page',
            },
            bases=('flatpages.flatpage',),
        ),
    ]
