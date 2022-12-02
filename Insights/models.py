from django import forms
from django.db import models

# Create your models here.
class Field(models.Model):
    field_name = models.CharField(db_column='Field_Name', primary_key=True, max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'field'


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


class Year(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    year = models.IntegerField(db_column='Year')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'year'


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
