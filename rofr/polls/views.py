import re

from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth.models import User
from polls.models import UserProfile, Question, Poll, UserResponse

from rofr import keyconfig

from polls.utils import hasNumbers

# General USER Endpoints

@api_view(["POST"])
def register(request):
    """
        Register a new user and create their UserProfile
    """
    data = request.data
    
    try:

        # Email input check
        email = str(data['email_id'])
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return Response({'message':'Please enter a valid email address.'}, status=403)
        
        # Unique username check
        username = str(data["username"])
        try:
            user = User.objects.get(username=username)
            return Response({"message": "Username taken"}, status=412)
        except User.DoesNotExist:
            pass
        
        # Already registered email check
        if UserProfile.objects.filter(auth_user__email=email).exists():
            return Response({"message": "Email already registered"}, status=412)

        else:
            first_name = str(data['first_name'])
            last_name = data['last_name']
            password = str(data["password"])
            confirm_pass = str(data["confirm_pass"])
            if password != confirm_pass:
                return Response({"message": "Passwords don't match"}, status=412)

            if last_name == None:
                last_name = ''
            
            if (hasNumbers(first_name) or hasNumbers(last_name)):
                return Response({"message": "Invalid first/last name format"}, status=412)

            gender = str(data['gender']) # M/F/O
            valid_values = ["M", "F", "O"]
            if gender not in valid_values:
                return Response({"message": "Invalid gender value"}, status=412)

            age = int(data["age"])

            if not age > 0:
                return Response({"message": "Invalid age value"}, status=412)
            
            location = str(data["location"])
            if location == "":
                return Response({"message": "Please enter a location"}, status=412)
            
            income = int(data['income'])
            if income < 0:
                return Response({"message": "Invalid income value"}, status=412)
            
            try:
                # Create django User
                user = User()
                user.username = username
                user.email = email
                user.set_password(password)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                try:
                    # Create UserProfile
                    profile = UserProfile()
                    profile.auth_user = user
                    profile.gender = gender
                    profile.age = age
                    profile.income = income
                    profile.location = location
                    profile.save()
                    return Response({"message": "Registered!"}, status=201)
                except:
                    user.delete()
                    return Response({"message": "An error occurred. Please try again!"}, status=500)
            except:
                return Response({"message": "An error occurred. Please try again!"}, status=500)
    except KeyError as missing_data:
        return Response({'message':'Data is Missing: {}'.format(missing_data)}, status=400) 

@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def available_polls(request):
    """
        Returns polls available to the user for attempting
    """       
    user = request.user

    polls = Poll.objects.all()
    payload = {
        "available_polls": [],
        "attempted_polls": []
    }
    for poll in polls:
        if poll in user.profile.attempted_polls.all():
            continue
        if (user.profile.age < poll.min_age or user.profile.income < poll.min_income):
            continue
        if (poll.max_age !=0 or poll.max_income != 0):
            if (user.profile.income > poll.max_income or user.profile.age > poll.max_age):
                continue
        questions = poll.questions.all()
        questions_data = []
        for question in questions:
            questions_data.append({
                "id": question.id,
                "title": question.title,
                "type": question.get_category_display(),
                "optional": question.optional
            })
        payload["available_polls"].append({
            "title": poll.title,
            "attempted_count": poll.attempted_count,
            "id": poll.id,
            "no_of_questions": poll.questions.all().count(),
            "questions": questions_data
        })
    
    for poll in user.profile.attempted_polls.all():
        payload["attempted_polls"].append({ # polls history of the user
            "title": poll.title
        })
        
    return Response(payload, status=200)

@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def attempt_poll(request, poll_id):
    """
        Allows users to attempt a poll by ID
    """
    print("*** POLL ID: ***", poll_id)
    user = request.user
    data = request.data

    if user.is_staff:
        return Response({"message": "Admin can't attempt a poll"}, status=412)

    try:
        try:
            poll = Poll.objects.get(id=poll_id)
            print("**** POLL TITLE: ***", poll.title)
            print("**** HEREE *****")
            if user in poll.users_attempted.all():
                print("**** ALREADY TAKEN ****")
                return Response({"message": "You have already taken this poll"}, status=412)
            question_responses = data["question_responses"]
            if len(question_responses) > poll.questions.all().count():
                return Response({"message": "Invalid number of question responses"}, 412)
        except Poll.DoesNotExist:
            return Response({"message": "Poll not found!"}, status=404)

        for question_response in question_responses:
            try:
                question_id = question_response["id"]
                try:
                    question = Question.objects.get(id=question_id)
                except Question.DoesNotExist:
                    return Response({"message": "Invalid question ID"}, status=404)    
                response_input = question_response["response_input"]

                if (question.optional == False and response_input == ""):
                    poll_responses = poll.responses.all()
                    poll_responses.delete()
                    poll.attempted_count -= 1
                    poll.save()
                    user.profile.attempted_polls.remove(poll)
                    user.profile.save()
                    return Response({"message": "Invalid response to question with ID: {}".format(question.id)}, status=412)

                if (question.category == "S"): # if a Scale (1-5) type question
                    try:
                        response_input = int(response_input)
                        if response_input not in range(1, 6):
                            poll_responses = poll.responses.all()
                            poll_responses.delete()
                            poll.attempted_count -= 1
                            poll.save()
                            user.profile.attempted_polls.remove(poll)
                            user.profile.save()
                            return Response({"message": "Question response value must be between 1 and 5"}, status=412)
                    except ValueError:
                        poll_responses = poll.responses.all()
                        poll_responses.delete()
                        poll.attempted_count -= 1
                        poll.save()
                        user.profile.attempted_polls.remove(poll)
                        user.profile.save()
                        return Response({"message": "Invalid response to question with ID: {}".format(question.id)}, status=412)

                response_instance = UserResponse()
                response_instance.poll = poll
                response_instance.question = question
                response_instance.response = response_input
                response_instance.save()

            except KeyError as missing_data:
                return Response({'message':'Data is Missing: {}'.format(missing_data)}, status=400)

        user.profile.attempted_polls.add(poll)
        user.profile.save()
        poll.attempted_count += 1
        poll.save()
        return Response({"message": "Poll taken successfully!"}, status=200)

    except KeyError as missing_data:
        return Response({'message':'Data is Missing: {}'.format(missing_data)}, status=400) 


# Admin API Endpoints

@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def create_poll(request):
    """
        Allows admins to create a new poll
    """       
    user = request.user
    data = request.data
    try:
        title = str(data["title"])
        questions = data["questions"]
        try:
            poll = Poll.objects.get(title=title)
            return Response({"message": "Poll with this title already exists"}, status=412)
        except Poll.DoesNotExist:
            poll = Poll.objects.create(title=title)
            try:
                if data["min_age"] != "":
                    poll.min_age = int(data["min_age"])
            except:
                pass    
            try:
                if data["max_age"] != "":
                    poll.max_age = int(data["max_age"])
            except:
                pass
            try:
                if data["min_income"] != "":
                    poll.min_income = int(data["min_income"])
            except:
                pass
            try:
                if data["max_income"] != "":
                    poll.max_income = int(data["max_income"])            
            except:
                pass
        for question in questions:
            valid_categories = ["MCSO", "MCMO", "OWNI", "S", "E"]
            try:
                question_title = str(question["question_title"])
                category = str(question["category"])
                if category not in valid_categories:
                    poll.delete()
                    return Response({"message": "Invalid question category"}, status=412)
                try:
                    optional = question["optional"]
                    valid_optionals = [True, False]
                    if optional not in valid_optionals:
                        poll.delete()
                        return Response({"message": "Invalid value for optional"}, status=412)
                except:
                    optional = False
                question = Question()
                question.title = question_title
                question.category = category
                question.optional = optional
                question.poll = poll
                question.save()
            except KeyError as missing_data:
                poll.delete()
                return Response({'message':'Data is Missing: {}'.format(missing_data)}, status=400) 
        return Response({"message": "Poll created!"}, status=201)
    except KeyError as missing_data:
        return Response({'message':'Data is Missing: {}'.format(missing_data)}, status=400) 