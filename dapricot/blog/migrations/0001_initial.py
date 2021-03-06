# Generated by Django 2.2.1 on 2019-06-01 05:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(blank=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'db_table': 'dapricot_blog_category',
            },
        ),
        migrations.CreateModel(
            name='Commenter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('status', models.CharField(choices=[('v', 'Verified'), ('u', 'Under verification')], default='u', editable=False, max_length=1)),
            ],
            options={
                'verbose_name': 'commenter',
                'verbose_name_plural': 'commentators',
                'db_table': 'dapricot_blog_commenter',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(blank=True)),
            ],
            options={
                'verbose_name': 'tag',
                'verbose_name_plural': 'tags',
                'db_table': 'dapricot_blog_tag',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=100)),
                ('content', models.TextField()),
                ('status', models.CharField(choices=[('d', 'Draft'), ('p', 'Published')], max_length=1)),
                ('enable_comments', models.BooleanField(default=False, verbose_name='enable comments')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('last_edition_date', models.DateTimeField(auto_now=True)),
                ('publication_date', models.DateTimeField(editable=False, null=True)),
                ('author', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dablog.Category')),
                ('tags', models.ManyToManyField(to='dablog.Tag')),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
                'db_table': 'dapricot_blog_post',
                'ordering': ('creation_date',),
                'unique_together': {('title', 'slug')},
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=500)),
                ('status', models.CharField(choices=[('a', 'Approved'), ('u', 'Under approvement')], default='u', max_length=1)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('answer_to', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='dablog.Comment')),
                ('author', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='dablog.Commenter')),
                ('post', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='dablog.Post')),
            ],
            options={
                'verbose_name': 'comment',
                'verbose_name_plural': 'comments',
                'db_table': 'dapricot_blog_comment',
                'ordering': ('creation_date',),
            },
        ),
    ]
