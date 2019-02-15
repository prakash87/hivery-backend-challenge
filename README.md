# Paranuara Challenge Solution
The soulution is built with Python3 and MySQL using Django Framework. 
First of all, create a virtual environment and activate it. Example-
```
python3 -m venv env
source env/bin/activate
```
Then clone this repo and CD to the project directory.

## Installation
Set the environment variables for the database and secret key as below-
```
export DATABASE_NAME='dbname'
export DATABASE_USER='username'
export DATABASE_PASSWORD='password'
export SECRET_KEY='somesecretkey!'
```

Run following commands to install the dependencies and import the data
```
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py import_data
```

## Tests
Run following commands to run the Unit Tests
```
python manage.py test
```

## Run Server
Run following command to run the solution
```
python manage.py runserver
```

## API
API endpoints to list all people and list all companies have been added for convenience although was not required.

### List all people
```
GET: http://localhost:8000/api/people/
```

### List all companies
```
GET: http://localhost:8000/api/companies/
```

### View company detail and employees
```
GET: http://localhost:8000/api/companies/<company_id>/
Example: http://localhost:8000/api/companies/416/
```

### View person's detail
```
GET: http://localhost:8000/api/people/<person_id>/
Example: http://localhost:8000/api/people/1143/
```

### Compare people and view common in following / friends
```
GET: http://localhost:8000/api/people/<person1_id,person2_id>/?eye_color=<color_code>&&is_alive=<boolean>
Example: http://localhost:8000/api/people/1154,1155/?eye_color=BR&&is_alive=True
```
Any number of person ids can be placed. They must be separated by commas and NO white spaces is allowed.

Eye color codes-
```
Albino: AL
Blue: BL
Brown: BR
Green: GR
Grey: GY
Hazel: HZ
Other: OT
```
Also, any field from the Person object can be placed on query string such as `gender=M` and so on.

**Please contact me if you have any question**

# Paranuara Challenge
Paranuara is a class-m planet. Those types of planets can support human life, for that reason the president of the Checktoporov decides to send some people to colonise this new planet and
reduce the number of people in their own country. After 10 years, the new president wants to know how the new colony is growing, and wants some information about his citizens. Hence he hired you to build a rest API to provide the desired information.

The government from Paranuara will provide you two json files (located at resource folder) which will provide information about all the citizens in Paranuara (name, age, friends list, fruits and vegetables they like to eat...) and all founded companies on that planet.
Unfortunately, the systems are not that evolved yet, thus you need to clean and organise the data before use.
For example, instead of providing a list of fruits and vegetables their citizens like, they are providing a list of favourite food, and you will need to split that list (please, check below the options for fruits and vegetables).

## New Features
Your API must provides these end points:
- Given a company, the API needs to return all their employees. Provide the appropriate solution if the company does not have any employees.
- Given 2 people, provide their information (Name, Age, Address, phone) and the list of their friends in common which have brown eyes and are still alive.
- Given 1 people, provide a list of fruits and vegetables they like. This endpoint must respect this interface for the output: `{"username": "Ahi", "age": "30", "fruits": ["banana", "apple"], "vegetables": ["beetroot", "lettuce"]}`

## Delivery
To deliver your system, you need to send the link on GitHub. Your solution must provide tasks to install dependencies, build the system and run. Solutions that does not fit this criteria **will not be accepted** as a solution. Assume that we have already installed in our environment Java, Ruby, Node.js, Python, MySQL, MongoDB and Redis; any other technologies required must be installed in the install dependencies task. Moreover well tested and designed systems are one of the main criteria of this assessement 

## Evaluation criteria
- Solutions written in Python would be preferred.
- Installation instructions that work.
- During installation, we may use different companies.json or people.json files.
- The API must work.
- Tests

Feel free to reach to your point of contact for clarification if you have any questions.
