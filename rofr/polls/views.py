import re

from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth.models import User
from polls.models import UserProfile, Question, Poll

from rofr import keyconfig

from polls.utils import hasNumbers

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