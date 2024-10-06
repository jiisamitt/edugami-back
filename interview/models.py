from django.db import models

# Student model
class Student(models.Model):
  id = models.PositiveIntegerField(primary_key=True)
  rut = models.CharField(max_length=13, unique=True)
  name = models.CharField(max_length=100)

# Test model
class Test(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
        
# Question model
class Question(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    statement = models.CharField(max_length=2500)
    explanation = models.CharField(max_length=2500)
    score = models.PositiveIntegerField()
    AXIS_TYPES = [
      ("Numeros", "Números"),
      ("Geometria", "Geometría"),
      ("Álgebra y Funciones", "Álgebra y funciones"),
      ("Probabilidad y estadística", "Probabilidad y estadística"),
    ]
    axis_type = models.CharField(max_length=50, choices=AXIS_TYPES)
    test = models.ForeignKey('Test', on_delete=models.CASCADE, related_name='questions')

# Alternative model    
class Alternative(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    content = models.CharField(max_length=500)
    correct = models.BooleanField()
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='alternatives')
    
# Student Test model
class StudentTest(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='tests')
    test = models.ForeignKey('Test', on_delete=models.CASCADE, related_name='students')
    
    class Meta:
      unique_together = ['student', 'test']  

# Answer model
class Answer(models.Model):
    student_test = models.ForeignKey('StudentTest', on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers')
    alternative = models.ForeignKey('Alternative', on_delete=models.CASCADE, related_name='answers')
    is_correct = models.BooleanField()
    
    class Meta:
      unique_together = ['student_test', 'question']