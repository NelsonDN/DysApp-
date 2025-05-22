// /**
//  * Fonctions spécifiques pour les exercices de dyscalculie
//  */

// /**
//  * Crée un exercice de reconnaissance de nombres
//  * @param {Object} container - Élément DOM contenant l'exercice
//  * @param {Array} numbers - Tableau de nombres à reconnaître
//  * @param {Function} onComplete - Fonction à exécuter lorsque l'exercice est terminé
//  */
// function createNumberRecognitionExercise(container, numbers, onComplete) {
//   // Vider le conteneur
//   container.innerHTML = ""

//   // Créer l'élément pour afficher le nombre
//   var numberDisplay = document.createElement("div")
//   numberDisplay.className = "number-display"
//   container.appendChild(numberDisplay)

//   // Créer le conteneur pour les options
//   var optionsContainer = document.createElement("div")
//   optionsContainer.className = "options-container"
//   container.appendChild(optionsContainer)

//   // Variables pour suivre l'état de l'exercice
//   var currentIndex = 0
//   var score = 0

//   // Fonction pour afficher un nombre
//   function displayNumber() {
//     if (currentIndex >= numbers.length) {
//       // L'exercice est terminé
//       onComplete(score, numbers.length)
//       return
//     }

//     var currentNumber = numbers[currentIndex]
//     numberDisplay.textContent = currentNumber

//     // Créer les options (le nombre correct et des nombres proches)
//     var options = [currentNumber]

//     // Ajouter des nombres proches comme distracteurs
//     while (options.length < 4) {
//       var offset = Math.floor(Math.random() * 5) + 1
//       offset *= Math.random() < 0.5 ? 1 : -1

//       var distractorNumber = currentNumber + offset

//       // Éviter les doublons
//       if (!options.includes(distractorNumber)) {
//         options.push(distractorNumber)
//       }
//     }

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
//         var isCorrect = option === currentNumber

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
//             if (Number.parseInt(btn.textContent) === currentNumber) {
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

//         // Passer au nombre suivant après un délai
//         setTimeout(() => {
//           currentIndex++
//           displayNumber()
//         }, 1500)
//       })

//       optionsContainer.appendChild(button)
//     })
//   }

//   // Fonction pour mélanger un tableau
//   function shuffleArray(array) {
//     for (let i = array.length - 1; i > 0; i--) {
//       const j = Math.floor(Math.random() * (i + 1))
//       ;[array[i], array[j]] = [array[j], array[i]]
//     }
//     return array
//   }

//   // Commencer l'exercice
//   displayNumber()
// }

// /**
//  * Crée un exercice de calcul mental
//  * @param {Object} container - Élément DOM contenant l'exercice
//  * @param {Array} operations - Tableau d'opérations à effectuer
//  * @param {Function} onComplete - Fonction à exécuter lorsque l'exercice est terminé
//  */
// function createMentalCalculationExercise(container, operations, onComplete) {
//   // Vider le conteneur
//   container.innerHTML = ""

//   // Créer l'élément pour afficher l'opération
//   var operationDisplay = document.createElement("div")
//   operationDisplay.className = "operation-display"
//   container.appendChild(operationDisplay)

//   // Créer le champ de saisie pour la réponse
//   var answerInput = document.createElement("input")
//   answerInput.type = "number"
//   answerInput.className = "form-control form-control-lg mt-3"
//   answerInput.placeholder = "Votre réponse"
//   container.appendChild(answerInput)

//   // Créer le bouton de validation
//   var validateButton = document.createElement("button")
//   validateButton.className = "btn btn-primary btn-lg mt-3"
//   validateButton.textContent = "Valider"
//   container.appendChild(validateButton)

//   // Créer l'élément pour afficher le feedback
//   var feedbackDisplay = document.createElement("div")
//   feedbackDisplay.className = "feedback-display mt-3"
//   container.appendChild(feedbackDisplay)

//   // Variables pour suivre l'état de l'exercice
//   var currentIndex = 0
//   var score = 0

//   // Fonction pour afficher une opération
//   function displayOperation() {
//     if (currentIndex >= operations.length) {
//       // L'exercice est terminé
//       onComplete(score, operations.length)
//       return
//     }

//     var currentOperation = operations[currentIndex]
//     operationDisplay.textContent = currentOperation.text

//     // Vider le champ de saisie
//     answerInput.value = ""
//     answerInput.focus()

//     // Vider le feedback
//     feedbackDisplay.innerHTML = ""

//     // Activer le bouton de validation
//     validateButton.disabled = false
//   }

//   // Fonction pour vérifier la réponse
//   function checkAnswer() {
//     // Désactiver le bouton de validation
//     validateButton.disabled = true

//     var userAnswer = Number.parseInt(answerInput.value)
//     var currentOperation = operations[currentIndex]

//     // Vérifier si la réponse est correcte
//     var isCorrect = userAnswer === currentOperation.result

//     // Mettre à jour le score
//     if (isCorrect) {
//       score++
//       feedbackDisplay.innerHTML = '<div class="alert alert-success">Bonne réponse !</div>'
//     } else {
//       feedbackDisplay.innerHTML =
//         '<div class="alert alert-danger">Mauvaise réponse. La réponse correcte est ' +
//         currentOperation.result +
//         ".</div>"
//     }

//     // Passer à l'opération suivante après un délai
//     setTimeout(() => {
//       currentIndex++
//       displayOperation()
//     }, 2000)
//   }

//   // Ajouter un événement au bouton de validation
//   validateButton.addEventListener("click", checkAnswer)

//   // Ajouter un événement au champ de saisie pour valider avec Entrée
//   answerInput.addEventListener("keypress", (event) => {
//     if (event.key === "Enter") {
//       checkAnswer()
//     }
//   })

//   // Commencer l'exercice
//   displayOperation()
// }

// /**
//  * Crée un exercice de comparaison de nombres
//  * @param {Object} container - Élément DOM contenant l'exercice
//  * @param {Array} comparisons - Tableau de comparaisons à effectuer
//  * @param {Function} onComplete - Fonction à exécuter lorsque l'exercice est terminé
//  */
// function createNumberComparisonExercise(container, comparisons, onComplete) {
//   // Vider le conteneur
//   container.innerHTML = ""

//   // Créer le conteneur pour la comparaison
//   var comparisonContainer = document.createElement("div")
//   comparisonContainer.className = "comparison-container d-flex justify-content-center align-items-center"
//   container.appendChild(comparisonContainer)

//   // Créer l'élément pour le feedback
//   var feedbackDisplay = document.createElement("div")
//   feedbackDisplay.className = "feedback-display mt-3"
//   container.appendChild(feedbackDisplay)

//   // Variables pour suivre l'état de l'exercice
//   var currentIndex = 0
//   var score = 0

//   // Fonction pour afficher une comparaison
//   function displayComparison() {
//     if (currentIndex >= comparisons.length) {
//       // L'exercice est terminé
//       onComplete(score, comparisons.length)
//       return
//     }

//     var currentComparison = comparisons[currentIndex]

//     // Construire l'interface de comparaison
//     comparisonContainer.innerHTML = `
//             <div class="number-box">${currentComparison.left}</div>
//             <div class="comparison-operators">
//                 <button class="btn btn-outline-primary m-1" data-operator="<">&lt;</button>
//                 <button class="btn btn-outline-primary m-1" data-operator="=">=</button>
//                 <button class="btn btn-outline-primary m-1" data-operator=">">&gt;</button>
//             </div>
//             <div class="number-box">${currentComparison.right}</div>
//         `

//     // Vider le feedback
//     feedbackDisplay.innerHTML = ""

//     // Ajouter des événements aux boutons d'opérateurs
//     var operatorButtons = comparisonContainer.querySelectorAll("button")
//     operatorButtons.forEach((button) => {
//       button.addEventListener("click", function () {
//         var selectedOperator = this.getAttribute("data-operator")
//         checkComparison(selectedOperator)
//       })
//     })
//   }

//   // Fonction pour vérifier la comparaison
//   function checkComparison(selectedOperator) {
//     var currentComparison = comparisons[currentIndex]
//     var correctOperator

//     // Déterminer l'opérateur correct
//     if (currentComparison.left < currentComparison.right) {
//       correctOperator = "<"
//     } else if (currentComparison.left === currentComparison.right) {
//       correctOperator = "="
//     } else {
//       correctOperator = ">"
//     }

//     // Vérifier si la réponse est correcte
//     var isCorrect = selectedOperator === correctOperator

//     // Mettre à jour le score
//     if (isCorrect) {
//       score++
//       feedbackDisplay.innerHTML = '<div class="alert alert-success">Bonne réponse !</div>'
//     } else {
//       feedbackDisplay.innerHTML =
//         '<div class="alert alert-danger">Mauvaise réponse. La réponse correcte est ' + correctOperator + ".</div>"
//     }

//     // Mettre en évidence le bouton sélectionné
//     var operatorButtons = comparisonContainer.querySelectorAll("button")
//     operatorButtons.forEach((button) => {
//       button.disabled = true

//       var operator = button.getAttribute("data-operator")

//       if (operator === selectedOperator) {
//         button.classList.remove("btn-outline-primary")
//         button.classList.add(isCorrect ? "btn-success" : "btn-danger")
//       } else if (operator === correctOperator && !isCorrect) {
//         button.classList.remove("btn-outline-primary")
//         button.classList.add("btn-success")
//       }
//     })

//     // Passer à la comparaison suivante après un délai
//     setTimeout(() => {
//       currentIndex++
//       displayComparison()
//     }, 2000)
//   }

//   // Commencer l'exercice
//   displayComparison()
// }

/**
 * Fonctions spécifiques pour les exercices de dyscalculie
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
      
      // Initialiser les outils
      initializeAbacus();
      initializeNumberLine();
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
 * Initialise le boulier virtuel
 */
function initializeAbacus() {
  const abacusBeads = document.querySelectorAll('.abacus-bead');
  if (abacusBeads.length === 0) return;
  
  abacusBeads.forEach(bead => {
    bead.addEventListener('click', function() {
      // Basculer l'état du bead
      this.classList.toggle('active');
      
      // Mettre à jour le compteur
      updateAbacusCounter();
    });
  });
  
  // Bouton de réinitialisation
  const resetButton = document.querySelector('.abacus-reset');
  if (resetButton) {
    resetButton.addEventListener('click', function() {
      // Réinitialiser tous les beads
      abacusBeads.forEach(bead => {
        bead.classList.remove('active');
      });
      
      // Mettre à jour le compteur
      updateAbacusCounter();
    });
  }
}

/**
 * Met à jour le compteur du boulier
 */
function updateAbacusCounter() {
  const counter = document.querySelector('.abacus-counter');
  if (!counter) return;
  
  // Compter les beads actifs
  const activeBeads = document.querySelectorAll('.abacus-bead.active');
  counter.textContent = activeBeads.length;
}

/**
 * Initialise la droite numérique
 */
function initializeNumberLine() {
  const numberLine = document.querySelector('.number-line');
  if (!numberLine) return;
  
  const marker = document.querySelector('.number-line-marker');
  if (!marker) return;
  
  // Rendre le marqueur déplaçable
  marker.addEventListener('mousedown', function(e) {
    e.preventDefault();
    
    // Position initiale
    const startX = e.clientX;
    const startLeft = parseInt(window.getComputedStyle(marker).left);
    
    // Largeur de la ligne
    const lineWidth = numberLine.offsetWidth;
    
    // Fonction de déplacement
    function moveMarker(e) {
      // Calculer la nouvelle position
      let newLeft = startLeft + (e.clientX - startX);
      
      // Limiter à la ligne
      newLeft = Math.max(0, Math.min(lineWidth, newLeft));
      
      // Déplacer le marqueur
      marker.style.left = `${newLeft}px`;
      
      // Mettre à jour la valeur
      updateNumberLineValue(newLeft / lineWidth);
    }
    
    // Fonction de fin de déplacement
    function stopMoving() {
      document.removeEventListener('mousemove', moveMarker);
      document.removeEventListener('mouseup', stopMoving);
    }
    
    // Ajouter les écouteurs d'événements
    document.addEventListener('mousemove', moveMarker);
    document.addEventListener('mouseup', stopMoving);
  });
}

/**
 * Met à jour la valeur de la droite numérique
 */
function updateNumberLineValue(percentage) {
  const valueDisplay = document.querySelector('.number-line-value');
  if (!valueDisplay) return;
  
  // Calculer la valeur (par exemple, de 0 à 20)
  const value = Math.round(percentage * 20);
  valueDisplay.textContent = value;
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
  const textInputs = document.querySelectorAll('input[type="text"], input[type="number"]');
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
  
  const textInput = document.querySelector('input[type="text"], input[type="number"]');
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
  const textInputs = document.querySelectorAll('input[type="text"], input[type="number"]');
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
  
  // Ajouter les outils d'aide
  html += `
    <div class="tools-container mt-4 mb-4">
      <div class="row">
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">
              <h5 class="mb-0">Boulier virtuel</h5>
            </div>
            <div class="card-body">
              <div class="abacus">
                <div class="abacus-row">
                  <div class="abacus-bead" data-value="100"></div>
                  <div class="abacus-bead" data-value="100"></div>
                  <div class="abacus-bead" data-value="100"></div>
                  <div class="abacus-bead" data-value="100"></div>
                  <div class="abacus-bead" data-value="100"></div>
                </div>
                <div class="abacus-row">
                  <div class="abacus-bead" data-value="10"></div>
                  <div class="abacus-bead" data-value="10"></div>
                  <div class="abacus-bead" data-value="10"></div>
                  <div class="abacus-bead" data-value="10"></div>
                  <div class="abacus-bead" data-value="10"></div>
                  <div class="abacus-bead" data-value="10"></div>
                  <div class="abacus-bead" data-value="10"></div>
                  <div class="abacus-bead" data-value="10"></div>
                  <div class="abacus-bead" data-value="10"></div>
                </div>
                <div class="abacus-row">
                  <div class="abacus-bead" data-value="1"></div>
                  <div class="abacus-bead" data-value="1"></div>
                  <div class="abacus-bead" data-value="1"></div>
                  <div class="abacus-bead" data-value="1"></div>
                  <div class="abacus-bead" data-value="1"></div>
                  <div class="abacus-bead" data-value="1"></div>
                  <div class="abacus-bead" data-value="1"></div>
                  <div class="abacus-bead" data-value="1"></div>
                  <div class="abacus-bead" data-value="1"></div>
                </div>
              </div>
              <div class="text-center mt-2">
                <span class="abacus-counter">0</span>
                <button class="btn btn-sm btn-outline-secondary abacus-reset">
                  <i class="fas fa-redo"></i> Réinitialiser
                </button>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">
              <h5 class="mb-0">Droite numérique</h5>
            </div>
            <div class="card-body">
              <div class="number-line">
                <div class="number-line-markers">
                  <div class="number-line-marker" style="left: 0%;">0</div>
                  <div class="number-line-marker" style="left: 10%;">2</div>
                  <div class="number-line-marker" style="left: 20%;">4</div>
                  <div class="number-line-marker" style="left: 30%;">6</div>
                  <div class="number-line-marker" style="left: 40%;">8</div>
                  <div class="number-line-marker" style="left: 50%;">10</div>
                  <div class="number-line-marker" style="left: 60%;">12</div>
                  <div class="number-line-marker" style="left: 70%;">14</div>
                  <div class="number-line-marker" style="left: 80%;">16</div>
                  <div class="number-line-marker" style="left: 90%;">18</div>
                  <div class="number-line-marker" style="left: 100%;">20</div>
                </div>
                <div class="number-line-track"></div>
                <div class="number-line-handle" style="left: 0%;"></div>
              </div>
              <div class="text-center mt-2">
                <span class="number-line-value">0</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `;
  
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
        <input type="number" class="form-control" id="numberAnswer" placeholder="Votre réponse">
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
  
  // Initialiser les outils
  initializeAbacus();
  initializeNumberLine();
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