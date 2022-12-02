from django.db import models

# Create your models here.
class Field(models.Model):
    field_name = models.CharField(db_column='Field_Name', primary_key=True, max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'field'


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