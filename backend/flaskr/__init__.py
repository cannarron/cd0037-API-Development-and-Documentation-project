import os
import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import not_, and_
from flask_cors import CORS
from helpers import paginate
import random

from models import setup_db, Question, Category


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
   
    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
  
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request_func(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', '*')
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def getAllCategories(): 
        categories = Category.query.all()
        formatted_categories = [category.format() for category in  categories]
        return jsonify(formatted_categories, 200)
    
        

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def getQuestions():
        page = request.args.get('page', 1, type=int)
        questions =  Question.query.all()
        categories = Category.query.all()
        formatted_questions = [question.format() for question in questions]
        return jsonify({
           'questions': paginate(formatted_questions, page),
            'total_questions': len(formatted_questions),
            'categories': [category.format() for category in categories]
        })
        
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<question_id>', methods=['DELETE'])
    def deleteQuestion(question_id):
         question =  Question.query.filter_by(id=question_id).one_or_none()
         if question:
            try:
                Question.delete(question)
            except:
                return jsonify({
                    'message': 'There was a problem, question could not be deleted'

                }), 500
            return jsonify({
                'message': 'Successfully deleted'
            }), 204
         else:
            return jsonify({
                "message" : 'Question does not exist'
            }), 404
         
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions/new', methods=['POST'])
    def newQuestion():
        data = request.get_json()
        question = data['question']
        answer = data['answer']
        category = data['category']
        difficulty = data['difficulty']
        try:
            new_question =  Question(question, answer, category, difficulty)
        except:
            return jsonify({
                'message': 'Internal server error'

            }), 500
        return jsonify({
            'message': 'Successfully added question'
            }), 201
            

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/questions/search', methods=['POST'])
    def retrieveQuestion():
        data = request.get_json()
        search_term = data['search_term']
        try:
            questions = Question.query.filter(Question.question.ilike(f'%{search_term}%'))
            formatted_questions = [question.format() for question in questions]
            if len(formatted_questions) > 0:
                return jsonify({
                "questions": formatted_questions
            })
            else:
                return jsonify({
                    "message": "Resource not found"
                })
        except:
            return jsonify({
                'message': "Internal server error"
            }), 500
        
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/questions/category/<int:category_id>', methods=['GET'])
    def getQuestionsbyCategory(category_id):
        questions =  Question.query.filter_by(category=category_id).all()
        formatted_questions = [question.format() for question in questions]
        return jsonify({
            "questions": paginate(formatted_questions, 1)
        }), 200

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/questions/play/random', methods=['GET'])
    def playByRandom():
        try:
            questions =  Question.query.all()
            formatted_questions = [question.format() for question in questions]
        except:
            return jsonify({
                "message": "Internal server error"
            })
        return jsonify({
            "question": random.choice(formatted_questions)
        }), 200

    @app.route('/questions/play/category', methods=['GET'])
    def playByCategory():
        data = request.get_json()
        categoryID = data['category']
        prevQuestionID = data['prevQuestion']
        try:
            questions =  Question.query.filter_by(category=categoryID).all()
            formatted_questions = [question.format() for question in questions]
            return jsonify({
                "question": random.choice(formatted_questions)
                 }), 200
        except:
            return jsonify({
                "message": "Internal server error"
            }), 500
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found():
        return jsonify({
            'message': 'Resource not found'
        })
    @app.errorhandler(422)
    def Unprocessable():
        return jsonify({
            'message': 'Unprocessable entity'
        })
    @app.errorhandler(409)
    def badRequestError():
        return jsonify({'message': 'Bad request'})

    @app.errorhandler(500)
    def serverError():
        return jsonify({
            'message': "Internal server error"
        })
    return app

