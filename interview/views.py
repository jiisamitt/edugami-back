from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from interview.models import Test, Question, Alternative, Student, Answer, StudentTest
from django.db import transaction
from openai import OpenAI

# View to create student
class StudentCreateView(APIView):
    """
    View to create student
    """

    def post(self, request):
        try:
            student_instance = Student.objects.create(id=request.data['id'],rut=request.data['rut'],name=request.data['name'])
            return Response({'id': student_instance.id, 'status': 'Ok', 'message': 'Student created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'status': 'Error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# View to create many students
class StudentCreateManyView(APIView):
    """
    View to create many students
    """

    def post(self, request):
        successes = []
        try:
            for student_data in request.data:
                student_instance = Student.objects.create(id=student_data['id'],rut=student_data['rut'],name=student_data['name'])
                successes.append(student_instance.id)
            return Response({'status': 'Ok', 'success': successes}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'status': 'Error', 'message': str(e), 'success': successes}, status=status.HTTP_400_BAD_REQUEST)

# View to create test
class TestCreateView(APIView):
    """
    View to create test, corresponding questions and alternatives
    """

    @transaction.atomic
    def post(self, request):
      try:
        with transaction.atomic():
          # Create the test instance
          test_instance = Test.objects.create(id=request.data["id"],name=request.data['name'])
          # Create the questions and their alternatives
          for question_data in request.data['questions']:
              question_instance = Question.objects.create(
                  id=question_data['id'],
                  statement=question_data['statement'],
                  explanation=question_data['explanation'],
                  score=question_data['score'],
                  axis_type=question_data['axis_type'],
                  test=test_instance
              )

              # Create the alternatives for the question
              for alternative_data in question_data['alternatives']:
                  Alternative.objects.create(
                      id=alternative_data['id'],
                      content=alternative_data['content'],
                      correct=alternative_data['correct']=="true" or alternative_data['correct']==True,
                      question=question_instance
                  )

          return Response({'id': test_instance.id, 'status': 'Ok', 'message': 'Test created successfully'}, status=status.HTTP_201_CREATED)
      except Exception as e:
          return Response({'status': 'Error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# View to assign test to students
class TestAssignView(APIView):
    """
    View to assign test to many students
    """

    def post(self, request, test_id):
      successes = []
      try:
        test_instance = Test.objects.get(id=test_id)
        students = request.data['students']
        for student_id in students:
            student_instance = Student.objects.get(id=student_id)
            StudentTest.objects.create(student=student_instance, test=test_instance)
            successes.append(student_id)
        return Response({'status': 'Ok', 'success': successes}, status=status.HTTP_201_CREATED)
      except Exception as e:
          return Response({'status': 'Error', 'message': str(e), 'success': successes}, status=status.HTTP_400_BAD_REQUEST)
        
# View to send student answers
class TestAnswerView(APIView):
  """
  View to send student answers and get test results
  """
  def post(self, request, test_id):
    successes = []
    try:
      test_instance = Test.objects.get(id=test_id)
      for student_data in request.data['students']:
          student_instance = Student.objects.get(id=student_data['id'])
          student_test_instance = StudentTest.objects.get(student=student_instance, test=test_instance)
          for question_data in student_data['questions']:
              question_instance = Question.objects.get(id=question_data['id'], test=test_instance)
              alternative_instance = Alternative.objects.get(question=question_instance, id=question_data['answer'])
              Answer.objects.create(student_test=student_test_instance, question=question_instance, alternative=alternative_instance, is_correct=alternative_instance.correct)
          successes.append(student_instance.id)
      return Response({'status': 'Ok', 'success': successes}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'status': 'Error', 'message': str(e), 'success': successes}, status=status.HTTP_400_BAD_REQUEST)
    
  def get(self, request, test_id):
    try:
      test_instance = Test.objects.get(id=test_id)
      students = []
      for student_test_instance in test_instance.students.all():
          student = {
              'id': student_test_instance.student.id,
              'name': student_test_instance.student.name,
              'score': sum([1 for answer in student_test_instance.answers.all() if answer.is_correct]),
              'stats': {
                  'correct': sum([1 for answer in student_test_instance.answers.all() if answer.is_correct]),
                  'wrong': sum([1 for answer in student_test_instance.answers.all() if not answer.is_correct]),
                  'skip': len(test_instance.questions.all()) - len(student_test_instance.answers.all())
              }
          }
          students.append(student)
      return Response({'id': test_instance.id, 'name': test_instance.name, 'students': students}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'status': 'Error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# View to get student recommendations
class StudentRecommendationView(APIView):
  """
  View to get student recommendations, based on every test result they have taken, using OpenAI to generate personalized recommendations

  """
  
  def get(self, request, student_id):
    try:
      # get stats of every test taken by the student
      student_instance = Student.objects.get(id=student_id)
      numbers_score = 0
      numbers_total = 0
      geometry_score = 0
      geometry_total = 0
      algebra_score = 0
      algebra_total = 0
      probability_score = 0
      probability_total = 0
      for student_test_instance in student_instance.tests.all():
          for answer in student_test_instance.answers.all():
              if answer.question.axis_type == "Numeros":
                  numbers_total += 1
                  if answer.is_correct:
                      numbers_score += 1
              elif answer.question.axis_type == "Geometria":
                  geometry_total += 1
                  if answer.is_correct:
                      geometry_score += 1
              elif answer.question.axis_type == "Álgebra y Funciones":
                  algebra_total += 1
                  if answer.is_correct:
                      algebra_score += 1
              elif answer.question.axis_type == "Probabilidad y estadística":
                  probability_total += 1
                  if answer.is_correct:
                      probability_score += 1
      

      # generate recommendations using OpenAI
      client = OpenAI()
      completion = client.chat.completions.create(
          model="gpt-4o-mini",
          messages=[{"role": "system", "content": """
                  You are an expert educator in the fields: 'Numbers','Geometry','Algebra and functions','Probability and statics'. You need to give recommendations to the student for things to study based on their test results. 
                  If they have low results in a specific axis, you will recommend an easy path for them to follow, starting from basic concepts and exercices.
                  If they have high results in a specific axis, you will congratulate them and give them harder challenges to keep them motivated.
                  If they have no results in a specific axis, you will recommend them to start from the basics and give them a path to follow.
                  """},{"role": "user", "content": f"The results of student are: {numbers_score}/{numbers_total} in 'Numbers', {geometry_score}/{geometry_total} in 'Geometry', {algebra_score}/{algebra_total} in 'Algebra and functions', {probability_score}/{probability_total} in 'Probability and statics'"}]
      )    
      completion.choices[0].message.content
      
      # return recommendations
      return Response({'recommendations': completion.choices[0].message.content}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'status': 'Error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
  
# View to reset database (erase all data)
class ResetView(APIView):
    """
    View to reset database (erase all data)
    """

    def delete(self, request):
        try:
            Answer.objects.all().delete()
            StudentTest.objects.all().delete()
            Student.objects.all().delete()
            Test.objects.all().delete()
            Question.objects.all().delete()
            Alternative.objects.all().delete()
            return Response({'status': 'Ok', 'message': 'Database reset successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'Error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)