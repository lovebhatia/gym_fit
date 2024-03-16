from django.urls import path
from . import views
from .views import (
    WorkoutListCreateAPIView, WorkoutRetrieveUpdateDestroyAPIView,
    ExerciseListCreateAPIView, ExerciseRetrieveUpdateDestroyAPIView,
    SetListCreateAPIView, SetRetrieveUpdateDestroyAPIView, SetsByUserWorkoutExerciseListAPIView, 
    SaveSetsDataAPIView, BMIRecordListCreateAPIView, BMIRecordRetrieveUpdateDestroyAPIView, 
    BMIRecordByUserAPIView
)



from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    #Authentication
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('', views.getRoutes),


    #Profile
    path('profile/', views.getProfile, name='profile'),
    path('profile/update/', views.updateProfile, name='update-profile'),
    
    #Exercise
    path('exerciseDays/', views.getExerciseListDay, name = 'exerciseDays'),
    path('exercise-day/<int:exercise_day_id>/exercises/', views.getExercises_by_day, name='exercises-by-day'),
    
    #exercise-workouts
    path('workouts/', WorkoutListCreateAPIView.as_view(), name='workout-list'),
    path('workouts/<int:pk>/', WorkoutRetrieveUpdateDestroyAPIView.as_view(), name='workout-detail'),
    path('exercises/', ExerciseListCreateAPIView.as_view(), name='exercise-list'),
    path('exercises/<int:pk>/', ExerciseRetrieveUpdateDestroyAPIView.as_view(), name='exercise-detail'),
    path('sets/', SetListCreateAPIView.as_view(), name='set-list'),
    path('sets/<int:pk>/', SetRetrieveUpdateDestroyAPIView.as_view(), name='set-detail'),
    path('sets/<int:user_id>/<int:workout_id>/<int:exercise_id>/', SetsByUserWorkoutExerciseListAPIView.as_view(), name='sets-by-user-workout-exercise'),
    path('save_sets_data/<int:user_id>/<int:workout_id>/<int:exercise_id>/', SaveSetsDataAPIView.as_view(), name='save_sets_data'),
    path('bmi/<int:user_id>/', BMIRecordListCreateAPIView.as_view(), name='bmi-list-create'),
    path('bmi/detail/<int:pk>/', BMIRecordRetrieveUpdateDestroyAPIView.as_view(), name='bmi-detail'),
    path('bmi/user/<int:user_id>/', BMIRecordByUserAPIView.as_view(), name='bmi-by-user'),
    path('get-video-url/', views.get_video_url, name='get_video_url'),





    
    




    #Notes
    path('notes/', views.getNotes, name="notes"),
    path('notes/<int:pk>/', views.getNote, name="note"),
    path('notes/<int:pk>/update/', views.updateNote, name="update-note"),
    path('notes/<int:pk>/delete/', views.deleteNote, name="delete-note"),
    path('users/<int:pk>/notes',views.getUserNotes, name="my-notes"),
    path('notes/create/', views.createNote, name="create-note"),
]