from django.db import models

# Create your models here.



class TagElement(models.Model):
  name = models.CharField(max_length=25, help_text="USE CAPITALS")
  is_block = models.BooleanField(default=True, help_text="Indicates whether or not an element creates a break in the text")
  weight = models.FloatField(default=1.0, help_text="Greater than 1 increases the importance of word and less than one decreases the importance. Use 0 to ignore all text from a tag")

  def __unicode__(self):
      return unicode(self.name)
