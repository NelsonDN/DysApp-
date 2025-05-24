# Guide de contribution

Merci de votre intérêt pour contribuer à notre application pour enfants dyslexiques et dyscalculiques ! Ce document vous guidera à travers le processus de contribution.

## Prérequis

- Python 3.10 ou supérieur
- Django 5.0 ou supérieur
- Git

## Installation pour le développement

1. Forkez le dépôt sur GitHub
2. Clonez votre fork localement :
\`\`\`bash
git clone https://github.com/NelsonDN/DysApp-.git
cd dyslexia-projects
\`\`\`

4. Créez un environnement virtuel et activez-le :
\`\`\`bash
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
\`\`\`

5. Installez les dépendances de développement :
\`\`\`bash
pip install -r requirements-dev.txt
\`\`\`

6. Appliquez les migrations :
\`\`\`bash
python manage.py migrate
\`\`\`

7. Créez un superutilisateur :
\`\`\`bash
python manage.py createsuperuser
\`\`\`

8. Lancez le serveur de développement :
\`\`\`bash
python manage.py runserver
\`\`\`

## Structure du projet

- `accounts/` : Gestion des utilisateurs et des profils
- `core/` : Application principale
- `dashboard/` : Tableaux de bord
- `exercises/` : Exercices pour dyslexie et dyscalculie
- `progress/` : Suivi des progrès et récompenses
- `static/` : Fichiers statiques (CSS, JS, images)
- `templates/` : Templates HTML

## Workflow de contribution

1. Créez une branche pour votre fonctionnalité ou correction :
\`\`\`bash
git checkout -b feature/nom-de-la-fonctionnalite
\`\`\`

2. Effectuez vos modifications et assurez-vous que les tests passent :
\`\`\`bash
python manage.py test
\`\`\`

3. Exécutez les vérifications de style de code :
\`\`\`bash
flake8
black .
\`\`\`

4. Committez vos changements :
\`\`\`bash
git commit -m "Description de vos changements"
\`\`\`

5. Poussez votre branche vers votre fork :
\`\`\`bash
git push origin feature/nom-de-la-fonctionnalite
\`\`\`

6. Créez une Pull Request sur GitHub

## Conventions de code

- Suivez les conventions PEP 8 pour le code Python
- Utilisez des noms de variables et de fonctions explicites
- Écrivez des docstrings pour toutes les classes et fonctions
- Ajoutez des commentaires pour expliquer le code complexe
- Utilisez des messages de commit clairs et descriptifs

## Tests

Tous les nouveaux développements doivent être accompagnés de tests unitaires. Nous utilisons le framework de test intégré à Django.

Pour exécuter les tests :
\`\`\`bash
python manage.py test
\`\`\`

Pour exécuter les tests avec couverture de code :
\`\`\`bash
coverage run --source='.' manage.py test
coverage report
\`\`\`

## Documentation

La documentation est essentielle pour ce projet. Veuillez documenter :
- Toutes les nouvelles fonctionnalités
- Les modifications apportées aux fonctionnalités existantes
- Les changements dans l'API ou les modèles de données

## Rapport de bugs

Si vous trouvez un bug, veuillez créer une issue sur GitHub avec les informations suivantes :
- Description détaillée du bug
- Étapes pour reproduire le bug
- Comportement attendu
- Captures d'écran (si applicable)
- Environnement (navigateur, système d'exploitation, etc.)

## Propositions de fonctionnalités

Les propositions de nouvelles fonctionnalités sont les bienvenues. Veuillez créer une issue sur GitHub avec les informations suivantes :
- Description détaillée de la fonctionnalité
- Justification de la fonctionnalité (pourquoi est-elle nécessaire ?)
- Exemples d'utilisation
- Maquettes ou wireframes (si applicable)

## Accessibilité

L'accessibilité est une priorité pour ce projet. Toutes les contributions doivent respecter les normes WCAG 2.1 niveau AA. Veuillez vous assurer que :
- Le contenu est perceptible pour tous les utilisateurs
- L'interface est opérable par tous les utilisateurs
- Le contenu est compréhensible pour tous les utilisateurs
- Le contenu est robuste et compatible avec les technologies d'assistance

## Licence

En contribuant à ce projet, vous acceptez que vos contributions soient sous la même licence que le projet (voir le fichier LICENSE).

## Contact

Si vous avez des questions ou besoin d'aide, n'hésitez pas à contacter l'équipe de développement à l'adresse email : nelsondada10@gmail.com


## 15. Fichiers de configuration principaux

Ajoutons les fichiers de configuration principaux pour le projet Django:

