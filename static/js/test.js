

//     // Configuration de jQuery pour inclure le CSRF token dans toutes les requêtes AJAX
// $.ajaxSetup({
//     beforeSend: function(xhr, settings) {
//         if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
//             xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
//         }
//     }
// });

// // Fonction pour récupérer le CSRF token
// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }
//     $(document).ready(function() {
//         // Variables
//         const attemptId = {{ attempt.id }};
//         let currentQuestionIndex = 0;
//         let totalQuestions = 0;
//         let questions = [];
//         let selectedAnswer = null;
//         let score = 0;
        
//         // Start exercise button
//         $('#start-exercise').click(function() {
//             $(this).prop('disabled', true);
//             $('#exercise-container').show();
//             loadQuestion(0);
//         });
        
//         // Load question
//         function loadQuestion(index) {
//             // Show loading state
//             $('#question-text').html('<div class="text-center"><i class="fas fa-spinner fa-spin fa-2x"></i><p>Chargement de la question...</p></div>');
//             $('#answers-container').empty();
            
//             // Fetch question data
//             $.ajax({
//                 url: `/exercises/attempt/${attemptId}/question/${index}/`,
//                 method: 'GET',
//                 success: function(data) {
//                     if (data.type === 'error') {
//                         showFeedback(data.message, 'danger');
//                         return;
//                     }
                    
//                     // Store questions data
//                     questions = data;
//                     totalQuestions = data.total_questions;
//                     currentQuestionIndex = data.current_index;
                    
//                     // Update progress indicator
//                     updateProgressIndicator();
                    
//                     // Update question counter
//                     $('#question-counter').text(`${currentQuestionIndex + 1}/${totalQuestions}`);
                    
//                     // Display question
//                     $('#question-text').html(data.text);
                    
//                     // Handle question image
//                     if (data.image) {
//                         $('#question-image').attr('src', data.image);
//                         $('#question-image-container').show();
//                     } else {
//                         $('#question-image-container').hide();
//                     }
                    
//                     // Handle question audio
//                     if (data.audio) {
//                         $('#question-audio').attr('src', data.audio);
//                         $('#question-audio-container').show();
//                     } else {
//                         $('#question-audio-container').hide();
//                     }
                    
//                     // Reset selected answer
//                     selectedAnswer = null;
                    
//                     // Display answers based on question type
//                     switch (data.question_type) {
//                         case 'multiple_choice':
//                             renderMultipleChoice(data.answers);
//                             break;
//                         case 'true_false':
//                             renderTrueFalse();
//                             break;
//                         case 'matching':
//                             renderMatching(data.answers);
//                             break;
//                         case 'drag_drop':
//                             renderDragDrop(data.answers);
//                             break;
//                         case 'fill_blank':
//                             renderFillBlank(data.text);
//                             break;
//                         case 'audio':
//                             renderAudio(data.answers);
//                             break;
//                         case 'visual':
//                             renderVisual(data.answers);
//                             break;
//                         default:
//                             renderMultipleChoice(data.answers);
//                     }
                    
//                     // Handle navigation buttons
//                     $('#prev-question').prop('disabled', currentQuestionIndex === 0);
//                     $('#submit-answer').show();
//                     $('#next-question').hide();
                    
//                     // If question was already answered
//                     if (data.already_answered) {
//                         if (data.previous_answer) {
//                             selectedAnswer = data.previous_answer;
//                             $(`.answer-option[data-id="${selectedAnswer}"]`).addClass('selected');
//                         }
                        
//                         if (data.was_correct) {
//                             showFeedback('Bonne réponse !', 'success');
//                         } else {
//                             showFeedback('Réponse incorrecte.', 'danger');
//                         }
                        
//                         $('#submit-answer').hide();
//                         $('#next-question').show();
//                     }
//                 },
//                 error: function() {
//                     showFeedback('Erreur lors du chargement de la question. Veuillez réessayer.', 'danger');
//                 }
//             });
//         }
        
//         // Update progress indicator
//         function updateProgressIndicator() {
//             const container = $('#progress-indicator');
//             container.empty();
            
//             for (let i = 0; i < totalQuestions; i++) {
//                 const step = $('<div class="progress-step"></div>').text(i + 1);
                
//                 if (i < currentQuestionIndex) {
//                     step.addClass('completed');
//                 } else if (i === currentQuestionIndex) {
//                     step.addClass('active');
//                 }
                
//                 container.append(step);
//             }
//         }
        
//         // Render multiple choice answers
//         function renderMultipleChoice(answers) {
//             const container = $('#answers-container');
//             container.empty();
            
//             answers.forEach(answer => {
//                 const option = $(`
//                     <div class="answer-option" data-id="${answer.id}">
//                         <div class="d-flex align-items-center">
//                             <div class="me-3">
//                                 <i class="far fa-circle"></i>
//                             </div>
//                             <div>
//                                 ${answer.text}
//                                 ${answer.image ? `<img src="${answer.image}" alt="Option image" class="img-fluid mt-2 rounded">` : ''}
//                             </div>
//                         </div>
//                     </div>
//                 `);
                
//                 option.click(function() {
//                     $('.answer-option').removeClass('selected');
//                     $(this).addClass('selected');
//                     $('.answer-option .fa-circle').removeClass('fa-check-circle').addClass('fa-circle');
//                     $(this).find('.fa-circle').removeClass('fa-circle').addClass('fa-check-circle');
//                     selectedAnswer = answer.id;
//                 });
                
//                 container.append(option);
//             });
//         }
        
//         // Render true/false answers
//         function renderTrueFalse() {
//             const container = $('#answers-container');
//             container.empty();
            
//             const trueOption = $(`
//                 <div class="answer-option" data-value="true">
//                     <div class="d-flex align-items-center">
//                         <div class="me-3">
//                             <i class="far fa-circle"></i>
//                         </div>
//                         <div>
//                             Vrai
//                         </div>
//                     </div>
//                 </div>
//             `);
            
//             const falseOption = $(`
//                 <div class="answer-option" data-value="false">
//                     <div class="d-flex align-items-center">
//                         <div class="me-3">
//                             <i class="far fa-circle"></i>
//                         </div>
//                         <div>
//                             Faux
//                         </div>
//                     </div>
//                 </div>
//             `);
            
//             trueOption.click(function() {
//                 $('.answer-option').removeClass('selected');
//                 $(this).addClass('selected');
//                 $('.answer-option .fa-circle').removeClass('fa-check-circle').addClass('fa-circle');
//                 $(this).find('.fa-circle').removeClass('fa-circle').addClass('fa-check-circle');
//                 selectedAnswer = 'true';
//             });
            
//             falseOption.click(function() {
//                 $('.answer-option').removeClass('selected');
//                 $(this).addClass('selected');
//                 $('.answer-option .fa-circle').removeClass('fa-check-circle').addClass('fa-circle');
//                 $(this).find('.fa-circle').removeClass('fa-circle').addClass('fa-check-circle');
//                 selectedAnswer = 'false';
//             });
            
//             container.append(trueOption);
//             container.append(falseOption);
//         }
        
//         // Render matching answers
//         function renderMatching(answers) {
//             $('#drag-drop-container').show();
//             const dragItems = $('#drag-items');
//             const dropZones = $('#drop-zones');
            
//             dragItems.empty();
//             dropZones.empty();
            
//             // Create shuffled array of answers
//             const shuffledAnswers = [...answers].sort(() => Math.random() - 0.5);
            
//             // Create drag items
//             shuffledAnswers.forEach(answer => {
//                 const item = $(`
//                     <div class="drag-item" draggable="true" data-id="${answer.id}">
//                         ${answer.text}
//                     </div>
//                 `);
                
//                 // Add drag events
//                 item.on('dragstart', function(e) {
//                     e.originalEvent.dataTransfer.setData('text/plain', answer.id);
//                     $(this).addClass('dragging');
//                 });
                
//                 item.on('dragend', function() {
//                     $(this).removeClass('dragging');
//                 });
                
//                 dragItems.append(item);
//             });
            
//             // Create drop zones
//             answers.forEach((answer, index) => {
//                 const zone = $(`
//                     <div class="drop-zone" data-index="${index}">
//                         <div class="drop-zone-label">${index + 1}</div>
//                     </div>
//                 `);
                
//                 // Add drop events
//                 zone.on('dragover', function(e) {
//                     e.preventDefault();
//                     $(this).addClass('active');
//                 });
                
//                 zone.on('dragleave', function() {
//                     $(this).removeClass('active');
//                 });
                
//                 zone.on('drop', function(e) {
//                     e.preventDefault();
//                     $(this).removeClass('active');
                    
//                     const itemId = e.originalEvent.dataTransfer.getData('text/plain');
//                     const item = $(`.drag-item[data-id="${itemId}"]`);
                    
//                     // Move item to drop zone
//                     $(this).append(item);
                    
//                     // Update selected answers
//                     if (!selectedAnswer) {
//                         selectedAnswer = {};
//                     }
                    
//                     selectedAnswer[index] = itemId;
//                 });
                
//                 dropZones.append(zone);
//             });
//         }
        
//         // Render drag and drop
//         function renderDragDrop(answers) {
//             $('#drag-drop-container').show();
//             // Similar to matching but with different UI
//         }
        
//         // Render fill in the blank
//         function renderFillBlank(text) {
//             $('#fill-blank-container').show();
//             const container = $('#fill-blank-text');
//             container.empty();
            
//             // Replace [blank] with input fields
//             const html = text.replace(/\[blank\]/g, '<input type="text" class="fill-blank-input">');
//             container.html(html);
            
//             // Focus on first input
//             container.find('input').first().focus();
            
//             // Handle enter key to move to next input or submit
//             container.find('input').keypress(function(e) {
//                 if (e.which === 13) {
//                     const inputs = container.find('input');
//                     const index = inputs.index(this);
                    
//                     if (index < inputs.length - 1) {
//                         inputs.eq(index + 1).focus();
//                     } else {
//                         $('#submit-answer').click();
//                     }
                    
//                     e.preventDefault();
//                 }
//             });
//         }
        
//         // Render audio question
//         function renderAudio(answers) {
//             // Similar to multiple choice but with audio controls
//         }
        
//         // Render visual question
//         function renderVisual(answers) {
//             // Similar to multiple choice but with visual elements
//         }
        
//         // Play audio
//         $('#play-audio').click(function() {
//             const audio = document.getElementById('question-audio');
//             audio.play();
//         });
        
//         // Submit answer
//         // Submit answer
//         // Submit answer
//         $('#submit-answer').click(function() {
//             // Validate answer
//             if (!validateAnswer()) {
//                 showFeedback('Veuillez sélectionner une réponse.', 'warning');
//                 return;
//             }
            
//             // Disable submit button
//             $(this).prop('disabled', true);
            
//             // Prepare data - CORRECTION ICI
//             const data = {
//                 question_id: questions.id,
//                 answer_id: null,
//                 text_response: null
//             };
            
//             // Get answer based on question type - CORRECTION ICI
//             if (questions.question_type === 'fill_blank') {
//                 // Pour les questions à texte libre
//                 data.text_response = $('#fill-blank-text input').val() || $('#math-result').val() || "";
//                 data.answer_id = null;
//             } else {
//                 // Pour les questions à choix multiple, true/false, etc.
//                 data.answer_id = selectedAnswer;
//                 data.text_response = "";  // Chaîne vide au lieu de null
//             }
            
//             console.log('Données à envoyer:', data); // Debug
            
//             // Add CSRF token
//             const csrftoken = getCookie('csrftoken');
            
//             // Submit answer
//             $.ajax({
//                 url: `/exercises/attempt/${attemptId}/submit/`,
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                     'X-CSRFToken': csrftoken
//                 },
//                 data: JSON.stringify(data),
//                 success: function(response) {
//                     console.log('Réponse reçue:', response); // Debug
                    
//                     // Update score
//                     score = response.score;
                    
//                     // Show feedback
//                     if (response.is_correct) {
//                         showFeedback(response.feedback || 'Bonne réponse !', 'success');
                        
//                         // Mark selected answer as correct
//                         $(`.answer-option[data-id="${selectedAnswer}"]`).addClass('correct');
//                     } else {
//                         showFeedback(response.feedback || 'Réponse incorrecte.', 'danger');
                        
//                         // Mark selected answer as incorrect
//                         $(`.answer-option[data-id="${selectedAnswer}"]`).addClass('incorrect');
//                     }
                    
//                     // Show next button
//                     $('#submit-answer').hide();
//                     $('#next-question').show();
                    
//                     // If exercise is completed
//                     if (response.completed) {
//                         $('#next-question').text('Terminer').addClass('btn-success');
//                     }
//                 },
//                 error: function(xhr, status, error) {
//                     console.error('Erreur AJAX:', error);
//                     console.error('Réponse du serveur:', xhr.responseText);
//                     showFeedback('Erreur lors de la soumission de la réponse. Veuillez réessayer.', 'danger');
//                     $('#submit-answer').prop('disabled', false);
//                 }
//             });
//         });

//         // Complete exercise
//         function completeExercise() {
//             // Show completion screen
//             $('#exercise-container').hide();
//             $('#exercise-complete').show();
            
//             // Update score
//             $('#final-score').text(score);
//             $('#max-score').text(questions.total_questions * 10);
            
//             const percentage = (score / (questions.total_questions * 10)) * 100;
//             $('#score-progress').css('width', `${percentage}%`).attr('aria-valuenow', percentage);
            
//             // Set result URL
//             $('#view-results').attr('href', `/exercises/result/${attemptId}/`);
            
//             // Submit completion to server
//             const csrftoken = getCookie('csrftoken');
            
//             $.ajax({
//                 url: `/exercises/attempt/${attemptId}/submit/`,
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                     'X-CSRFToken': csrftoken
//                 },
//                 data: JSON.stringify({
//                     type: 'complete_exercise'
//                 }),
//                 success: function(response) {
//                     console.log('Exercise completed successfully');
//                     if (response.redirect_url) {
//                         window.location.href = response.redirect_url;
//                     }
//                 },
//                 error: function(xhr, status, error) {
//                     console.error('Error completing exercise:', error);
//                 }
//             });
//         }
        
//         // Validate answer
//         // Validate answer
//         function validateAnswer() {
//             console.log('Validation - Type de question:', questions.question_type);
//             console.log('Validation - Réponse sélectionnée:', selectedAnswer);
            
//             switch (questions.question_type) {
//                 case 'multiple_choice':
//                 case 'true_false':
//                     return selectedAnswer !== null && selectedAnswer !== undefined;
//                 case 'fill_blank':
//                     const inputs = $('#fill-blank-text input');
//                     let valid = true;
                    
//                     inputs.each(function() {
//                         if (!$(this).val().trim()) {
//                             valid = false;
//                             return false;
//                         }
//                     });
                    
//                     return valid;
//                 case 'matching':
//                 case 'drag_drop':
//                     // Validate matching and drag-drop answers
//                     return selectedAnswer !== null;
//                 default:
//                     return selectedAnswer !== null;
//             }
//         }
        
//         // Show feedback message
//         function showFeedback(message, type) {
//             const feedback = $('#feedback-message');
//             feedback.removeClass('alert-success alert-danger alert-warning').addClass(`alert-${type}`);
//             feedback.html(message);
//             feedback.show();
//         }
        
//         // Previous question button
//         $('#prev-question').click(function() {
//             if (currentQuestionIndex > 0) {
//                 loadQuestion(currentQuestionIndex - 1);
//             }
//         });
        
//         // Next question button
//         $('#next-question').click(function() {
//             if (currentQuestionIndex < totalQuestions - 1) {
//                 loadQuestion(currentQuestionIndex + 1);
//             } else {
//                 // Complete exercise
//                 completeExercise();
//             }
//         });
        
//         // Complete exercise
//         function completeExercise() {
//             // Show completion screen
//             $('#exercise-container').hide();
//             $('#exercise-complete').show();
            
//             // Update score
//             $('#final-score').text(score);
//             $('#max-score').text(questions.total_questions * 10);
            
//             const percentage = (score / (questions.total_questions * 10)) * 100;
//             $('#score-progress').css('width', `${percentage}%`).attr('aria-valuenow', percentage);
            
//             // Set result URL
//             $('#view-results').attr('href', `/exercises/result/${attemptId}/`);
            
//             // Submit completion to server
//             $.ajax({
//                 url: `/exercises/attempt/${attemptId}/submit/`,
//                 method: 'POST',
//                 contentType: 'application/json',
//                 data: JSON.stringify({
//                     type: 'complete_exercise'
//                 }),
//                 success: function(response) {
//                     console.log('Exercise completed successfully');
//                 },
//                 error: function() {
//                     console.error('Error completing exercise');
//                 }
//             });
//         }
//     });



