import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}@{}/{}" \
                                .format('postgres','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_all_categories_success(self):    
        response = self.client().get('/api/v1/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_categories'], len(data['categories']))

    
    def test_get_paginated_questions(self):
        response = self.client().get('/api/v1/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']) > 0)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))

    def test_404_get_paginated_questions_page_out_of_range(self):
        response = self.client().get('api/v1/questions?page=1000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_200_get_quetions_by_category(self):
        response = self.client().get('/api/v1/categories/3/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['questions']), 3)
        self.assertTrue(data['current_category'])

    def test_404_get_questions_by_category(self):
        response = self.client().get('/api/v1/categories/3000/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
    
    def test_200_search_questions(self):
        search_term = {'searchTerm': 'soccer'}
        response = self.client().post('/api/v1/questions/search', json=search_term)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 2)
        self.assertEqual(data['total_questions'], 2)

    def test_404_search_questions_search_term_not_found(self):
        search_term = {'searchTerm': 'tennis'}
        response = self.client().post('/api/v1/questions/search', json=search_term)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_400_search_questions_none_search_term(self):
        search_term = {'searchTerm': None}
        response = self.client().post('/api/v1/questions/search', json=search_term)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_200_create_question(self):
        new_question_request = {'question': 'Who is the President of United States?',
            'answer': 'Donald Trump',
            'difficulty': 1,
            'category': 4
        }
        response = self.client().post('/api/v1/questions', json=new_question_request)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['created'] > 19)

    def test_400_create_question_when_no_request_body(self):
        new_question_request = {}
        response = self.client().post('/api/v1/questions', json=new_question_request)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_422_create_question_when_required_fields_missing_from_request(self):
        new_question_request = {'answer': 'Donald Trump',
            'difficulty': 1,
            'category': 4
        }
        response = self.client().post('/api/v1/questions', json=new_question_request)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)

    
    def test_200_delete_question(self):
        response = self.client().delete('/api/v1/questions/5')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question_deleted'])
    

    def test_404_delete_question_wrong_question_id(self):
        response = self.client().delete('/api/v1/questions/5000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_200_play_quizzes_all_category(self):
        request_body = {
            "previous_questions": [],
            "quiz_category": {
                "type": "click",
                "id": 0 
            }
        }

        response = self.client().post('/api/v1/quizzes', json=request_body)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_200_play_quizzes_with_previous_question(self):
        request_body = {
            "previous_questions": [22],
            "quiz_category": {
                "type": "Science",
                "id": "1" 
            }
        }

        response = self.client().post('/api/v1/quizzes', json=request_body)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question']['id'] not in request_body['previous_questions'])

    def test_400_play_quizzes_when_no_previous_questions_in_request(self):
        request_body = {
            "quiz_category": {
                "type": "Science",
                "id": "1" 
            }
        }

        response = self.client().post('/api/v1/quizzes', json=request_body)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)


    def test_400_play_quizzes_when_no_quiz_category_in_request(self):
        request_body = {
            "previous_questions": [22]
        }

        response = self.client().post('/api/v1/quizzes', json=request_body)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()