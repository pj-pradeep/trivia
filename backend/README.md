# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
The Project uses PostgreSQL as the backend database to drive the application. Please follow the installation instructions for your operating system as per instructions here [Install Postgres](https://www.postgresql.org/download/)

With Postgres running, restore a database using the trivia.psql file provided. The application is implemented to use **postgres** as the database username and the database name **trivia** for the connection properties.

From the backend folder in terminal run:
```bash
createdb trivia
psql -U postgres -d trivia -a -f trivia.psql
```
The above commands will create the initial seed data required for the trivia application to work.


## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## REST API Reference

### General

* **Base URL** - The application is currently implemented to run locally under the standard port 5000. The API base url http://localhost:5000/api/v1
* **Headers** - For all your requests, set the HTTP request header ```Content-Type: application/json```
* **Authentication** - There is no authentication implemented in current implementation. It might be added as a future enhancement. 

### Errors

The Trivia applicatoin uses convential HTTP response codes to indicate the success or failure of an API request. In general: Codes in 2xx range indicate success. Codes in the 4xx range indicate an error that failed given the information provided. Below json response will be returned for any failed API request:

```
{
    "success": False,
    "error": 404,
    "message": "Resource Not Found"
}
```

List of errors to expect:


Error Code | Error Message
---------- | -------------
404 | Resource Not Found
400 | Bad Request
422 | Unprocessable Error
405 | method not allowed



### API Endpoints


### Retrieve All Question Categories
Retrieves all the categories of questions. 
#### Parameters
No Parameters
#### Returns
List of all categories with **id** and **type**

```
GET /api/v1/categories
```
#### Sample Request/Response
```
curl http://localhost:5000/api/v1/categories

{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true, 
  "total_categories": 6
}
```



### Retrieve All Questions
Retrieve all the existing Trivia Questions across all categories as a paginated list. The api returns 10 questions per page.
#### Parameters
Current Page number. If page number is not speicified, it is defaulted to 1.
#### Returns
Paginated list of all questions

```
GET /api/v1/questions?page=1
```

#### Sample Request/Response
```
curl http://localhost:5000/api/v1/questions\?page\=2

{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }, 
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }, 
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "Scarab", 
      "category": 4, 
      "difficulty": 4, 
      "id": 23, 
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }, 
    {
      "answer": "Sam Houston", 
      "category": 4, 
      "difficulty": 4, 
      "id": 24, 
      "question": "Who served as the first and third president of the Republic of Texas?"
    }
  ], 
  "success": true, 
  "total_questions": 22
}
```



### Delete a question
Delete question identified by **id**
#### Parameters
**id** - The uniqued identifier of the question to be deleted

#### Returns
Success response confirming the **id** of the question deleted

```
DELETE /api/v1/questions/<int:question_id>
```

#### Sample Request/Response 
```
curl -X DELETE http://localhost:5000/api/v1/questions/10 -H "Content-Type: application/json"

{
  "question_deleted": 10, 
  "success": true
}
```




### Create new question
Create or add a new question to the Trivia question database. 
#### Parameters
* question - the new question text 
* answer - the answer for the question
* difficulty - difficulty level of the question. If not specified, defaulted to difficulty level 1.
* category - the category the question belongs to. If not specified, defaulted to *Science* category.

#### Returns
The identifier of the new question created

```
POSST /api/v1/questions
```

#### Sample Request/Response 
```
curl -X POST http://localhost:5000/api/v1/questions -H "Content-Type: application/json" -d '{ "question": "Which basketball team did Michael Jordan play for in college?", "answer": "University of North Carolina at Chapel Hill", "difficulty": 2, "category": 6}'

{
  "created": 28, 
  "success": true
}
```




### Search Questions
Retrieve all the questions matching a search term. The api will return any question where the search term is a substring of the question.
#### Parameters
* searchTerm - The search term to look for in question

#### Returns
List of questions matching the search term


```
POST /api/v1/questions/search
```

#### Sample Request/Response 
```
curl -X POST http://localhost:5000/api/v1/questions/search -H "Content-Type: application/json" -d '{"searchTerm": "soccer"}'

{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}
```




### Retrieve Questions for a category
Retrieve all questions belonging to a specific category
#### Parameters
* category_id - the identifier of the category
#### Returns
List of all questions in the specified category

```
GET /api/v1/categories/<int:category_id>/questions
```

#### Sample Request/Response 
```
curl http://localhost:5000/api/v1/categories/3/questions

{
  "current_category": {
    "3": "Geography"
  }, 
  "questions": [
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 22
}
```




### Play Trivia Quizz
The api returns a random question not previously shown. The api returns question from a specified category or across all categories.
#### Parameters
* previous_questions - list of previous questions shown
* quiz_category - one of the available categories.
#### Returns
Returns a random question which is not yet played.

```
POST /api/v1/quizzes
```

#### Sample Request/Response 
```
curl -X POST http://localhost:5000/api/v1/quizzes -H "Content-Type: application/json" -d '{"previous_questions":[],"quiz_category":{"type": "Geography","id":3}}'

{
  "question": {
    "answer": "Lake Victoria", 
    "category": 3, 
    "difficulty": 2, 
    "id": 13, 
    "question": "What is the largest lake in Africa?"
  }, 
  "success": true
}
```



## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql -U postgres -d trivia_test -a -f trivia.psql
python test_flaskr.py
```