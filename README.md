# rofr-polls
REST API made using Django for a polls app made as an assignment for Rofr Labs.

Steps to Get the project running on your local machine:
1. Clone the repository
2. Create a virtual environment and run: pip install -r requirements.txt
3. Create your own keyconfig.py inside rofr-polls/rofr/rofr/ (alongside settings.py). Put values for DEBUG(boolean), SECRET_KEY(Django secret key), SERVER(boolean -> False, if running locally.)
4. Run python manage.py migrate inside rofr-polls/rofr/
5. Run python manage.py runserver and your development server will be up on localhost:8000/
