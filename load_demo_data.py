import os
import django
import random
from datetime import timedelta

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dyslexia_project.settings')
django.setup()

# Import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from accounts.models import ChildProfile, ParentProfile, TeacherProfile
from exercises.models import (
    ExerciseCategory, ExerciseType, Exercise, Question, Answer, 
    ExerciseAttempt, QuestionResponse
)
from progress.models import (
    Achievement, UserAchievement, ProgressRecord, ProgressReport,
    RewardItem, UserReward
)

User = get_user_model()

def create_users():
    print("Creating users...")
    
    # Create admin user
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'user_type': 'admin',
            'is_staff': True,
            'is_superuser': True
        }
    )
    
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("Admin user created")
    
    # Create parent user
    parent_user, created = User.objects.get_or_create(
        username='parent',
        defaults={
            'email': 'parent@example.com',
            'user_type': 'parent',
            'first_name': 'Sophie',
            'last_name': 'Martin'
        }
    )
    
    if created:
        parent_user.set_password('parent123')
        parent_user.save()
        ParentProfile.objects.create(user=parent_user)
        print("Parent user created")
    
    # Create teacher user
    teacher_user, created = User.objects.get_or_create(
        username='teacher',
        defaults={
            'email': 'teacher@example.com',
            'user_type': 'teacher',
            'first_name': 'Thomas',
            'last_name': 'Dubois'
        }
    )
    
    if created:
        teacher_user.set_password('teacher123')
        teacher_user.save()
        TeacherProfile.objects.create(
            user=teacher_user,
            school_name='École Primaire Jean Moulin',
            specialization='Troubles DYS'
        )
        print("Teacher user created")
    
    # Create child users
    child_data = [
        {
            'username': 'lucas',
            'email': 'lucas@example.com',
            'first_name': 'Lucas',
            'last_name': 'Martin',
            'password': 'lucas123',
            'profile': {
                'school_level': 'ce2',
                'has_dyslexia': True,
                'has_dyscalculia': False,
                'dyslexia_level': 2,
                'dyscalculia_level': None
            }
        },
        {
            'username': 'emma',
            'email': 'emma@example.com',
            'first_name': 'Emma',
            'last_name': 'Petit',
            'password': 'emma123',
            'profile': {
                'school_level': 'cm1',
                'has_dyslexia': False,
                'has_dyscalculia': True,
                'dyslexia_level': None,
                'dyscalculia_level': 2
            }
        },
        {
            'username': 'theo',
            'email': 'theo@example.com',
            'first_name': 'Théo',
            'last_name': 'Bernard',
            'password': 'theo123',
            'profile': {
                'school_level': 'ce1',
                'has_dyslexia': True,
                'has_dyscalculia': True,
                'dyslexia_level': 3,
                'dyscalculia_level': 1
            }
        }
    ]
    
    children = []
    
    for data in child_data:
        child, created = User.objects.get_or_create(
            username=data['username'],
            defaults={
                'email': data['email'],
                'user_type': 'child',
                'first_name': data['first_name'],
                'last_name': data['last_name']
            }
        )
        
        if created:
            child.set_password(data['password'])
            child.save()
            
            profile_data = data['profile']
            ChildProfile.objects.create(
                user=child,
                school_level=profile_data['school_level'],
                has_dyslexia=profile_data['has_dyslexia'],
                has_dyscalculia=profile_data['has_dyscalculia'],
                dyslexia_level=profile_data['dyslexia_level'],
                dyscalculia_level=profile_data['dyscalculia_level']
            )
            print(f"Child user {data['username']} created")
        
        children.append(child)
    
    # Associate children with parent
    parent_profile = ParentProfile.objects.get(user=parent_user)
    for child in children[:2]:  # First two children belong to the parent
        parent_profile.children.add(child)
    
    # Associate children with teacher
    teacher_profile = TeacherProfile.objects.get(user=teacher_user)
    for child in children:  # All children have the teacher
        teacher_profile.students.add(child)
    
    return {
        'admin': admin_user,
        'parent': parent_user,
        'teacher': teacher_user,
        'children': children
    }

def create_categories():
    print("Creating exercise categories...")
    
    categories = [
        {
            'name': 'Lecture',
            'description': 'Exercices pour améliorer la lecture et la reconnaissance des lettres',
            'icon': 'fa-book-reader',
            'color': '#4E54C8'
        },
        {
            'name': 'Écriture',
            'description': 'Exercices pour améliorer l\'écriture et l\'orthographe',
            'icon': 'fa-pencil-alt',
            'color': '#FF6B6B'
        },
        {
            'name': 'Nombres',
            'description': 'Exercices pour améliorer la reconnaissance et la compréhension des nombres',
            'icon': 'fa-sort-numeric-up',
            'color': '#1ABC9C'
        },
        {
            'name': 'Calcul',
            'description': 'Exercices pour améliorer les compétences en calcul',
            'icon': 'fa-calculator',
            'color': '#F39C12'
        },
        {
            'name': 'Problèmes',
            'description': 'Exercices pour améliorer la résolution de problèmes mathématiques',
            'icon': 'fa-puzzle-piece',
            'color': '#9B59B6'
        }
    ]
    
    created_categories = []
    
    for data in categories:
        category, created = ExerciseCategory.objects.get_or_create(
            name=data['name'],
            defaults={
                'description': data['description'],
                'icon': data['icon'],
                'color': data['color']
            }
        )
        
        if created:
            print(f"Category '{data['name']}' created")
        
        created_categories.append(category)
    
    return created_categories

def create_exercise_types(categories):
    print("Creating exercise types...")
    
    exercise_types = [
        # Dyslexia exercise types
        {
            'name': 'Reconnaissance de lettres',
            'category': categories[0],  # Lecture
            'description': 'Exercices pour améliorer la reconnaissance des lettres et des sons',
            'disorder_type': 'dyslexia',
            'icon': 'fa-font'
        },
        {
            'name': 'Lecture de mots',
            'category': categories[0],  # Lecture
            'description': 'Exercices pour améliorer la lecture de mots avec mise en évidence syllabique',
            'disorder_type': 'dyslexia',
            'icon': 'fa-file-word'
        },
        {
            'name': 'Dictée adaptée',
            'category': categories[1],  # Écriture
            'description': 'Exercices de dictée adaptés aux enfants dyslexiques',
            'disorder_type': 'dyslexia',
            'icon': 'fa-headphones'
        },
        
        # Dyscalculia exercise types
        {
            'name': 'Reconnaissance de nombres',
            'category': categories[2],  # Nombres
            'description': 'Exercices pour améliorer la reconnaissance et la compréhension des nombres',
            'disorder_type': 'dyscalculia',
            'icon': 'fa-sort-numeric-up'
        },
        {
            'name': 'Calcul mental',
            'category': categories[3],  # Calcul
            'description': 'Exercices pour améliorer les compétences en calcul mental',
            'disorder_type': 'dyscalculia',
            'icon': 'fa-calculator'
        },
        {
            'name': 'Résolution de problèmes',
            'category': categories[4],  # Problèmes
            'description': 'Exercices pour améliorer la résolution de problèmes mathématiques',
            'disorder_type': 'dyscalculia',
            'icon': 'fa-puzzle-piece'
        }
    ]
    
    created_types = []
    
    for data in exercise_types:
        exercise_type, created = ExerciseType.objects.get_or_create(
            name=data['name'],
            category=data['category'],
            defaults={
                'description': data['description'],
                'disorder_type': data['disorder_type'],
                'icon': data['icon']
            }
        )
        
        if created:
            print(f"Exercise type '{data['name']}' created")
        
        created_types.append(exercise_type)
    
    return created_types

def create_dyslexia_exercises(exercise_types):
    print("Creating dyslexia exercises...")
    
    # Get dyslexia exercise types
    letter_recognition = exercise_types[0]  # Reconnaissance de lettres
    word_reading = exercise_types[1]  # Lecture de mots
    dictation = exercise_types[2]  # Dictée adaptée
    
    exercises = [
        # Letter recognition exercises
        {
            'title': 'Lettres similaires: b, d, p, q',
            'exercise_type': letter_recognition,
            'instructions': """
                <p>Dans cet exercice, tu vas t'entraîner à reconnaître les lettres qui se ressemblent: <strong>b</strong>, <strong>d</strong>, <strong>p</strong> et <strong>q</strong>.</p>
                <p>Pour chaque question, choisis la bonne lettre qui correspond à l'image ou au son.</p>
                <p>Tu peux utiliser les outils d'aide si tu en as besoin.</p>
            """,
            'difficulty': 1,
            'estimated_time': 10,
            'points': 50,
            'questions': [
                {
                    'text': 'Quelle est cette lettre? <span class="letter-container">b</span>',
                    'question_type': 'multiple_choice',
                    'answers': [
                        {'text': 'b', 'is_correct': True, 'feedback': 'Bravo! C\'est bien la lettre b.'},
                        {'text': 'd', 'is_correct': False, 'feedback': 'Ce n\'est pas la lettre d. Regarde bien: la boucle du b est à gauche.'},
                        {'text': 'p', 'is_correct': False, 'feedback': 'Ce n\'est pas la lettre p. Regarde bien: la boucle du b est en haut.'},
                        {'text': 'q', 'is_correct': False, 'feedback': 'Ce n\'est pas la lettre q. Regarde bien: la boucle du b est à gauche et en haut.'}
                    ]
                },
                {
                    'text': 'Quelle est cette lettre? <span class="letter-container">d</span>',
                    'question_type': 'multiple_choice',
                    'answers': [
                        {'text': 'b', 'is_correct': False, 'feedback': 'Ce n\'est pas la lettre b. Regarde bien: la boucle du d est à droite.'},
                        {'text': 'd', 'is_correct': True, 'feedback': 'Bravo! C\'est bien la lettre d.'},
                        {'text': 'p', 'is_correct': False, 'feedback': 'Ce n\'est pas la lettre p. Regarde bien: la boucle du d est en haut.'},
                        {'text': 'q', 'is_correct': False, 'feedback': 'Ce n\'est pas la lettre q. Regarde bien: la boucle du d est à droite et en haut.'}
                    ]
                },
                {
                    'text': 'Quelle est cette lettre? <span class="letter-container">p</span>',
                    'question_type': 'multiple_choice',
                    'answers': [
                        {'text': 'b', 'is_correct': False, 'feedback': 'Ce n\'est pas la lettre b. Regarde bien: la boucle du p est en bas.'},
                        {'text': 'd', 'is_correct': False, 'feedback': 'Ce n\'est pas la lettre d. Regarde bien: la boucle du p est à gauche.'},
                        {'text': 'p', 'is_correct': True, 'feedback': 'Bravo! C\'est bien la lettre p.'},
                        {'text': 'q', 'is_correct': False, 'feedback': 'Ce n\'est pas la lettre q. Regarde bien: la boucle du p est à gauche et en bas.'}
                    ]
                },
                {
                    'text': 'Quelle est cette lettre? <span class="letter-container">q</span>',
                    'question_type': 'multiple_choice',
                    'answers': [
                        {'text': 'b', 'is_correct': False, 'feedback': 'Ce n\'est pas la lettre b. Regarde bien: la boucle du q est en bas.'},
                        {'text': 'd', 'is_correct': False, 'feedback': 'Ce n\'est pas la lettre d. Regarde bien: la boucle du q est à droite.'},
                        {'text': 'p', 'is_correct': False, 'feedback': 'Ce n\'est pas la lettre p. Regarde bien: la boucle du q est à droite et en bas.'},
                        {'text': 'q', 'is_correct': True, 'feedback': 'Bravo! C\'est bien la lettre q.'}
                    ]
                },
                {
                    'text': 'Trouve le mot qui contient la lettre "b".',
                    'question_type': 'multiple_choice',
                    'answers': [
                        {'text': 'bateau', 'is_correct': True, 'feedback': 'Bravo! Le mot "bateau" contient bien la lettre "b".'},
                        {'text': 'domino', 'is_correct': False, 'feedback': 'Le mot "domino" contient la lettre "d", pas "b".'},
                        {'text': 'pomme', 'is_correct': False, 'feedback': 'Le mot "pomme" contient la lettre "p", pas "b".'},
                        {'text': 'quatre', 'is_correct': False, 'feedback': 'Le mot "quatre" contient la lettre "q", pas "b".'}
                    ]
                }
            ]
        },
        
        # Word reading exercises
        {
            'title': 'Lecture de mots avec syllabes',
            'exercise_type': word_reading,
            'instructions': """
                <p>Dans cet exercice, tu vas t'entraîner à lire des mots en les découpant en syllabes.</p>
                <p>Pour chaque mot, clique sur les syllabes pour les entendre, puis réponds à la question.</p>
                <p>Tu peux utiliser les outils d'aide si tu en as besoin.</p>
            """,
            'difficulty': 2,
            'estimated_time': 15,
            'points': 75,
            'questions': [
                {
                    'text': 'Lis ce mot: <span class="syllable">cha</span><span class="syllable">peau</span>',
                    'question_type': 'multiple_choice',
                    'answers': [
                        {'text': 'Un objet qu\'on met sur la tête', 'is_correct': True, 'feedback': 'Bravo! Un chapeau est bien un objet qu\'on met sur la tête.'},
                        {'text': 'Un animal qui miaule', 'is_correct': False, 'feedback': 'Ce n\'est pas un chat, mais un chapeau.'},
                        {'text': 'Un fruit rouge', 'is_correct': False, 'feedback': 'Ce n\'est pas une fraise, mais un chapeau.'},
                        {'text': 'Un moyen de transport', 'is_correct': False, 'feedback': 'Ce n\'est pas une voiture, mais un chapeau.'}
                    ]
                },
                {
                    'text': 'Lis ce mot: <span class="syllable">pa</span><span class="syllable">pi</span><span class="syllable">llon</span>',
                    'question_type': 'multiple_choice',
                    'answers': [
                        {'text': 'Un insecte qui vole', 'is_correct': True, 'feedback': 'Bravo! Un papillon est bien un insecte qui vole.'},
                        {'text': 'Un fruit jaune', 'is_correct': False, 'feedback': 'Ce n\'est pas une banane, mais un papillon.'},
                        {'text': 'Un légume orange', 'is_correct': False, 'feedback': 'Ce n\'est pas une carotte, mais un papillon.'},
                        {'text': 'Un animal qui nage', 'is_correct': False, 'feedback': 'Ce n\'est pas un poisson, mais un papillon.'}
                    ]
                },
                {
                    'text': 'Lis ce mot: <span class="syllable">é</span><span class="syllable">lé</span><span class="syllable">phant</span>',
                    'question_type': 'multiple_choice',
                    'answers': [
                        {'text': 'Un grand animal avec une trompe', 'is_correct': True, 'feedback': 'Bravo! Un éléphant est bien un grand animal avec une trompe.'},
                        {'text': 'Un animal qui vole', 'is_correct': False, 'feedback': 'Ce n\'est pas un oiseau, mais un éléphant.'},
                        {'text': 'Un animal qui nage', 'is_correct': False, 'feedback': 'Ce n\'est pas un poisson, mais un éléphant.'},
                        {'text': 'Un petit insecte', 'is_correct': False, 'feedback': 'Ce n\'est pas une fourmi, mais un éléphant.'}
                    ]
                },
                {
                    'text': 'Lis ce mot: <span class="syllable">cho</span><span class="syllable">co</span><span class="syllable">lat</span>',
                    'question_type': 'multiple_choice',
                    'answers': [
                        {'text': 'Une friandise sucrée brune', 'is_correct': True, 'feedback': 'Bravo! Le chocolat est bien une friandise sucrée brune.'},
                        {'text': 'Un légume vert', 'is_correct': False, 'feedback': 'Ce n\'est pas un brocoli, mais du chocolat.'},
                        {'text': 'Un fruit rouge', 'is_correct': False, 'feedback': 'Ce n\'est pas une fraise, mais du chocolat.'},
                        {'text': 'Une boisson chaude', 'is_correct': False, 'feedback': 'Le chocolat peut être une boisson, mais ici on parle de la friandise.'}
                    ]
                },
                {
                    'text': 'Lis ce mot: <span class="syllable">or</span><span class="syllable">di</span><span class="syllable">na</span><span class="syllable">teur</span>',
                    'question_type': 'multiple_choice',
                    'answers': [
                        {'text': 'Une machine électronique', 'is_correct': True, 'feedback': 'Bravo! Un ordinateur est bien une machine électronique.'},
                        {'text': 'Un instrument de musique', 'is_correct': False, 'feedback': 'Ce n\'est pas un piano, mais un ordinateur.'},
                        {'text': 'Un meuble pour s\'asseoir', 'is_correct': False, 'feedback': 'Ce n\'est pas une chaise, mais un ordinateur.'},
                        {'text': 'Un outil pour écrire', 'is_correct': False, 'feedback': 'Ce n\'est pas un stylo, mais un ordinateur.'}
                    ]
                }
            ]
        },
        
        # Dictation exercises
        {
            'title': 'Dictée de mots simples',
            'exercise_type': dictation,
            'instructions': """
                <p>Dans cet exercice, tu vas écouter des mots et les écrire.</p>
                <p>Clique sur l'icône du haut-parleur pour entendre le mot, puis écris-le dans la case.</p>
                <p>Tu peux réécouter le mot autant de fois que nécessaire.</p>
            """,
            'difficulty': 1,
            'estimated_time': 10,
            'points': 50,
            'questions': [
                {
                    'text': 'Écris le mot que tu entends.',
                    'question_type': 'fill_blank',
                    'audio': '/static/audio/chat.mp3',
                    'answers': [
                        {'text': 'chat', 'is_correct': True, 'feedback': 'Bravo! Tu as bien écrit le mot "chat".'},
                        {'text': 'sha', 'is_correct': False, 'feedback': 'Ce n\'est pas la bonne orthographe. On écrit "chat".'},
                        {'text': 'cha', 'is_correct': False, 'feedback': 'Il manque une lettre. On écrit "chat".'},
                        {'text': 'chatte', 'is_correct': False, 'feedback': 'Tu as ajouté des lettres. On écrit "chat".'}
                    ]
                },
                {
                    'text': 'Écris le mot que tu entends.',
                    'question_type': 'fill_blank',
                    'audio': '/static/audio/maison.mp3',
                    'answers': [
                        {'text': 'maison', 'is_correct': True, 'feedback': 'Bravo! Tu as bien écrit le mot "maison".'},
                        {'text': 'méson', 'is_correct': False, 'feedback': 'Ce n\'est pas la bonne orthographe. On écrit "maison".'},
                        {'text': 'mèzon', 'is_correct': False, 'feedback': 'Ce n\'est pas la bonne orthographe. On écrit "maison".'},
                        {'text': 'maizon', 'is_correct': False, 'feedback': 'Ce n\'est pas la bonne orthographe. On écrit "maison".'}
                    ]
                },
                {
                    'text': 'Écris le mot que tu entends.',
                    'question_type': 'fill_blank',
                    'audio': '/static/audio/ecole.mp3',
                    'answers': [
                        {'text': 'école', 'is_correct': True, 'feedback': 'Bravo! Tu as bien écrit le mot "école".'},
                        {'text': 'écol', 'is_correct': False, 'feedback': 'Il manque une lettre. On écrit "école".'},
                        {'text': 'écolle', 'is_correct': False, 'feedback': 'Tu as ajouté une lettre. On écrit "école".'},
                        {'text': 'écaule', 'is_correct': False, 'feedback': 'Ce n\'est pas la bonne orthographe. On écrit "école".'}
                    ]
                },
                {
                    'text': 'Écris le mot que tu entends.',
                    'question_type': 'fill_blank',
                    'audio': '/static/audio/lapin.mp3',
                    'answers': [
                        {'text': 'lapin', 'is_correct': True, 'feedback': 'Bravo! Tu as bien écrit le mot "lapin".'},
                        {'text': 'lapain', 'is_correct': False, 'feedback': 'Ce n\'est pas la bonne orthographe. On écrit "lapin".'},
                        {'text': 'lappin', 'is_correct': False, 'feedback': 'Tu as ajouté une lettre. On écrit "lapin".'},
                        {'text': 'rapin', 'is_correct': False, 'feedback': 'Ce n\'est pas la bonne orthographe. On écrit "lapin".'}
                    ]
                },
                {
                    'text': 'Écris le mot que tu entends.',
                    'question_type': 'fill_blank',
                    'audio': '/static/audio/voiture.mp3',
                    'answers': [
                        {'text': 'voiture', 'is_correct': True, 'feedback': 'Bravo! Tu as bien écrit le mot "voiture".'},
                        {'text': 'voitur', 'is_correct': False, 'feedback': 'Il manque une lettre. On écrit "voiture".'},
                        {'text': 'voatur', 'is_correct': False, 'feedback': 'Ce n\'est pas la bonne orthographe. On écrit "voiture".'},
                        {'text': 'wouature', 'is_correct': False, 'feedback': 'Ce n\'est pas la bonne orthographe. On écrit "voiture".'}
                    ]
                }
            ]
        }
    ]
    
    created_exercises = []
    
    for exercise_data in exercises:
        exercise = Exercise.objects.create(
            title=exercise_data['title'],
            exercise_type=exercise_data['exercise_type'],
            instructions=exercise_data['instructions'],
            difficulty=exercise_data['difficulty'],
            estimated_time=exercise_data['estimated_time'],
            points=exercise_data['points']
        )
        
        # Create questions and answers
        for question_data in exercise_data['questions']:
            question = Question.objects.create(
                exercise=exercise,
                question_text=question_data['text'],
                question_type=question_data['question_type'],
                audio=question_data.get('audio', None)
            )
            
            # Create answers
            for answer_data in question_data['answers']:
                Answer.objects.create(
                    question=question,
                    answer_text=answer_data['text'],
                    is_correct=answer_data['is_correct'],
                    feedback=answer_data['feedback']
                )
        
        created_exercises.append(exercise)
        print(f"Exercise '{exercise.title}' created")
    
    return created_exercises

def create_dyscalculia_exercises(exercise_types):
    print("Creating dyscalculia exercises...")
    
    # Get dyscalculia exercise types
    number_recognition = exercise_types[3]  # Reconnaissance de nombres
    mental_calculation = exercise_types[4]  # Calcul mental
    problem_solving = exercise_types[5]  # Résolution de problèmes
    
    exercises = [
        # Number recognition exercises
        {
            'title': 'Reconnaître les nombres de 1 à 20',
            'exercise_type': number_recognition,
            'instructions': """
                <p>Dans cet exercice, tu vas t'entraîner à reconnaître les nombres de 1 à 20.</p>
                <p>Pour chaque question, choisis le bon nombre qui correspond à l'image ou à la description.</p>
                <p>Tu peux utiliser le boulier virtuel et la droite numérique pour t'aider.</p>
            """,
            'difficulty': 1,
            'estimated_time': 10,
            'points': 50,
            'questions': [
                {
                    'text': 'Quel nombre est représenté par ces points?',
                    'question_type': 'multiple_choice',
                    'image': '/static/images/number_dots_7.png',
                    'answers': [
                        {'text': '7', 'is_correct': True, 'feedback': 'Bravo! Il y a bien 7 points.'},
                        {'text': '6', 'is_correct': False, 'feedback': 'Ce n\'est pas 6. Compte bien tous les points.'},
                        {'text': '8', 'is_correct': False, 'feedback': 'Ce n\'est pas 8. Compte bien tous les points.'},
                        {'text': '9', 'is_correct': False, 'feedback': 'Ce n\'est pas 9. Compte bien tous les points.'}
                    ]
                },
                {
                    'text': 'Quel est le nombre qui vient juste après 12?',
                    'question_type': 'multiple_choice',
                    'answers': [
                        {'text': '13', 'is_correct': True, 'feedback': 'Bravo! 13 vient juste après 12.'},
                        {'text': '11', 'is_correct': False, 'feedback': '11 vient avant 12, pas après.'},
                        {'text': '14', 'is_correct': False, 'feedback': '14 vient après 13, pas directement après 12.'},
                        {'text': '21', 'is_correct': False, 'feedback': '21 est beaucoup plus grand que 12.'}
                    ]
                },
                {
                    'text': 'Quel nombre est représenté sur l\'abaque?',
                    'question_type': 'multiple_choice',
                    'image': '/static/images/abacus_15.png',
                    'answers': [
                        {'text': '15', 'is_correct': True, 'feedback': 'Bravo! L\'abaque montre bien 15 (1 dizaine et 5 unités).'},
                        {'text': '51', 'is_correct': False, 'feedback': 'Ce n\'est pas 51. Regarde bien: il y a 1 dizaine et 5 unités, donc 15.'},
                        {'text': '6', 'is_correct': False, 'feedback': 'Ce n\'est pas 6. Regarde bien: il y a 1 dizaine et 5 unités, donc 15.'},
                        {'text': '105', 'is_correct': False, 'feedback': 'Ce n\'est pas 105. Regarde bien: il y a 1 dizaine et 5 unités, donc 15.'}
                    ]
                },
                {
                    'text': 'Quel est le nombre qui vient juste avant 10?',
                    'question_type': 'multiple_choice',
                    'answers': [
                        {'text': '9', 'is_correct': True, 'feedback': 'Bravo! 9 vient juste avant 10.'},
                        {'text': '8', 'is_correct': False, 'feedback': '8 vient avant 9, pas directement avant 10.'},
                        {'text': '11', 'is_correct': False, 'feedback': '11 vient après 10, pas avant.'},
                        {'text': '1', 'is_correct': False, 'feedback': '1 est beaucoup plus petit que 10.'}
                    ]
                },
                {
                    'text': 'Quel nombre est écrit en lettres: dix-huit?',
                    'question_type': 'multiple_choice',
                    'answers': [
                        {'text': '18', 'is_correct': True, 'feedback': 'Bravo! "Dix-huit" s\'écrit bien 18 en chiffres.'},
                        {'text': '80', 'is_correct': False, 'feedback': 'Ce n\'est pas 80. "Quatre-vingts" s\'écrit 80 en chiffres.'},
                        {'text': '28', 'is_correct': False, 'feedback': 'Ce n\'est pas 28. "Vingt-huit" s\'écrit 28 en chiffres.'},
                        {'text': '108', 'is_correct': False, 'feedback': 'Ce n\'est pas 108. "Cent huit" s\'écrit 108 en chiffres.'}
                    ]
                }
            ]
        },
        
        # Mental calculation exercises
        {
            'title': 'Additions et soustractions jusqu\'à 20',
            'exercise_type': mental_calculation,
            'instructions': """
                <p>Dans cet exercice, tu vas t'entraîner à faire des additions et des soustractions avec des nombres jusqu'à 20.</p>
                <p>Pour chaque calcul, trouve le résultat.</p>
                <p>Tu peux utiliser le boulier virtuel et la droite numérique pour t'aider.</p>
            """,
            'difficulty': 2,
            'estimated_time': 15,
            'points': 75,
            'questions': [
                {
                    'text': 'Calcule: 5 + 3 = ?',
                    'question_type': 'fill_blank',
                    'answers': [
                        {'text': '8', 'is_correct': True, 'feedback': 'Bravo! 5 + 3 = 8'},
                        {'text': '7', 'is_correct': False, 'feedback': 'Ce n\'est pas 7. Essaie de recompter.'},
                        {'text': '9', 'is_correct': False, 'feedback': 'Ce n\'est pas 9. Essaie de recompter.'},
                        {'text': '2', 'is_correct': False, 'feedback': 'Ce n\'est pas 2. Tu as peut-être fait une soustraction au lieu d\'une addition.'}
                    ]
                },
                {
                    'text': 'Calcule: 10 - 4 = ?',
                    'question_type': 'fill_blank',
                    'answers': [
                        {'text': '6', 'is_correct': True, 'feedback': 'Bravo! 10 - 4 = 6'},
                        {'text': '5', 'is_correct': False, 'feedback': 'Ce n\'est pas 5. Essaie de recompter.'},
                        {'text': '7', 'is_correct': False, 'feedback': 'Ce n\'est pas 7. Essaie de recompter.'},
                        {'text': '14', 'is_correct': False, 'feedback': 'Ce n\'est pas 14. Tu as peut-être fait une addition au lieu d\'une soustraction.'}
                    ]
                },
                {
                    'text': 'Calcule: 7 + 7 = ?',
                    'question_type': 'fill_blank',
                    'answers': [
                        {'text': '14', 'is_correct': True, 'feedback': 'Bravo! 7 + 7 = 14'},
                        {'text': '13', 'is_correct': False, 'feedback': 'Ce n\'est pas 13. Essaie de recompter.'},
                        {'text': '15', 'is_correct': False, 'feedback': 'Ce n\'est pas 15. Essaie de recompter.'},
                        {'text': '0', 'is_correct': False, 'feedback': 'Ce n\'est pas 0. Tu as peut-être fait une soustraction au lieu d\'une addition.'}
                    ]
                },
                {
                    'text': 'Calcule: 15 - 8 = ?',
                    'question_type': 'fill_blank',
                    'answers': [
                        {'text': '7', 'is_correct': True, 'feedback': 'Bravo! 15 - 8 = 7'},
                        {'text': '6', 'is_correct': False, 'feedback': 'Ce n\'est pas 6. Essaie de recompter.'},
                        {'text': '8', 'is_correct': False, 'feedback': 'Ce n\'est pas 8. Essaie de recompter.'},
                        {'text': '23', 'is_correct': False, 'feedback': 'Ce n\'est pas 23. Tu as peut-être fait une addition au lieu d\'une soustraction.'}
                    ]
                },
                {
                    'text': 'Calcule: 9 + 6 = ?',
                    'question_type': 'fill_blank',
                    'answers': [
                        {'text': '15', 'is_correct': True, 'feedback': 'Bravo! 9 + 6 = 15'},
                        {'text': '14', 'is_correct': False, 'feedback': 'Ce n\'est pas 14. Essaie de recompter.'},
                        {'text': '16', 'is_correct': False, 'feedback': 'Ce n\'est pas 16. Essaie de recompter.'},
                        {'text': '3', 'is_correct': False, 'feedback': 'Ce n\'est pas 3. Tu as peut-être fait une soustraction au lieu d\'une addition.'}
                    ]
                }
            ]
        },
        
        # Problem solving exercises
        {
            'title': 'Problèmes simples avec des nombres jusqu\'à 20',
            'exercise_type': problem_solving,
            'instructions': """
                <p>Dans cet exercice, tu vas résoudre des problèmes simples avec des nombres jusqu'à 20.</p>
                <p>Lis attentivement chaque problème, puis trouve la réponse.</p>
                <p>Tu peux utiliser le boulier virtuel et la droite numérique pour t'aider.</p>
            """,
            'difficulty': 3,
            'estimated_time': 20,
            'points': 100,
            'questions': [
                {
                    'text': 'Léa a 5 billes. Son ami lui donne 3 billes de plus. Combien de billes Léa a-t-elle maintenant?',
                    'question_type': 'fill_blank',
                    'answers': [
                        {'text': '8', 'is_correct': True, 'feedback': 'Bravo! 5 + 3 = 8 billes'},
                        {'text': '7', 'is_correct': False, 'feedback': 'Ce n\'est pas 7. Essaie de recompter: 5 + 3 = 8 billes.'},
                        {'text': '9', 'is_correct': False, 'feedback': 'Ce n\'est pas 9. Essaie de recompter: 5 + 3 = 8 billes.'},
                        {'text': '2', 'is_correct': False, 'feedback': 'Ce n\'est pas 2. Tu as peut-être fait une soustraction au lieu d\'une addition: 5 + 3 = 8 billes.'}
                    ]
                },
                {
                    'text': 'Tom a 12 bonbons. Il en mange 4. Combien de bonbons lui reste-t-il?',
                    'question_type': 'fill_blank',
                    'answers': [
                        {'text': '8', 'is_correct': True, 'feedback': 'Bravo! 12 - 4 = 8 bonbons'},
                        {'text': '7', 'is_correct': False, 'feedback': 'Ce n\'est pas 7. Essaie de recompter: 12 - 4 = 8 bonbons.'},
                        {'text': '9', 'is_correct': False, 'feedback': 'Ce n\'est pas 9. Essaie de recompter: 12 - 4 = 8 bonbons.'},
                        {'text': '16', 'is_correct': False, 'feedback': 'Ce n\'est pas 16. Tu as peut-être fait une addition au lieu d\'une soustraction: 12 - 4 = 8 bonbons.'}
                    ]
                },
                {
                    'text': 'Dans un panier, il y a 7 pommes rouges et 6 pommes vertes. Combien y a-t-il de pommes en tout?',
                    'question_type': 'fill_blank',
                    'answers': [
                        {'text': '13', 'is_correct': True, 'feedback': 'Bravo! 7 + 6 = 13 pommes'},
                        {'text': '12', 'is_correct': False, 'feedback': 'Ce n\'est pas 12. Essaie de recompter: 7 + 6 = 13 pommes.'},
                        {'text': '14', 'is_correct': False, 'feedback': 'Ce n\'est pas 14. Essaie de recompter: 7 + 6 = 13 pommes.'},
                        {'text': '1', 'is_correct': False, 'feedback': 'Ce n\'est pas 1. Tu as peut-être fait une soustraction au lieu d\'une addition: 7 + 6 = 13 pommes.'}
                    ]
                },
                {
                    'text': 'Julie a 15 euros. Elle achète un livre qui coûte 8 euros. Combien d\'argent lui reste-t-il?',
                    'question_type': 'fill_blank',
                    'answers': [
                        {'text': '7', 'is_correct': True, 'feedback': 'Bravo! 15 - 8 = 7 euros'},
                        {'text': '6', 'is_correct': False, 'feedback': 'Ce n\'est pas 6. Essaie de recompter: 15 - 8 = 7 euros.'},
                        {'text': '8', 'is_correct': False, 'feedback': 'Ce n\'est pas 8. Essaie de recompter: 15 - 8 = 7 euros.'},
                        {'text': '23', 'is_correct': False, 'feedback': 'Ce n\'est pas 23. Tu as peut-être fait une addition au lieu d\'une soustraction: 15 - 8 = 7 euros.'}
                    ]
                },
                {
                    'text': 'Dans une classe, il y a 20 élèves. 9 élèves sont des filles. Combien y a-t-il de garçons?',
                    'question_type': 'fill_blank',
                    'answers': [
                        {'text': '11', 'is_correct': True, 'feedback': 'Bravo! 20 - 9 = 11 garçons'},
                        {'text': '10', 'is_correct': False, 'feedback': 'Ce n\'est pas 10. Essaie de recompter: 20 - 9 = 11 garçons.'},
                        {'text': '12', 'is_correct': False, 'feedback': 'Ce n\'est pas 12. Essaie de recompter: 20 - 9 = 11 garçons.'},
                        {'text': '29', 'is_correct': False, 'feedback': 'Ce n\'est pas 29. Tu as peut-être fait une addition au lieu d\'une soustraction: 20 - 9 = 11 garçons.'}
                    ]
                }
            ]
        }
    ]
    
    created_exercises = []
    
    for exercise_data in exercises:
        exercise = Exercise.objects.create(
            title=exercise_data['title'],
            exercise_type=exercise_data['exercise_type'],
            instructions=exercise_data['instructions'],
            difficulty=exercise_data['difficulty'],
            estimated_time=exercise_data['estimated_time'],
            points=exercise_data['points']
        )
        
        # Create questions and answers
        for question_data in exercise_data['questions']:
            question = Question.objects.create(
                exercise=exercise,
                question_text=question_data['text'],
                question_type=question_data['question_type'],
                image=question_data.get('image', None)
            )
            
            # Create answers
            for answer_data in question_data['answers']:
                Answer.objects.create(
                    question=question,
                    answer_text=answer_data['text'],
                    is_correct=answer_data['is_correct'],
                    feedback=answer_data['feedback']
                )
        
        created_exercises.append(exercise)
        print(f"Exercise '{exercise.title}' created")
    
    return created_exercises

def create_achievements():
    print("Creating achievements...")
    
    achievements = [
        {
            'name': 'Premier pas',
            'description': 'Compléter ton premier exercice',
            'icon': 'fa-shoe-prints',
            'points': 10
        },
        {
            'name': 'Apprenti lecteur',
            'description': 'Compléter 5 exercices de lecture',
            'icon': 'fa-book-open',
            'points': 25
        },
        {
            'name': 'Maître des nombres',
            'description': 'Compléter 5 exercices de mathématiques',
            'icon': 'fa-sort-numeric-up',
            'points': 25
        },
        {
            'name': 'Persévérance',
            'description': 'S\'entraîner 5 jours de suite',
            'icon': 'fa-calendar-check',
            'points': 50
        },
        {
            'name': 'Score parfait',
            'description': 'Obtenir un score parfait sur un exercice',
            'icon': 'fa-star',
            'points': 30
        },
        {
            'name': 'Explorateur',
            'description': 'Essayer tous les types d\'exercices',
            'icon': 'fa-compass',
            'points': 40
        },
        {
            'name': 'Champion',
            'description': 'Atteindre le niveau 5',
            'icon': 'fa-trophy',
            'points': 100
        }
    ]
    
    created_achievements = []
    
    for data in achievements:
        achievement, created = Achievement.objects.get_or_create(
            name=data['name'],
            defaults={
                'description': data['description'],
                'icon': data['icon'],
                'points': data['points']
            }
        )
        
        if created:
            print(f"Achievement '{data['name']}' created")
        
        created_achievements.append(achievement)
    
    return created_achievements

def create_exercise_attempts(users, exercises):
    print("Creating exercise attempts...")
    
    # Get child users
    children = [user for user in users['children']]
    
    # Create attempts for each child
    for child in children:
        # Get child profile
        child_profile = ChildProfile.objects.get(user=child)
        
        # Determine which exercises to attempt based on child's profile
        if child_profile.has_dyslexia and child_profile.has_dyscalculia:
            # Both dyslexia and dyscalculia
            child_exercises = exercises
        elif child_profile.has_dyslexia:
            # Only dyslexia
            child_exercises = [ex for ex in exercises if ex.exercise_type.disorder_type == 'dyslexia']
        elif child_profile.has_dyscalculia:
            # Only dyscalculia
            child_exercises = [ex for ex in exercises if ex.exercise_type.disorder_type == 'dyscalculia']
        else:
            # No disorders (shouldn't happen, but just in case)
            child_exercises = exercises
        
        # Create attempts for a random subset of exercises
        num_attempts = min(len(child_exercises), random.randint(3, 5))
        for i in range(num_attempts):
            exercise = child_exercises[i]
            
            # Create attempt
            attempt = ExerciseAttempt.objects.create(
                user=child,
                exercise=exercise,
                started_at=timezone.now() - timedelta(days=random.randint(0, 7)),
                completed_at=timezone.now() - timedelta(days=random.randint(0, 6)),
                score=random.randint(5, 10) * 10,  # Score between 50 and 100
                max_score=100,
                time_spent=random.randint(5, 15) * 60  # Time spent in seconds
            )
            
            # Create responses for each question
            for question in exercise.questions.all():
                # Get correct answer
                correct_answer = question.answers.filter(is_correct=True).first()
                
                # Determine if response is correct (80% chance)
                is_correct = random.random() < 0.8
                
                if is_correct:
                    # Correct response
                    QuestionResponse.objects.create(
                        attempt=attempt,
                        question=question,
                        answer=correct_answer,
                        is_correct=True,
                        response_time=random.randint(5, 30)  # Response time in seconds
                    )
                else:
                    # Incorrect response
                    incorrect_answer = question.answers.filter(is_correct=False).first()
                    QuestionResponse.objects.create(
                        attempt=attempt,
                        question=question,
                        answer=incorrect_answer,
                        is_correct=False,
                        response_time=random.randint(10, 45)  # Response time in seconds
                    )
            
            print(f"Created attempt for {child.username} on exercise '{exercise.title}'")
            
            # Update child's points
            child_profile.points += attempt.score
            child_profile.save()
    
    return True

def create_progress_records(users):
    print("Creating progress records...")
    
    # Get child users
    children = [user for user in users['children']]
    
    # Get exercise types
    exercise_types = ExerciseType.objects.all()
    
    # Create progress records for each child
    for child in children:
        # Get child profile
        child_profile = ChildProfile.objects.get(user=child)
        
        # Determine which exercise types to track based on child's profile
        if child_profile.has_dyslexia and child_profile.has_dyscalculia:
            # Both dyslexia and dyscalculia
            child_exercise_types = exercise_types
        elif child_profile.has_dyslexia:
            # Only dyslexia
            child_exercise_types = exercise_types.filter(disorder_type='dyslexia')
        elif child_profile.has_dyscalculia:
            # Only dyscalculia
            child_exercise_types = exercise_types.filter(disorder_type='dyscalculia')
        else:
            # No disorders (shouldn't happen, but just in case)
            child_exercise_types = exercise_types
        
        # Create progress records for each exercise type
        for exercise_type in child_exercise_types:
            # Get attempts for this exercise type
            attempts = ExerciseAttempt.objects.filter(
                user=child,
                exercise__exercise_type=exercise_type
            )
            
            # Calculate skill level based on attempts
            if attempts.exists():
                avg_score = sum([a.score for a in attempts]) / attempts.count()
                skill_level = min(10, max(1, int(avg_score / 10)))
            else:
                skill_level = 1
            
            # Create progress record
            ProgressRecord.objects.create(
                user=child,
                exercise_type=exercise_type,
                skill_level=skill_level,
                exercises_completed=attempts.count(),
                last_updated=timezone.now()
            )
            
            print(f"Created progress record for {child.username} on exercise type '{exercise_type.name}'")
    
    return True

def create_user_achievements(users, achievements):
    print("Creating user achievements...")
    
    # Get child users
    children = [user for user in users['children']]
    
    # Create achievements for each child
    for child in children:
        # Get attempts for this child
        attempts = ExerciseAttempt.objects.filter(user=child)
        
        if attempts.exists():
            # First achievement: Premier pas
            UserAchievement.objects.create(
                user=child,
                achievement=achievements[0],
                date_earned=attempts.order_by('completed_at').first().completed_at
            )
            print(f"Awarded 'Premier pas' achievement to {child.username}")
            
            # Check for perfect score
            perfect_score_attempts = attempts.filter(score=100)
            if perfect_score_attempts.exists():
                # Fifth achievement: Score parfait
                UserAchievement.objects.create(
                    user=child,
                    achievement=achievements[4],
                    date_earned=perfect_score_attempts.order_by('completed_at').first().completed_at
                )
                print(f"Awarded 'Score parfait' achievement to {child.username}")
            
            # Check for reading exercises
            reading_attempts = attempts.filter(exercise__exercise_type__category__name='Lecture')
            if reading_attempts.count() >= 2:
                # Second achievement: Apprenti lecteur
                UserAchievement.objects.create(
                    user=child,
                    achievement=achievements[1],
                    date_earned=reading_attempts.order_by('-completed_at').first().completed_at
                )
                print(f"Awarded 'Apprenti lecteur' achievement to {child.username}")
            
            # Check for math exercises
            math_attempts = attempts.filter(
                exercise__exercise_type__category__name__in=['Nombres', 'Calcul', 'Problèmes']
            )
            if math_attempts.count() >= 2:
                # Third achievement: Maître des nombres
                UserAchievement.objects.create(
                    user=child,
                    achievement=achievements[2],
                    date_earned=math_attempts.order_by('-completed_at').first().completed_at
                )
                print(f"Awarded 'Maître des nombres' achievement to {child.username}")
    
    return True

def main():
    # Create users
    users = create_users()
    
    # Create categories
    categories = create_categories()
    
    # Create exercise types
    exercise_types = create_exercise_types(categories)
    
    # Create exercises
    dyslexia_exercises = create_dyslexia_exercises(exercise_types)
    dyscalculia_exercises = create_dyscalculia_exercises(exercise_types)
    all_exercises = dyslexia_exercises + dyscalculia_exercises
    
    # Create achievements
    achievements = create_achievements()
    
    # Create exercise attempts
    create_exercise_attempts(users, all_exercises)
    
    # Create progress records
    create_progress_records(users)
    
    # Create user achievements
    create_user_achievements(users, achievements)
    
    print("Demo data creation completed successfully!")

if __name__ == "__main__":
    main()
