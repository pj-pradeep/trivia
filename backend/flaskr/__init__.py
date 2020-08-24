import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    response.headers.add('Content-Type', 'application/json')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/api/v1/categories', methods=['GET'])
  def get_categories():
    print('Retrieving all categories')
    categories = Category.query.order_by(Category.type.asc()).all()

    if len(categories) == 0:
      abort(404)
    

    return jsonify({
      'success': True,
      'total_categories': len(categories),
      'categories': {category.id: category.type for category in categories}
    })
    

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/api/v1/questions', methods=['GET'])
  def get_paginated_questions():
    print('Retrieving paginated questions')
    questions = Question.query.order_by(Question.id).all()

    if questions is None:
      abort(404)

    current_questions = paginate_questions(request, questions)

    if len(current_questions) == 0:
      abort(404)

    categories = Category.query.all()

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(questions),
      'categories': {category.id: category.type for category in categories},
      'current_category': None
    })  


  def paginate_questions(request, questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    current_questions = [question.format() for question in questions]
    return current_questions[start:end]

    
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/api/v1/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
  
    question = Question.query.get(question_id)

    if question is None:
      print(f'There is no question with id {question_id}. Nothing to delete')
      abort(404)

    try:
      question.delete()

      return jsonify({
        "success": True,
        "question_deleted": question.id
      })
    except Exception as e:
      print(f'There was an exception trying to delete question {question_id}')
      print(e)
      abort(422)      
      
      

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/api/v1/questions', methods=['POST'])
  def create_questions():
    request_body = request.get_json()

    if not request_body:
      print("There was not request body. Not a valid request")
      abort(400)
    
    new_question = request_body.get('question', None)
    new_answer = request_body.get('answer', None)
    new_difficulty = request_body.get('difficulty', 1)
    new_category = request_body.get('category', 1)

    # we are defaulting difficulty and category to 1 if not available
    if (new_question is None or new_answer is None):
      abort(422)

    try:
      question_to_add = Question(
        question = new_question,
        answer = new_answer,
        category = new_category,
        difficulty = new_difficulty
      )

      question_to_add.insert()

      return jsonify({
        "success": True,
        "created": question_to_add.id
      })
    except Exception as e:
      print('There was an exception while adding new question')
      print(e)
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/api/v1/questions/search', methods=['POST'])
  def search_questions():
    request_body = request.get_json()

    if not request_body:
      print("There was not request body. Not a valid request")
      abort(400)

    search_str = request_body.get('searchTerm', None)
    
    if search_str is None:
      print("There was not search string mentioned. Nothing to search")
      abort(400)

    questions = Question.query.filter(Question.question.ilike(f'%{search_str}%')).all()

    total_questions = len(questions)

    categories = Category.query.all()

    if total_questions == 0:
      abort(404)

    return jsonify({
      "success": True,
      "questions": [question.format() for question in questions],
      "total_questions": total_questions,
      'categories': {category.id: category.type for category in categories},
      "current_category": None
    })


  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/api/v1/categories/<int:category_id>/questions', methods=['GET'])
  def get_questions_by_category(category_id):
    questions_by_category = Question.query.filter(Question.category == category_id).all()

    if (len(questions_by_category) == 0):
      abort(404)

    current_category = Category.query.filter(Category.id == category_id).first()

    return jsonify({
      'success': True,
      'questions': [question.format() for question in questions_by_category],
      'total_questions': len(Question.query.all()),
      'current_category': {current_category.id: current_category.type}
    })

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/api/v1/quizzes', methods=['POST'])
  def play_trivia_quiz():
    request_body = request.get_json()

    if request_body is None:
      abort(400)

    previous_questions = request_body.get('previous_questions', None)
    quiz_category = request_body.get('quiz_category', None)

    if previous_questions is None or quiz_category is None:
      abort(400)

    if quiz_category['id'] == 0:
      questions = Question.query.filter(Question.id.notin_((previous_questions))).all()
    else:
      questions = Question.query.filter(Question.category == quiz_category['id']).filter(Question.id.notin_((previous_questions))).all()

    random_question = questions[random.randrange(0, len(questions), 1)]

    return jsonify({
      "success": True,
      "question": random_question.format()
    })

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found_error(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "Resource Not Found"
    }), 404

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "Bad Request"
    }), 400

  @app.errorhandler(422)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "Unprocessable Error"
    }), 422
  
  return app

    