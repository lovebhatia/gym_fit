import datetime
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from core.serializers import MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import Note, CustomUser, ExerciseDay, ExerciseDataList
from core.serializers import NoteSerializer, ProfileSerializer, ExerciseDaySerializer, ExerciseDataListSerializer
from rest_framework import generics
from .serializers import WorkoutSerializer, ExerciseSerializer, SetSerializer, BMIRecordSerializer
from .models import Workout, Exercise, Set, BMIRecord
import os
from google.cloud import storage
from google.oauth2 import service_account





# Create your views here.

#Login User
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

#Register User
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token/',
        '/api/register/',
        '/api/token/refresh/',
        '/api/prediction/'
        'api/notes/',
        'api/note/<int:pk>/',
        'api/note/<int:pk>/update/',
        'api/note/<int:pk>/delete/',
        'api/note/mynotes/',
        'api/notes/create/',
        'api/profile/',
        'api/profile/update/',
        'api/users/<int:pk>/notes',

    ]
    return Response(routes)

#api/notes
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getNotes(request):
    public_notes = Note.objects.filter(is_public=True).order_by('-updated')[:10]
    user_notes = request.user.notes.all().order_by('-updated')[:10]
    notes = public_notes | user_notes
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getExerciseListDay(request):
    exerciseDay = ExerciseDay.objects.all()
    serializer = ExerciseDaySerializer(exerciseDay, many = True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def exercise_day_list(request):
    exercise_days = ExerciseDay.objects.select_related('exercise').all()
    # Select_related is used to fetch related 'Exercise' objects in a single query
    data = [{'date': day.date, 'exercise_name': day.exercise.name} for day in exercise_days]
    return JsonResponse(data, safe=False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getExercises_by_day(request, exercise_day_id):
    try:
        # Retrieve ExerciseDay instance by ID
        exercise_day = ExerciseDay.objects.get(id=exercise_day_id)
        # Retrieve related Exercise data for the ExerciseDay
        exercises = ExerciseDataList.objects.filter(name_of_parts_exercise=exercise_day)
        # Serialize Exercise data
        data = [{'id': exercise.id, 'name': exercise.name_of_exercise, 'sets': exercise.sets, 'gif': exercise.gif,
                 'description': exercise.description } for exercise in exercises]
        return JsonResponse(data, safe=False)
    except ExerciseDay.DoesNotExist:
        return JsonResponse({'error': 'ExerciseDay not found'}, status=404)
    

#api/notes/<int:pk>
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getNote(request, pk):
    note = request.user.notes.get(id=pk)
    serializer = NoteSerializer(note, many=False)
    return Response(serializer.data)


#api/notes/<int:pk>/update
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def updateNote(request, pk):
    note = request.user.notes.get(id=pk)
    serializer = NoteSerializer(instance=note, data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)



#api/notes/<int:pk>/delete
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteNote(request, pk):
    note = request.user.notes.get(id=pk)
    note.delete()
    return Response('Note was deleted')


#api/notes/create
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createNote(request):
    user = request.user
    data = request.data
    note = Note.objects.create(
           user=user,
        title=data['title'],
        body=data['body'],
        cover_image=data['cover_image']
    )
    serializer = NoteSerializer(note, many=False)
    return Response(serializer.data)


#api/profile  and api/profile/update
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProfile(request):
    user = request.user
    serializer = ProfileSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def updateProfile(request):
    user = request.user
    serializer = ProfileSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)



#api/notes/user/<int:pk>/mynotes
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserNotes(request, pk):
    user = CustomUser.objects.get(id=pk)
    notes = Note.objects.filter(user=user)
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)


class WorkoutListCreateAPIView(generics.ListCreateAPIView):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    permission_classes = [IsAuthenticated]

class WorkoutRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    permission_classes = [IsAuthenticated]

class ExerciseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]

class ExerciseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]

class SetListCreateAPIView(generics.ListCreateAPIView):
    queryset = Set.objects.all()
    serializer_class = SetSerializer
    permission_classes = [IsAuthenticated]

class SetRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Set.objects.all()
    serializer_class = SetSerializer
    permission_classes = [IsAuthenticated]
    
class SetsByUserWorkoutExerciseListAPIView(generics.ListAPIView):
    serializer_class = SetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        workout_id = self.kwargs['workout_id']
        exercise_id = self.kwargs['exercise_id']
        
        # Filter sets based on user, workout, and exercise IDs
        return Set.objects.filter(exercise__workout__user_id=user_id, exercise__workout_id=workout_id, exercise_id=exercise_id)


class SaveSetsDataAPIView(generics.CreateAPIView):
    serializer_class = SetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        workout_id = self.kwargs.get('workout_id')
        exercise_id = self.kwargs.get('exercise_id')
        return Set.objects.filter(exercise__workout__user_id=user_id, exercise__workout_id=workout_id, exercise_id=exercise_id)


    def create(self, request, user_id, workout_id, exercise_id, *args, **kwargs):
        sets_data = request.data.get('sets_data', [])
        try:
            exercise = Exercise.objects.get(id=exercise_id, workout_id=workout_id)
            saved_sets = []
            for set_data in sets_data:
                weight = set_data.get('weight')
                reps = set_data.get('reps')
                # Validate data
                if weight is not None and reps is not None:
                    set_instance = Set.objects.create(exercise=exercise, weight=weight, reps=reps)
                    saved_sets.append(set_instance)
            serializer = self.get_serializer(saved_sets, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exercise.DoesNotExist:
            return Response({"error": "Exercise not found."}, status=status.HTTP_404_NOT_FOUND)
        
        
class BMIRecordListCreateAPIView(generics.ListCreateAPIView):
    queryset = BMIRecord.objects.all()
    serializer_class = BMIRecordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Retrieve user ID from URL parameter
        user_id = self.kwargs.get('user_id')

        # Retrieve other parameters from request body
        sex = request.data.get('sex')
        height = request.data.get('height')
        weight = request.data.get('weight')
        age = request.data.get('age')
        bmi = request.data.get('bmi')

        # Validate user existence
        try:
            user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=400)

        # Create BMI record
        bmi_record = BMIRecord.objects.create(
            user=user,
            sex=sex,
            height=height,
            weight=weight,
            age=age,
            bmi=bmi
        )

        # Serialize BMI record
        bmi_record_serializer = BMIRecordSerializer(bmi_record)

        # Return BMI record and associated user data in response
        response_data = {
            'user': {
                'id': user.id,
                'username': user.username,
                # Include other user fields as needed
            },
            'bmi_record': bmi_record_serializer.data
        }
        return JsonResponse(response_data, status=201)

class BMIRecordRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BMIRecord.objects.all()
    serializer_class = BMIRecordSerializer
    permission_classes = [IsAuthenticated]
    
class BMIRecordByUserAPIView(generics.ListAPIView):
    serializer_class = BMIRecordSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        print('test')
        return BMIRecord.objects.filter(user_id=user_id)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_video_url(bucket_name):
    key_path = 'C:/Users/lovebhatia/Downloads/key_google_json.json'

    # Initialize a client using the service account key file
    credentials = service_account.Credentials.from_service_account_file(key_path)
    storage_client = storage.Client(credentials=credentials)
    #client = storage.Client.from_service_account_json(key_path)
    
    # Replace 'your_bucket_name' and 'your_video.mp4' with your actual bucket name and video file name
    bucket_name = 'gym_fit_bucket'
    video_name = 'Fly.gif'
    
    # Generate a signed URL for the video
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(video_name)
    expiration = datetime.timedelta(days=30)
    signed_url = blob.generate_signed_url(expiration=expiration)  # URL expires in 1 hour

    print(signed_url)
    return Response({'video_url': signed_url})


class ExerciseDayCreate(generics.ListCreateAPIView):
    queryset = ExerciseDay.objects.all()
    serializer_class = ExerciseDaySerializer

class DayRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExerciseDataList.objects.all()
    serializer_class = ExerciseDataListSerializer

class ExerciseListCreate(generics.ListCreateAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

class ExerciseRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer


   


    



'''
@api_view(['GET', 'POST'])
def workout_list(request):
    if request.method == 'GET':
        workouts = Workout.objects.all()
        serializer = WorkoutSerializer(workouts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = WorkoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def workout_detail(request, pk):
    try:
        workout = Workout.objects.get(pk=pk)
    except Workout.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = WorkoutSerializer(workout)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = WorkoutSerializer(workout, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        workout.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        
def save_sets_data(user_id, workout_id, exercise_id, sets_data):
    saved_sets = []
    try:
        exercise = Exercise.objects.get(id=exercise_id, workout_id=workout_id)
        for set_data in sets_data:
            weight = set_data.get('weight')
            reps = set_data.get('reps')
            # Validate data
            if weight is not None and reps is not None:
                set_instance = Set.objects.create(exercise=exercise, weight=weight, reps=reps)
                saved_sets.append(set_instance)
    except Exercise.DoesNotExist:
        # Handle case where exercise does not exist
        pass

    return saved_sets
    
''' 

    


    
