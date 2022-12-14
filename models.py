# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Author(models.Model):
    author_id = models.IntegerField(db_column='Author_ID', primary_key=True)  # Field name made lowercase.
    auhtor_name = models.CharField(db_column='Auhtor_Name', max_length=50)  # Field name made lowercase.
    affliation = models.CharField(db_column='Affliation', max_length=50, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=50, blank=True, null=True)  # Field name made lowercase.
    author_profile = models.TextField(db_column='Author_Profile', blank=True, null=True)  # Field name made lowercase.
    citation_count = models.IntegerField(db_column='Citation_Count', blank=True, null=True)  # Field name made lowercase.
    scholarly_output = models.IntegerField(db_column='Scholarly_Output', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'author'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DocAbstractTokens(models.Model):
    token = models.CharField(max_length=255)
    position = models.CharField(max_length=255, blank=True, null=True)
    frequency = models.IntegerField(blank=True, null=True)
    doc_id = models.IntegerField(blank=True, null=True)
    topic_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'doc_abstract_tokens'


class Document(models.Model):
    document_id = models.IntegerField(db_column='Document_ID', primary_key=True)  # Field name made lowercase.
    authors = models.TextField(db_column='Authors', blank=True, null=True)  # Field name made lowercase.
    name = models.TextField(db_column='Name', blank=True, null=True)  # Field name made lowercase.
    year = models.IntegerField(db_column='Year', blank=True, null=True)  # Field name made lowercase.
    cited_by = models.IntegerField(db_column='Cited_by', blank=True, null=True)  # Field name made lowercase.
    link = models.TextField(db_column='Link', blank=True, null=True)  # Field name made lowercase.
    abstract = models.TextField(db_column='Abstract', blank=True, null=True)  # Field name made lowercase.
    author_keywords = models.TextField(db_column='Author_Keywords', blank=True, null=True)  # Field name made lowercase.
    indexed_keywords = models.TextField(db_column='Indexed_Keywords', blank=True, null=True)  # Field name made lowercase.
    publisher = models.TextField(db_column='Publisher', blank=True, null=True)  # Field name made lowercase.
    document_type = models.TextField(db_column='Document_Type', blank=True, null=True)  # Field name made lowercase.
    topic = models.ForeignKey('Topic', models.DO_NOTHING, db_column='Topic_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'document'


class DocumentTitleTokens(models.Model):
    token = models.CharField(max_length=255)
    position = models.CharField(max_length=255, blank=True, null=True)
    frequency = models.IntegerField(blank=True, null=True)
    doc_id = models.IntegerField(blank=True, null=True)
    topic_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'document_title_tokens'


class Field(models.Model):
    field_name = models.CharField(db_column='Field_Name', primary_key=True, max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'field'


class FieldHasAuthors(models.Model):
    field_name = models.OneToOneField(Field, models.DO_NOTHING, db_column='Field_Name', primary_key=True)  # Field name made lowercase.
    author = models.ForeignKey(Author, models.DO_NOTHING, db_column='Author_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'field_has_authors'
        unique_together = (('field_name', 'author'),)


class FieldHasKeyphrase(models.Model):
    f_keyphrase_id = models.IntegerField(db_column='F_Keyphrase_ID', primary_key=True)  # Field name made lowercase.
    field_name = models.ForeignKey(Field, models.DO_NOTHING, db_column='Field_Name')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'field_has_keyphrase'
        unique_together = (('f_keyphrase_id', 'field_name'),)


class FieldKeyPhrase(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'field_key_phrase'


class FieldKeyphraseByYear(models.Model):
    f_keyphrase = models.OneToOneField(FieldKeyPhrase, models.DO_NOTHING, db_column='F_Keyphrase_ID', primary_key=True)  # Field name made lowercase.
    year = models.ForeignKey('Year', models.DO_NOTHING, db_column='Year_ID')  # Field name made lowercase.
    scholarly_output = models.IntegerField(db_column='Scholarly_Output')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'field_keyphrase_by_year'
        unique_together = (('f_keyphrase', 'year'),)


class Topic(models.Model):
    topic_id = models.IntegerField(db_column='Topic_ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50)  # Field name made lowercase.
    views_count = models.IntegerField(db_column='Views_Count')  # Field name made lowercase.
    scholarly_output = models.IntegerField(db_column='Scholarly_Output')  # Field name made lowercase.
    citation_count = models.IntegerField(db_column='Citation_Count')  # Field name made lowercase.
    field_name = models.ForeignKey(Field, models.DO_NOTHING, db_column='Field_Name')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'topic'


class TopicHasKeyphrase(models.Model):
    topic = models.OneToOneField(Topic, models.DO_NOTHING, db_column='Topic_ID', primary_key=True)  # Field name made lowercase.
    t_keyphrase = models.ForeignKey('TopicKeyphrase', models.DO_NOTHING, db_column='T_Keyphrase_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'topic_has_keyphrase'
        unique_together = (('topic', 't_keyphrase'),)


class TopicKeyphrase(models.Model):
    t_keyphrase_id = models.IntegerField(db_column='T_Keyphrase_ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=50)  # Field name made lowercase.
    relevance = models.FloatField(db_column='Relevance')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'topic_keyphrase'


class TopicTokens(models.Model):
    token_id = models.IntegerField(primary_key=True)
    tokens = models.CharField(max_length=100, db_collation='utf8_general_ci', blank=True, null=True)
    positions = models.IntegerField(blank=True, null=True)
    frequency = models.IntegerField(blank=True, null=True)
    topic_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'topic_tokens'


class UserDocument(models.Model):
    username = models.OneToOneField(AuthUser, models.DO_NOTHING, db_column='Username', primary_key=True)  # Field name made lowercase.
    document = models.ForeignKey(Document, models.DO_NOTHING, db_column='Document_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_document'
        unique_together = (('username', 'document'),)


class UserField(models.Model):
    username = models.OneToOneField(AuthUser, models.DO_NOTHING, db_column='Username', primary_key=True)  # Field name made lowercase.
    field_name = models.ForeignKey(Field, models.DO_NOTHING, db_column='Field_Name')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_field'
        unique_together = (('username', 'field_name'),)


class UserHistory(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    history_name = models.CharField(db_column='History_Name', max_length=500)  # Field name made lowercase.
    username = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='Username')  # Field name made lowercase.
    url = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_history'


class Year(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    year = models.IntegerField(db_column='Year')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'year'
