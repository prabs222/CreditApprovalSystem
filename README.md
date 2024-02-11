# WealthWorks!

WealthWorks is a comprehensive financial management platform designed to empower users with tools for budgeting, approval, and wealth accumulation. With intuitive interfaces and insightful analytics, it aims to streamline financial decision-making and foster long-term financial success.

Postman Workspace: https://www.postman.com/prabs222/workspace/wealthworks/request/26808853-008c87b1-7458-4fc4-bdf1-53234fcb8850

Video: https://drive.google.com/drive/folders/1xB2OMdquVWcqiN2vtjMA8eL61V4sQnF3?usp=sharing

## Screenshots:
 
### POST /check-eligibility/
<img src="https://github.com/prabs222/CreditApprovalSystem/assets/106028895/2534c097-bcba-4733-8f2b-9c6e2836ebd9" width="600" height="300">

<br> 

### POST /create-loan/

<img src="https://github.com/prabs222/CreditApprovalSystem/assets/106028895/a70b070e-3fa8-45dd-9491-75357cae37c1" width="550" height="300">

<br> 

### GET /view-loans/:customer_id/


<img src="https://github.com/prabs222/CreditApprovalSystem/assets/106028895/3695e837-a6f4-4b8d-a814-6dd9c8069dcb" width="550" height="300">


### Tech Stacs Used:

Django,
Celery,
Redis,
PostgeeSQL,
Docker,
Docker Compose
Django RESTFramework

## Running the application:

1. Clone this repository or your own fork!
 ```shell
git clone git@github.com:prabs222/CreditApprovalSystem.git
```

2. Navigate to the project's directory.
 ```shell
cd CreditApprovalSystem
```
3. Run below command to build and run the containers
 ```shell
docker-compose up --build
```
Note: This command might take sometime if you are running it the first time!

#### After running the command successfullly this might start the django server at `http://localhost:8000/`

### Next Steps:
You might want to populate the database by using some static data.

4. Make a GET Request to `http://localhost:8000/trigger-import/` to start the data injestion process in the background using Celery, this wll populate data from .xlsx file to postgreSQL Database!

## Using the application:

### Available API routes:

- `'GET /'`: The home route return the list of available routes.
- `'GET /trigger-import/'`: Starts the data injestion process in the background using Celery.
- `'POST /register/'`: Register a new customer.
- `'POST /check-eligibility/'`: Check the loan eligibility.
- `'POST /create-loan/'`: Create a new loan if elligible.
    `{
    "loan_amount": 10000.00,
    "interest_rate": 8,
    "customer_id": 201,
    "tenure": 30
   }`
- `'GET /view-loan/<int:loan_id>/'`: View details of a specific loan based on the loan id.
- `'GET /view-loans/<int:customer_id>/'`: View details of all loans by a customer based on their loan id.

### Using management commands:
Along with API endpoint, this project also supports some management commands:

- `python manage.py import_customers` can be used to import the customer data using cli.
- `python manage.py import_loans` can be used to import the loan data using cli.
