// /**
//  * Fonctions spécifiques pour les exercices de dyslexie
//  */

// // Fonction pour mélanger un tableau
// function shuffleArray(array) {
//   for (let i = array.length - 1; i > 0; i--) {
//     const j = Math.floor(Math.random() * (i + 1))
//     ;[array[i], array[j]] = [array[j], array[i]]
//   }
//   return array
// }

// /**
//  * Crée un exercice de reconnaissance de lettres
//  * @param {Object} container - Élément DOM contenant l'exercice
//  * @param {Array} letters - Tableau de lettres à reconnaître
//  * @param {Function} onComplete - Fonction à exécuter lorsque l'exercice est terminé
//  */
// function createLetterRecognitionExercise(container, letters, onComplete) {
//   // Vider le conteneur
//   container.innerHTML = ""

//   // Créer l'élément pour afficher la lettre
//   var letterDisplay = document.createElement("div")
//   letterDisplay.className = "letter-display"
//   container.appendChild(letterDisplay)

//   // Créer le conteneur pour les options
//   var optionsContainer = document.createElement("div")
//   optionsContainer.className = "options-container"
//   container.appendChild(optionsContainer)

//   // Variables pour suivre l'état de l'exercice
//   var currentIndex = 0
//   var score = 0

//   // Fonction pour afficher une lettre
//   function displayLetter() {
//     if (currentIndex >= letters.length) {
//       // L'exercice est terminé
//       onComplete(score, letters.length)
//       return
//     }

//     var currentLetter = letters[currentIndex]
//     letterDisplay.textContent = currentLetter.letter

//     // Créer les options (la lettre correcte et des lettres similaires)
//     var options = [currentLetter.letter]

//     // Ajouter les lettres similaires comme distracteurs
//     currentLetter.similar.forEach((similarLetter) => {
//       options.push(similarLetter)
//     })

//     // Mélanger les options
//     options = shuffleArray(options)

//     // Afficher les options
//     optionsContainer.innerHTML = ""
//     options.forEach((option) => {
//       var button = document.createElement("button")
//       button.className = "btn btn-lg btn-outline-primary m-2"
//       button.textContent = option

//       button.addEventListener("click", () => {
//         // Vérifier si la réponse est correcte
//         var isCorrect = option === currentLetter.letter

//         // Mettre à jour le score
//         if (isCorrect) {
//           score++
//           button.classList.remove("btn-outline-primary")
//           button.classList.add("btn-success")
//         } else {
//           button.classList.remove("btn-outline-primary")
//           button.classList.add("btn-danger")

//           // Mettre en évidence la bonne réponse
//           var buttons = optionsContainer.querySelectorAll("button")
//           buttons.forEach((btn) => {
//             if (btn.textContent === currentLetter.letter) {
//               btn.classList.remove("btn-outline-primary")
//               btn.classList.add("btn-success")
//             }
//           })
//         }

//         // Désactiver tous les boutons
//         var buttonsList = optionsContainer.querySelectorAll("button")
//         buttonsList.forEach((btn) => {
//           btn.disabled = true
//         })

//         // Passer à la lettre suivante après un délai
//         setTimeout(() => {
//           currentIndex++
//           displayLetter()
//         }, 1500)
//       })

//       optionsContainer.appendChild(button)
//     })
//   }

//   // Commencer l'exercice
//   displayLetter()
// }

// /**
//  * Crée un exercice de lecture de mots
//  * @param {Object} container - Élément DOM contenant l'exercice
//  * @param {Array} words - Tableau de mots à lire
//  * @param {Function} onComplete - Fonction à exécuter lorsque l'exercice est terminé
//  */
// function createWordReadingExercise(container, words, onComplete) {
//   // Vider le conteneur
//   container.innerHTML = ""

//   // Créer l'élément pour afficher le mot
//   var wordDisplay = document.createElement("div")
//   wordDisplay.className = "word-display"
//   container.appendChild(wordDisplay)

//   // Créer le conteneur pour les options
//   var optionsContainer = document.createElement("div")
//   optionsContainer.className = "options-container"
//   container.appendChild(optionsContainer)

//   // Variables pour suivre l'état de l'exercice
//   var currentIndex = 0
//   var score = 0

//   // Fonction pour afficher un mot
//   function displayWord() {
//     if (currentIndex >= words.length) {
//       // L'exercice est terminé
//       onComplete(score, words.length)
//       return
//     }

//     var currentWord = words[currentIndex]
//     wordDisplay.textContent = currentWord.word

//     // Créer les options (l'image correcte et des images incorrectes)
//     var options = [currentWord.correctImage]

//     // Ajouter les images incorrectes comme distracteurs
//     currentWord.incorrectImages.forEach((incorrectImage) => {
//       options.push(incorrectImage)
//     })

//     // Mélanger les options
//     options = shuffleArray(options)

//     // Afficher les options
//     optionsContainer.innerHTML = ""
//     options.forEach((option) => {
//       var imageContainer = document.createElement("div")
//       imageContainer.className = "image-option m-2"

//       var image = document.createElement("img")
//       image.src = option.src
//       image.alt = option.alt
//       image.className = "img-fluid"

//       imageContainer.appendChild(image)
//       optionsContainer.appendChild(imageContainer)

//       imageContainer.addEventListener("click", () => {
//         // Vérifier si la réponse est correcte
//         var isCorrect = option === currentWord.correctImage

//         // Mettre à jour le score
//         if (isCorrect) {
//           score++
//           imageContainer.classList.add("correct-answer")
//         } else {
//           imageContainer.classList.add("incorrect-answer")

//           // Mettre en évidence la bonne réponse
//           var containers = optionsContainer.querySelectorAll(".image-option")
//           containers.forEach((container, index) => {
//             if (options[index] === currentWord.correctImage) {
//               container.classList.add("correct-answer")
//             }
//           })
//         }

//         // Désactiver tous les conteneurs d'images
//         var containersList = optionsContainer.querySelectorAll(".image-option")
//         containersList.forEach((container) => {
//           container.style.pointerEvents = "none"
//         })

//         // Passer au mot suivant après un délai
//         setTimeout(() => {
//           currentIndex++
//           displayWord()
//         }, 1500)
//       })
//     })
//   }

//   // Commencer l'exercice
//   displayWord()
// }

// /**
//  * Crée un exercice de complétion de phrases
//  * @param {Object} container - Élément DOM contenant l'exercice
//  * @param {Array} sentences - Tableau de phrases à compléter
//  * @param {Function} onComplete - Fonction à exécuter lorsque l'exercice est terminé
//  */
// function createSentenceCompletionExercise(container, sentences, onComplete) {
//   // Vider le conteneur
//   container.innerHTML = ""

//   // Créer l'élément pour afficher la phrase
//   var sentenceDisplay = document.createElement("div")
//   sentenceDisplay.className = "sentence-display"
//   container.appendChild(sentenceDisplay)

//   // Créer le conteneur pour les options
//   var optionsContainer = document.createElement("div")
//   optionsContainer.className = "options-container"
//   container.appendChild(optionsContainer)

//   // Créer l'élément pour le feedback
//   var feedbackDisplay = document.createElement("div")
//   feedbackDisplay.className = "feedback-display mt-3"
//   container.appendChild(feedbackDisplay)

//   // Variables pour suivre l'état de l'exercice
//   var currentIndex = 0
//   var score = 0

//   // Fonction pour afficher une phrase
//   function displaySentence() {
//     if (currentIndex >= sentences.length) {
//       // L'exercice est terminé
//       onComplete(score, sentences.length)
//       return
//     }

//     var currentSentence = sentences[currentIndex]

//     // Construire la phrase avec un espace pour le mot manquant
//     var sentenceText = currentSentence.text.replace("___", '<span class="missing-word">_____</span>')
//     sentenceDisplay.innerHTML = sentenceText

//     // Créer les options (le mot correct et des mots incorrects)
//     var options = [currentSentence.correctWord]

//     // Ajouter les mots incorrects comme distracteurs
//     currentSentence.incorrectWords.forEach((incorrectWord) => {
//       options.push(incorrectWord)
//     })

//     // Mélanger les options
//     options = shuffleArray(options)

//     // Afficher les options
//     optionsContainer.innerHTML = ""
//     options.forEach((option) => {
//       var button = document.createElement("button")
//       button.className = "btn btn-outline-primary m-2"
//       button.textContent = option

//       button.addEventListener("click", () => {
//         // Vérifier si la réponse est correcte
//         var isCorrect = option === currentSentence.correctWord

//         // Mettre à jour le score
//         if (isCorrect) {
//           score++
//           button.classList.remove("btn-outline-primary")
//           button.classList.add("btn-success")
//           feedbackDisplay.innerHTML = '<div class="alert alert-success">Bonne réponse !</div>'
//         } else {
//           button.classList.remove("btn-outline-primary")
//           button.classList.add("btn-danger")
//           feedbackDisplay.innerHTML =
//             '<div class="alert alert-danger">Mauvaise réponse. Le mot correct est "' +
//             currentSentence.correctWord +
//             '".</div>'

//           // Mettre en évidence la bonne réponse
//           var buttons = optionsContainer.querySelectorAll("button")
//           buttons.forEach((btn) => {
//             if (btn.textContent === currentSentence.correctWord) {
//               btn.classList.remove("btn-outline-primary")
//               btn.classList.add("btn-success")
//             }
//           })
//         }

//         // Remplacer le mot manquant par le mot correct
//         var sentenceText = currentSentence.text.replace(
//           "___",
//           '<span class="correct-word">' + currentSentence.correctWord + "</span>",
//         )
//         sentenceDisplay.innerHTML = sentenceText

//         // Désactiver tous les boutons
//         var buttonsList = optionsContainer.querySelectorAll("button")
//         buttonsList.forEach((btn) => {
//           btn.disabled = true
//         })

//         // Passer à la phrase suivante après un délai
//         setTimeout(() => {
//           currentIndex++
//           displaySentence()
//         }, 2000)
//       })

//       optionsContainer.appendChild(button)
//     })
//   }

//   // Commencer l'exercice
//   displaySentence()
// }
/**
 * Fonctions spécifiques pour les exercices de dyslexie
 */

document.addEventListener("DOMContentLoaded", function() {
  // Initialiser l'exercice si on est sur une page d'exercice
  if (document.getElementById('exerciseContainer')) {
    initializeExercise();
  }
});

/**
 * Initialise l'exercice
 */
function initializeExercise() {
  const startButton = document.querySelector('button[id^="commencer"]');
  if (startButton) {
    startButton.addEventListener('click', function() {
      // Cacher les instructions et afficher la première question
      document.querySelector('[id^="instructions"]').style.display = 'none';
      document.querySelector('[id^="question"]').style.display = 'block';
      
      // Initialiser les éléments interactifs
      initializeSyllables();
      initializeAudioButtons();
      initializeAnswerButtons();
    });
  }
  
  // Initialiser le bouton de validation
  const validateButton = document.getElementById('valider');
  if (validateButton) {
    validateButton.addEventListener('click', validateAnswer);
  }
  
  // Initialiser les boutons de navigation
  const prevButton = document.getElementById('precedent');
  if (prevButton) {
    prevButton.addEventListener('click', goToPreviousQuestion);
  }
}

/**
 * Initialise les syllabes cliquables
 */
function initializeSyllables() {
  const syllables = document.querySelectorAll('.syllable');
  syllables.forEach(syllable => {
    syllable.addEventListener('click', function() {
      // Jouer le son de la syllabe
      const audio = new Audio(`/static/audio/syllables/${syllable.textContent.trim()}.mp3`);
      audio.play();
      
      // Mettre en évidence la syllabe
      syllable.classList.add('syllable-highlight');
      setTimeout(() => {
        syllable.classList.remove('syllable-highlight');
      }, 500);
    });
  });
}

/**
 * Initialise les boutons audio
 */
function initializeAudioButtons() {
  const audioButtons = document.querySelectorAll('.audio-button');
  audioButtons.forEach(button => {
    button.addEventListener('click', function() {
      const audioSrc = this.getAttribute('data-audio');
      if (audioSrc) {
        const audio = new Audio(audioSrc);
        audio.play();
      }
    });
  });
}

/**
 * Initialise les boutons de réponse
 */
function initializeAnswerButtons() {
  const answerButtons = document.querySelectorAll('input[type="radio"], .answer-option');
  answerButtons.forEach(button => {
    button.addEventListener('click', function() {
      // Activer le bouton de validation
      document.getElementById('valider').disabled = false;
    });
  });
  
  // Pour les champs texte
  const textInputs = document.querySelectorAll('input[type="text"]');
  textInputs.forEach(input => {
    input.addEventListener('input', function() {
      // Activer le bouton de validation si le champ n'est pas vide
      document.getElementById('valider').disabled = this.value.trim() === '';
    });
  });
}

/**
 * Valide la réponse actuelle
 */
function validateAnswer() {
  // Récupérer l'ID de la tentative et l'index de la question
  const attemptId = document.getElementById('exerciseContainer').getAttribute('data-attempt-id');
  const questionIndex = document.querySelector('.active-question').getAttribute('data-index');
  
  // Récupérer la réponse
  let answer = null;
  let textResponse = '';
  
  const selectedRadio = document.querySelector('input[type="radio"]:checked');
  if (selectedRadio) {
    answer = selectedRadio.value;
  }
  
  const textInput = document.querySelector('input[type="text"]');
  if (textInput) {
    textResponse = textInput.value.trim();
  }
  
  // Désactiver le bouton de validation
  document.getElementById('valider').disabled = true;
  document.getElementById('valider').innerHTML = '<i class="fas fa-spinner fa-spin"></i> Validation...';
  
  // Envoyer la réponse
  fetch(`/exercises/attempt/${attemptId}/submit/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
      question_id: questionIndex,
      answer_id: answer,
      text_response: textResponse
    })
  })
  .then(response => response.json())
  .then(data => {
    // Afficher le feedback
    showFeedback(data.is_correct, data.feedback);
    
    // Activer le bouton suivant
    document.getElementById('suivant').disabled = false;
    
    // Désactiver les options de réponse
    disableAnswerOptions();
  })
  .catch(error => {
    console.error('Erreur lors de la soumission de la réponse:', error);
    alert('Une erreur est survenue lors de la validation de votre réponse.');
    
    // Réactiver le bouton de validation
    document.getElementById('valider').disabled = false;
    document.getElementById('valider').innerHTML = 'Valider';
  });
}

/**
 * Affiche un feedback après la validation
 */
function showFeedback(isCorrect, feedbackText) {
  const feedbackContainer = document.getElementById('feedbackContainer');
  if (!feedbackContainer) return;
  
  let feedbackClass = isCorrect ? 'alert-success' : 'alert-danger';
  let feedbackIcon = isCorrect ? 'fa-check-circle' : 'fa-times-circle';
  let feedbackTitle = isCorrect ? 'Bonne réponse !' : 'Mauvaise réponse';
  
  feedbackContainer.innerHTML = `
    <div class="alert ${feedbackClass}">
      <h5><i class="fas ${feedbackIcon}"></i> ${feedbackTitle}</h5>
      <p>${feedbackText || ''}</p>
    </div>
  `;
  
  feedbackContainer.style.display = 'block';
}

/**
 * Désactive les options de réponse après validation
 */
function disableAnswerOptions() {
  // Désactiver les boutons radio
  const radioButtons = document.querySelectorAll('input[type="radio"]');
  radioButtons.forEach(radio => {
    radio.disabled = true;
  });
  
  // Désactiver les champs texte
  const textInputs = document.querySelectorAll('input[type="text"]');
  textInputs.forEach(input => {
    input.disabled = true;
  });
  
  // Désactiver les options cliquables
  const clickableOptions = document.querySelectorAll('.answer-option');
  clickableOptions.forEach(option => {
    option.style.pointerEvents = 'none';
    option.classList.add('disabled');
  });
}

/**
 * Passe à la question suivante
 */
function goToNextQuestion() {
  // Récupérer l'ID de la tentative et l'index de la question actuelle
  const attemptId = document.getElementById('exerciseContainer').getAttribute('data-attempt-id');
  const currentQuestion = document.querySelector('.active-question');
  const currentIndex = parseInt(currentQuestion.getAttribute('data-index'));
  const nextIndex = currentIndex + 1;
  
  // Charger la question suivante
  loadQuestion(attemptId, nextIndex);
}

/**
 * Revient à la question précédente
 */
function goToPreviousQuestion() {
  // Récupérer l'ID de la tentative et l'index de la question actuelle
  const attemptId = document.getElementById('exerciseContainer').getAttribute('data-attempt-id');
  const currentQuestion = document.querySelector('.active-question');
  const currentIndex = parseInt(currentQuestion.getAttribute('data-index'));
  const prevIndex = currentIndex - 1;
  
  if (prevIndex >= 0) {
    // Charger la question précédente
    loadQuestion(attemptId, prevIndex);
  }
}

/**
 * Charge une question spécifique
 */
function loadQuestion(attemptId, questionIndex) {
  // Afficher le chargement
  document.getElementById('loadingContainer').style.display = 'block';
  document.getElementById('questionContainer').style.display = 'none';
  document.getElementById('feedbackContainer').style.display = 'none';
  
  // Récupérer la question depuis l'API
  fetch(`/exercises/attempt/${attemptId}/question/${questionIndex}/`)
    .then(response => response.json())
    .then(data => {
      if (data.type === 'error') {
        showError(data.message);
        return;
      }
      
      // Mettre à jour l'interface
      updateQuestionUI(data);
      
      // Cacher le chargement
      document.getElementById('loadingContainer').style.display = 'none';
      document.getElementById('questionContainer').style.display = 'block';
    })
    .catch(error => {
      console.error('Erreur lors du chargement de la question:', error);
      showError('Une erreur est survenue lors du chargement de la question.');
    });
}

/**
 * Met à jour l'interface pour afficher une question
 */
function updateQuestionUI(questionData) {
  // Mettre à jour le compteur de questions
  document.getElementById('questionCounter').textContent = `Question ${questionData.current_index + 1}/${questionData.total_questions}`;
  
  // Mettre à jour la barre de progression
  const progress = ((questionData.current_index + 1) / questionData.total_questions) * 100;
  document.getElementById('exerciseProgress').style.width = `${progress}%`;
  
  // Afficher la question
  const questionContainer = document.getElementById('questionContainer');
  questionContainer.innerHTML = '';
  questionContainer.setAttribute('data-index', questionData.current_index);
  questionContainer.classList.add('active-question');
  
  // Construire le HTML de la question selon son type
  let html = `<div class="question-text">${questionData.text}</div>`;
  
  // Ajouter l'image si présente
  if (questionData.image) {
    html += `<div class="question-image"><img src="${questionData.image}" alt="Image de la question"></div>`;
  }
  
  // Ajouter l'audio si présent
  if (questionData.audio) {
    html += `
      <div class="question-audio mt-3 mb-3">
        <button class="btn btn-outline-primary audio-button" data-audio="${questionData.audio}">
          <i class="fas fa-volume-up"></i> Écouter
        </button>
      </div>
    `;
  }
  
  // Ajouter les options de réponse selon le type de question
  html += '<div class="answers-container mt-4">';
  
  if (questionData.question_type === 'multiple_choice' || questionData.question_type === 'true_false') {
    html += '<div class="list-group">';
    questionData.answers.forEach(answer => {
      html += `
        <label class="list-group-item list-group-item-action">
          <input type="radio" name="answer" value="${answer.id}" class="me-2">
          ${answer.text}
        </label>
      `;
    });
    html += '</div>';
  } else if (questionData.question_type === 'fill_blank') {
    html += `
      <div class="form-group">
        <input type="text" class="form-control" id="textAnswer" placeholder="Votre réponse">
      </div>
    `;
  }
  
  html += '</div>'; // answers-container
  
  // Ajouter les boutons de navigation
  html += `
    <div class="exercise-actions mt-4 text-center">
      <button id="precedent" class="btn btn-outline-secondary me-2" ${questionData.current_index === 0 ? 'disabled' : ''}>
        <i class="fas fa-arrow-left"></i> Précédent
      </button>
      <button id="valider" class="btn btn-success me-2" disabled>
        Valider
      </button>
      <button id="suivant" class="btn btn-primary" disabled>
        Suivant <i class="fas fa-arrow-right"></i>
      </button>
    </div>
  `;
  
  // Insérer le HTML dans le conteneur
  questionContainer.innerHTML = html;
  
  // Initialiser les éléments interactifs
  initializeSyllables();
  initializeAudioButtons();
  initializeAnswerButtons();
  
  // Ajouter l'événement au bouton suivant
  document.getElementById('suivant').addEventListener('click', goToNextQuestion);
  document.getElementById('precedent').addEventListener('click', goToPreviousQuestion);
  document.getElementById('valider').addEventListener('click', validateAnswer);
}

/**
 * Affiche une erreur
 */
function showError(message) {
  const feedbackContainer = document.getElementById('feedbackContainer');
  if (!feedbackContainer) return;
  
  feedbackContainer.innerHTML = `
    <div class="alert alert-danger">
      <h5><i class="fas fa-exclamation-circle"></i> Erreur</h5>
      <p>${message}</p>
    </div>
  `;
  
  feedbackContainer.style.display = 'block';
  document.getElementById('loadingContainer').style.display = 'none';
}

/**
 * Récupère un cookie par son nom
 */
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}