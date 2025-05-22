import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from exercises.models import ExerciseAttempt, Question, Answer, QuestionResponse
from django.utils import timezone

class ExerciseConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.attempt_id = self.scope['url_route']['kwargs']['attempt_id']
        self.room_group_name = f'exercise_{self.attempt_id}'
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')
        
        if message_type == 'submit_answer':
            question_id = data.get('question_id')
            answer_id = data.get('answer_id')
            text_response = data.get('text_response')
            
            # Process the answer
            result = await self.save_response(
                self.attempt_id,
                question_id,
                answer_id,
                text_response
            )
            
            # Send response back to the client
            await self.send(text_data=json.dumps(result))
        
        elif message_type == 'get_question':
            question_index = data.get('question_index', 0)
            
            # Get the question data
            question_data = await self.get_question_data(
                self.attempt_id,
                question_index
            )
            
            # Send question data back to the client
            await self.send(text_data=json.dumps(question_data))
        
        elif message_type == 'complete_exercise':
            # Mark the exercise as completed
            result = await self.complete_exercise(self.attempt_id)
            
            # Send completion confirmation back to the client
            await self.send(text_data=json.dumps(result))
    
    @database_sync_to_async
    def save_response(self, attempt_id, question_id, answer_id, text_response):
        try:
            attempt = ExerciseAttempt.objects.get(id=attempt_id)
            question = Question.objects.get(id=question_id)
            
            # Determine if answer is correct
            is_correct = False
            answer = None
            
            if answer_id:
                answer = Answer.objects.get(id=answer_id)
                is_correct = answer.is_correct
            elif text_response and question.question_type == 'fill_blank':
                # For text responses, check against correct answers
                correct_answers = question.answers.filter(is_correct=True)
                for correct_answer in correct_answers:
                    if text_response.lower().strip() == correct_answer.answer_text.lower().strip():
                        is_correct = True
                        answer = correct_answer
                        break
            
            # Create or update response
            response, created = QuestionResponse.objects.update_or_create(
                attempt=attempt,
                question=question,
                defaults={
                    'answer': answer,
                    'text_response': text_response,
                    'is_correct': is_correct
                }
            )
            
            # Update score if correct
            if is_correct:
                attempt.score += 10  # 10 points per correct answer
                attempt.save()
            
            # Prepare feedback
            feedback = None
            if answer and answer.feedback:
                feedback = answer.feedback
            
            return {
                'type': 'answer_result',
                'is_correct': is_correct,
                'feedback': feedback,
                'score': attempt.score
            }
        
        except Exception as e:
            return {
                'type': 'error',
                'message': str(e)
            }
    
    @database_sync_to_async
    def get_question_data(self, attempt_id, question_index):
        try:
            attempt = ExerciseAttempt.objects.get(id=attempt_id)
            exercise = attempt.exercise
            
            # Get questions in order
            questions = list(exercise.questions.all().order_by('order'))
            
            # Check if question index is valid
            if question_index >= len(questions):
                return {
                    'type': 'error',
                    'message': 'Question not found'
                }
            
            question = questions[question_index]
            
            # Get answers for the question
            answers = list(question.answers.all())
            
            # Check if this question has already been answered
            existing_response = QuestionResponse.objects.filter(
                attempt=attempt,
                question=question
            ).first()
            
            # Prepare question data
            question_data = {
                'type': 'question_data',
                'id': question.id,
                'text': question.question_text,
                'question_type': question.question_type,
                'image': question.image.url if question.image else None,
                'audio': question.audio.url if question.audio else None,
                'answers': [
                    {
                        'id': answer.id,
                        'text': answer.answer_text,
                        'image': answer.image.url if answer.image else None
                    } for answer in answers
                ],
                'total_questions': len(questions),
                'current_index': question_index,
                'already_answered': existing_response is not None,
                'previous_answer': existing_response.answer.id if existing_response and existing_response.answer else None,
                'previous_text': existing_response.text_response if existing_response else None,
                'was_correct': existing_response.is_correct if existing_response else None
            }
            
            return question_data
        
        except Exception as e:
            return {
                'type': 'error',
                'message': str(e)
            }
    
    @database_sync_to_async
    def complete_exercise(self, attempt_id):
        try:
            attempt = ExerciseAttempt.objects.get(id=attempt_id)
            
            # Mark attempt as completed
            attempt.completed = True
            attempt.completed_at = timezone.now()
            
            # Calculate time spent
            time_spent = (attempt.completed_at - attempt.started_at).total_seconds()
            attempt.time_spent = int(time_spent)
            
            attempt.save()
            
            return {
                'type': 'exercise_completed',
                'success': True,
                'score': attempt.score,
                'max_score': attempt.max_score,
                'time_spent': attempt.time_spent,
                'result_url': f'/exercises/result/{attempt.id}/'
            }
        
        except Exception as e:
            return {
                'type': 'error',
                'message': str(e)
            }
