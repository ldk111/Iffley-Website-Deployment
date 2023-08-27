from django.db import models
import json

class Hold(models.Model):
    name = models.CharField(max_length = 50, unique = True)
    pixels_x1 = models.IntegerField()
    pixels_x2 = models.IntegerField()
    pixels_y1 = models.IntegerField()
    pixels_y2 = models.IntegerField()

class TechGrade(models.Model):
    grade = models.CharField(max_length = 50, unique = True)

class FurlongGrade(models.Model):
    grade = models.CharField(max_length = 50, unique = True)

class BGrade(models.Model):
    grade = models.CharField(max_length = 50, unique = True)

class Section(models.Model):
    short_name = models.CharField(max_length = 50, unique = True)
    long_name = models.CharField(max_length= 50)

class Route(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    holds = models.ManyToManyField(Hold, related_name = 'holds')
    start_holds = models.ManyToManyField(Hold, related_name = 'starting_holds')
    image = models.ImageField(blank = True, null = True, upload_to = "img")
    holds_str = models.TextField(blank = True, null = True)
    stand_start = models.BooleanField(blank = True, null = True)
    tech_grade = models.ForeignKey(TechGrade, related_name = "tech_grade", on_delete=models.CASCADE, null = True, blank = True)
    b_grade = models.ForeignKey(BGrade, related_name = "b_grade", on_delete=models.CASCADE, null = True, blank = True)
    furlong_grade = models.ForeignKey(FurlongGrade, related_name = "furlong_grade", on_delete=models.CASCADE, null = True, blank = True)
    other_grade = models.CharField(max_length = 50, null = True, blank = True)
    section = models.ForeignKey(Section, related_name = "section", on_delete=models.CASCADE, null = True, blank = True )
    description = models.TextField(null = True, blank = True)
    tag_all = models.BooleanField(blank = True, null = True)
    tag_tall = models.BooleanField(blank = True, null = True)
    tag_tech = models.BooleanField(blank = True, null = True)
    tag_flex = models.BooleanField(blank = True, null = True)
    tag_strong = models.BooleanField(blank = True, null = True)
    tag_dyno = models.BooleanField(blank = True, null = True)
    tag_finger = models.BooleanField(blank = True, null = True)
    tag_infamous = models.BooleanField(blank = True, null = True)
    tag_ambulance = models.BooleanField(blank = True, null = True)
    stars = models.IntegerField(blank = True, null = True)


