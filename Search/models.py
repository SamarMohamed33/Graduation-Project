from django.db import models

# Create your models here.
class Field(models.Model):
    field_name = models.CharField(db_column='Field_Name', primary_key=True, max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'field'

  

    def __str__(self):
        return self.field_name    



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

    #def __str__(self):
    #    return self.field_name       




class Document(models.Model):
    document_id = models.IntegerField(db_column='Document_ID', primary_key=True)  # Field name made lowercase.
    authors = models.TextField(db_column='Authors', blank=True, null=True)  # Field name made lowercase.
    name = models.TextField(db_column='Name', blank=True, null=True)  # Field name made lowercase.
    year = models.IntegerField(db_column='Year', blank=True, null=True)  # Field name made lowercase.
    cited_by = models.IntegerField(db_column='Cited_by', blank=True, null=True)  # Field name made lowercase.
    #link = models.TextField(db_column='Link', blank=True, null=True)  # Field name made lowercase.
    abstract = models.TextField(db_column='Abstract', blank=True, null=True)  # Field name made lowercase.
    author_keywords = models.TextField(db_column='Author_Keywords', blank=True, null=True)  # Field name made lowercase.
    indexed_keywords = models.TextField(db_column='Indexed_Keywords', blank=True, null=True)  # Field name made lowercase.
    publisher = models.TextField(db_column='Publisher', blank=True, null=True)  # Field name made lowercase.
    document_type = models.TextField(db_column='Document_Type', blank=True, null=True)  # Field name made lowercase.
    topic = models.ForeignKey('Topic', models.DO_NOTHING, db_column='Topic_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'document'

    def __str__(self):
        return self.name 
        


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

        
    def __str__(self):
        return self.name 
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
    def __str__(self):
        return self.field_name   

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


class Year(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    year = models.IntegerField(db_column='Year')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'year'


class DocumentTitleTokens(models.Model):
    token = models.CharField(max_length=255)
    position = models.CharField(max_length=255, blank=True, null=True)
    frequency = models.IntegerField(blank=True, null=True)
    doc_id = models.IntegerField(blank=True, null=True)
    topic_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'document_title_tokens'        


class DocAbstractTokens(models.Model):
    token = models.CharField(max_length=255)
    position = models.CharField(max_length=255, blank=True, null=True)
    frequency = models.IntegerField(blank=True, null=True)
    doc_id = models.IntegerField(blank=True, null=True)
    topic_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'doc_abstract_tokens'        


class TopicTokens(models.Model):
    token_id = models.IntegerField(primary_key=True)
    tokens = models.CharField(max_length=100, db_collation='utf8_general_ci', blank=True, null=True)
    positions = models.IntegerField(blank=True, null=True)
    frequency = models.IntegerField(blank=True, null=True)
    topic_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'topic_tokens'        

class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150, primary_key=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'
        
class UserHistory(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    history_name = models.CharField(db_column='History_Name', max_length=500)  # Field name made lowercase.
    username = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='Username')  # Field name made lowercase.
    url = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_history'

class UserField(models.Model):
    username = models.OneToOneField(AuthUser, models.DO_NOTHING, db_column='Username', primary_key=True)  # Field name made lowercase.
    field_name = models.ForeignKey(Field, models.DO_NOTHING, db_column='Field_Name')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_field'
        unique_together = (('username', 'field_name'),)        

class UserDocument(models.Model):
    username = models.OneToOneField(AuthUser, models.DO_NOTHING, db_column='Username', primary_key=True)  # Field name made lowercase.
    document = models.ForeignKey(Document, models.DO_NOTHING, db_column='Document_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_document'
        unique_together = (('username', 'document'),)        