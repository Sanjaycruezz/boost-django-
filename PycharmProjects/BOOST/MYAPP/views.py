import subprocess
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import never_cache
# Create your views here.
from MYAPP.models import *
import datetime

from .classify_page import check
def logout(request):
    request.session['lid']=''
    return HttpResponse('''<script>alert('Logged Out!,Login again to avail services.');window.location='/'</script>''')

@never_cache
def login(request):
    return render(request,'loginnew.html')
def loginnew(request):
    username=request.POST['textfield']
    password=request.POST['textfield2']
    try:
        a=login_table.objects.get(user_name=username,password=password)
        request.session['lid']=a.id
        if a.type=='admin':
            return  HttpResponse('''<script>alert('Admin logged in !');window.location='/home_page'</script>''')
        elif a.type=='user':
            return  HttpResponse('''<script>alert('User logged in !');window.location='/user_home_page'</script>''')

        else:
            return  HttpResponse('''<script>alert('Invalid Username or Password.');window.location='/'</script>''')
    except:
        return HttpResponse('''<script>alert('Invalid Username or Password.');window.location='/'</script>''')


# def login_post(request):
#     username=request.POST['textfield']
#     password=request.POST['textfield2']
#     a=login_table.objects.get(user_name=username,password=password)
#     request.session['lid']=a.id
#     if a.type=='admin':
#         return  HttpResponse('''<script>alert('Admin logged in !');window.location='/home_page'</script>''')
#
#     else:
#         return  HttpResponse('''<script>alert('Invalid Username or Password.');window.location='/'</script>''')
#
@never_cache
def view_tips(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('Logged Out!,Login again to avail services.');window.location='/'</script>''')

    a=tips_table.objects.all()
    return render(request,'view_tips.html',{'data':a})


def view_tips_delete(request,id):
    a=tips_table.objects.get(id=id)
    a.delete()
    return HttpResponse('''<script>alert('Tip deleted Successfully !');window.location='/view_tips'</script>''')


@never_cache
def add_tip(request):
    if request.session['lid'] == '':
        return HttpResponse('''<script>alert('Logged Out!,Login again to avail services.');window.location='/'</script>''')

    return render(request,'AddNew.html')

def add_tip_post(request):
    tip=request.POST['textfield']
    details=request.POST['textfield2']
    c=tips_table()
    c.tips=tip
    c.details=details
    c.date=datetime.datetime.now()
    c.save()
    return HttpResponse('''<script>alert('Tip added Successfully !');window.location='/view_tips'</script>''')

@never_cache
def edit_tip(request,id):
    request.session['tid']=id
    a=tips_table.objects.get(id=id)
    return render(request,'Edit.html',{'data':a})

def edit_tip_post(request):
    tip = request.POST['textfield']
    details = request.POST['textfield2']
    c = tips_table.objects.get(id=request.session['tid'])
    c.tips = tip
    c.details = details
    c.date = datetime.datetime.now()
    c.save()
    return HttpResponse('''<script>alert('Tip edited ! ');window.location='/view_tips'</script>''')


@never_cache
def view_complaints(request):
    if request.session['lid'] == '':
        return HttpResponse('''<script>alert('Logged Out!,Login again to avail services.');window.location='/'</script>''')

    d=complaint_table.objects.all()
    return render(request,'view_complaints.html',{"data":d})

@never_cache
def view_feedback(request):
    if request.session['lid'] == '':
        return HttpResponse('''<script>alert('Logged Out!,Login again to avail services.');window.location='/'</script>''')

    e=feedback.objects.all()
    return render(request,'view_feedback.html',{'data':e})

@never_cache
def view_user(request):
    if request.session['lid'] == '':
        return HttpResponse('''<script>alert('Logged Out!,Login again to avail services.');window.location='/'</script>''')

    f=user_table.objects.all()
    return render(request ,'view_user.html',{'data':f})


@never_cache
def home_page(request):
    if request.session['lid'] == '':
        return HttpResponse('''<script>alert('Logged Out!,Login again to avail services.');window.location='/'</script>''')

    return render(request ,'index.html')

def reply(request,id):
   request.session['cid']=id
   return render(request ,'Reply.html')

def reply_post(request):
    reply=request.POST['textfield2']
    cid=request.session['cid']
    r=complaint_table.objects.get(id=cid)
    r.reply=reply
    r.save()
    return HttpResponse('''<script>alert('Reply sent !');window.location='/view_complaints'</script>''')


#-----------------------------------------------------------------------------------------------------------------------


def android_login(request):
    username=request.POST['username']
    password=request.POST['password']


    a=login_table.objects.filter(user_name=username,password=password)
    if a.exists():
        b = login_table.objects.get(user_name=username, password=password)
        if b.type == 'user':

            obx=user_table.objects.filter(LOGIN=b.id)

            if len(obx)>0:
                return JsonResponse({'status':'ok','lid':str(b.id),'type':b.type,"height":obx[0].height,"weight":obx[0].weight})
            else:
                return JsonResponse({'status': 'not ok', })

        else:
            return JsonResponse({'status':'not ok',})
    else:
        return JsonResponse({'status': 'not ok', })


def view_profile(request):
    lid = request.POST['lid']
    user = user_table.objects.get(LOGIN=lid)
    profile = [{

        'name':user.name,
        'age' :user.age,
        'email':user.email,
        'phone_no':user.phone_no,
        'height':user.height,
        'weight':user.weight,
        'photo':user.photo.url[1:],
        'gender':user.gender


    }]
    return JsonResponse({'status': 'ok',"data":profile })

def ViewMyComplaints(request):
    lid = request.POST['id']
    user = user_table.objects.get(LOGIN=lid)
    complaint = []
    com = complaint_table.objects.filter(USER=user)
    for i in com:
        complaint.append({
            'id':i.id,
            'complaint':i.complaint,
            'reply':i.reply,
            'date':i.date
        })
    return JsonResponse({'status':'ok','complaint':complaint})

def SendAppComplaint(request):
    lid=request.POST['id']
    complaint=request.POST['complaint']
    c=complaint_table()
    c.complaint=complaint
    c.reply='pending'
    c.date=datetime.datetime.now().date()
    c.USER = user_table.objects.get(LOGIN=lid)
    c.save()
    return JsonResponse({'status':'ok'})

def DeleteMyComplaint(request):
    id = request.POST['complaint_id']
    a=complaint_table.objects.get(id=id)
    a.delete()
    return JsonResponse({'status':'ok'})

def viewfeedback(request):
    lid = request.POST['lid']
    user = user_table.objects.get(LOGIN=lid)
    feedbacks = []
    f = feedback.objects.filter(USER=user)
    for i in f:
        feedbacks.append({
            'id': i.id,
            'feedback': i.feedback,
            'date': i.date
        })
    print(feedbacks)
    return JsonResponse({'status': 'ok', 'feedback': feedbacks})

def sendfeedback(request):
    lid=request.POST['lid']
    fb=request.POST['feedback']
    c=feedback()
    c.feedback=fb
    c.date=datetime.datetime.now()
    c.USER = user_table.objects.get(LOGIN=lid)
    c.save()
    return JsonResponse({'status':'ok'})


from django.http import JsonResponse
import base64
import json

from .models import login_table, user_table  # Assuming your models are imported correctly


def registrationcode(request):
    # Retrieving form data
    fname = request.POST.get('fname')
    lname = request.POST.get('lname')
    email = request.POST.get('email')
    phone = request.POST['phone']
    age = request.POST['age']
    height = request.POST.get('height')
    weight = request.POST.get('weight')
    uname = request.POST.get('username')
    password = request.POST.get('password')
    gender = request.POST.get('gender')
    photo = request.FILES['photo']

    # Checking if the image is provided
    if not photo:
        return JsonResponse({'task': 'invalid', 'message': 'No photo uploaded'})
    fs=FileSystemStorage()
    fsave=fs.save(photo.name,photo)

    # Create login entry
    login_obj = login_table()
    login_obj.user_name = uname
    login_obj.password = password
    login_obj.type = 'user'
    login_obj.save()

    # Create user entry
    user_obj = user_table()
    user_obj.LOGIN = login_obj
    user_obj.name = fname+" "+lname  # Concatenate first and last name
    user_obj.email = email
    user_obj.age = age
    user_obj.phone_no = phone
    user_obj.height = height
    user_obj.weight = weight
    user_obj.gender = gender
    user_obj.photo = fsave  # Save relative image path
    user_obj.save()

    # Return a response indicating success
    data = {"task": "ok"}
    response = json.dumps(data)
    print(response)

    return JsonResponse({'task': 'valid', 'message': 'User registered successfully'})

from django.http import JsonResponse
from .models import dietplan


def diet_plan(request):
    if request.method == 'POST':
        # Retrieving form data
        lid = request.POST.get('lid')  # Assuming this is the user's login ID
        # age = request.POST.get('age')
        # height = request.POST.get('height')
        # weight = request.POST.get('weight')
        # gender = request.POST.get('gender')
        activity_level = request.POST.get('activity_level')
        goal = request.POST.get('goal')
        diet_type = request.POST.get('diet_type')
        medical_condition = request.POST.get('medical_condition', '')  # Optional field
        msg1 = (
            "I need a structured diet plan for a day.i am a person with the activity level of "+str(activity_level)+" My goal is " + str(goal) + ", and my preferred diet type is " + str(diet_type) +
            ". I have the following dietary restrictions or medical conditions: " + str(medical_condition) +
            ". Structure a simple, well-balanced meal plan for me, ensuring it aligns with my fitness goal."
            "prepare diet plan for exactly one day with 4 meals in one day"
            "1. No need to generate other unnecessary details. I only require the meal names, their brief descriptions, and meal prep instructions."
            "2. Present the diet plan in a well-structured manner where each day's meals are clearly separated and the readability is enhanced."
            "3. Remove introductory sentences and unnecessary details."
            "4. Provide a properly numbered and structured diet plan, highlighting meals involved."
            "5. Only require the meal name, a short description, and meal prep instructions (e.g., 'Grilled Chicken with Quinoa & Steamed Vegetables – Marinate chicken overnight, grill for 10 minutes per side, cook quinoa separately')."
            "6. At the end of the plan, generate a sentence asking users to refer to the AI assistant within the app for any doubts or clarifications regarding the diet recommendations."
            "7. Provide proper instructions regarding hydration, portion control, and nutrient balance."
            "8. Include meal prep instructions that are simple, efficient, and optimized ."
            "10. Present the plan in a well-structured and aesthetically pleasing design, highlighting meal names and meal prep details properly."
            "11.try to include indian food items to max"
            "12.budget friendly alternative should be discussed"
            "13. a easy to understand and not cpmplicated meal prep is to be provided"
            " 14.provide 4 meal plans for the day and also display the calorie per each meal"
            " sample = Meal 1: egg omlet - calorie(0000) then followed by a simple meal prep"
            "after the meal name and calorie then show the ingredients required and meal prep "
            "each ingredient must be displayed as a seperate point or bulletine"
            "strictly follow the 13 points mentionedMake sure all 13 points mentioned are strictly followed."
        )

        sol = dietbot_response(msg1)
        print(sol)

        return JsonResponse({'task': 'ok', 'message': sol})

        # Validate required fields
        if not all([lid, activity_level, goal, diet_type]):
            return JsonResponse({'task': 'invalid', 'message': 'Missing required fields'})

        try:
            # Create DietPlan object manually
            diet_plan_obj = dietplan()
            # diet_plan_obj.age = age
            # diet_plan_obj.height = height
            # diet_plan_obj.weight = weight
            # diet_plan_obj.gender = gender
            diet_plan_obj.USER = user_table.objects.get(LOGIN_id=lid)
            diet_plan_obj.activity_level = activity_level
            diet_plan_obj.goal = goal
            diet_plan_obj.diet_type = diet_type
            diet_plan_obj.medical_condition = medical_condition
            # Save the object to the database
            diet_plan_obj.save()

            # Return success response
            return JsonResponse({'task': 'ok', 'message': sol})
            return JsonResponse({'status': 'ok', 'message': sol, 'lid': lid})
        except Exception as e:
            # Handle database errors
            print("++++++++++++++++****************")
            print(e)
            return JsonResponse({'task': 'ok', 'message': sol})
            return JsonResponse({'task': 'ok', 'message': sol})
            return JsonResponse({'task': 'error', 'message': str(e)})
    else:
        # Handle invalid request method
        print("======================")
        return JsonResponse({'task': 'ok', 'message': ""})
        return JsonResponse({'task': 'invalid', 'message': 'Invalid request method'})

import datetime
from django.http import JsonResponse

def workout_plan(request):
    lid = request.POST['lid']
    goal = request.POST['goal']
    workout_days = request.POST['workout_days']
    equipment = request.POST['equipment']
    squats = request.POST['can_do_squats']
    maximumpushup = request.POST['max_pushups']
    plank = request.POST['plank_time']

    msg = (
        f"I need a workout plan. My goal is {goal}, and I can work out for {workout_days} days a week. "
        f"I have the following equipment: {equipment}. "
        f"I can perform a maximum of {maximumpushup} push-ups at a time and a maximum of {squats} squats at a time. "
        f"I can hold the plank position for {plank} seconds. I am a beginner to workouts and gym training. "
        f"Structure a simple workout plan for me, including warm-up exercises before each session. "
        f"Ensure the workout days align with the number of days I can work out, based on the following structure:\n"
        f"Monday: Chest & Triceps\n"
        f"Tuesday: Cardio\n"
        f"Wednesday: Back & Shoulders\n"
        f"Thursday: Abs & Core\n"
        f"Friday: Legs & Arms\n"
        f"Saturday: Stretches & Recovery\n"
        f"Sunday: Rest Day\n"
        f"If I can only work out for fewer than 6 days, prioritize the most essential workouts "
        f"(Chest & Triceps, Back & Shoulders, Abs & Core, and Legs & Arms) while still including necessary cardio and recovery.\n"
        f"1. No need to generate other information. I only require the day, the workouts for that day, the workout name, "
        f"and the number of suggested repetitions and sets.\n"
        f"2. Also give the workout plan in a very structured manner where each workout is properly separated and the readability is enhanced.\n"
        f"3. Remove introductory sentences and unnecessary details.\n"
        f"4. Provide properly numbered and structured workout plan, highlight the days and workouts involved.\n"
        f"5. Only require the name, rep count, and set numbers mentioned like (push-up 20 reps * 3 sets).\n"
        f"6. At the end of the plan, generate a sentence.\n"
        f"7. Similarly, generate a sentence which basically asks to refer the AI assistant issued within the app for any doubts or clarification regarding the workouts given.\n"
        f"9. Provide a well-structured and aesthetically pleasing design for it.\n"
        f"10. Highlight each workout name and the reps and set count.\n"
        f"11. Also show calories being burned while each workout is being completed.\n"
        f"12. Also show the total calories to be burned by the end of the workouts.\n"
        f"Generate the workout plan like the below, provided for each individual day:\n"
        f"Monday: Chest & Triceps\n"
        f"1. Push-ups: 10 reps * 3 sets (approx. 100 calories burned)\n"
        f"2. Dumbbell Bench Press: 10 reps * 3 sets (approx. 150 calories burned)\n"
        f"3. Dumbbell Incline Press: 10 reps * 3 sets (approx. 120 calories burned)\n"
        f"4. Dumbbell Triceps Extensions: 12 reps * 3 sets (approx. 100 calories burned)\n"
        f"5. Close-Grip Dumbbell Bench Press: 10 reps * 3 sets (approx. 100 calories burned)"
    )

    sol, tcal = workbot_response(msg)
    print(sol)

    workout_plan_obj = workoutplan()
    workout_plan_obj.USER = user_table.objects.get(LOGIN_id=lid)
    workout_plan_obj.squats = squats
    workout_plan_obj.goal = goal
    workout_plan_obj.workoutdays = workout_days
    workout_plan_obj.equipements = equipment
    workout_plan_obj.maximumpushup = maximumpushup
    workout_plan_obj.plank = plank
    workout_plan_obj.save()

    ob = calorie()
    ob.date = datetime.datetime.today()
    ob.cal_burn = tcal
    ob.save()

    return JsonResponse({'status': 'ok', 'message': sol})


def get_user_details(request):
    lid = request.GET.get("lid")
    user = user_table.objects.get(LOGIN_id=lid)

    data = {
        "age": user.age,
        "height": user.height,
        "weight": user.weight,
        "gender": user.gender,
    }

    return JsonResponse(data)



from django.http import JsonResponse
from .models import user_table  # Ensure you import your user_table model

def update_profile(request):
    lid = request.POST['lid']
    try:
        user = user_table.objects.get(LOGIN=lid)
        user.name = request.POST.get('name', user.name)
        user.age = request.POST.get('age',user.age)# Use 'name' instead of 'fname' and 'lname'
        user.email = request.POST.get('email', user.email)
        user.phone_no = request.POST.get('phone', user.phone_no)
        user.height = request.POST.get('height', user.height)
        user.weight = request.POST.get('weight', user.weight)
        user.gender = request.POST.get('gender', user.gender)
        user.photo = request.FILES.get('photo',user.photo)
        user.save()
        return JsonResponse({'status': 'ok', 'message': 'Profile updated successfully'})
    except user_table.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found'})


# import textwrap
# import google.generativeai as genai
# from django.http import JsonResponse
# from django.shortcuts import render
#
# # Configure Google Gemini API
# GOOGLE_API_KEY = 'AIzaSyCl3OkF02hWTyZMo82-lXYZMufC6vWapH4'
# genai.configure(api_key=GOOGLE_API_KEY)
#
# # Select a Generative Model
# model = None
# for m in genai.list_models():
#     if 'generateContent' in m.supported_generation_methods:
#         print("Using model: {m.name}")
#         model = genai.GenerativeModel('gemini-1.5-flash')
#         break
#
# def generate_gemini_response(prompt):
#     """
#     Generate a response using the Gemini model with a context about Sreepathy College.
#     """
#     context_prompt = " {prompt}"
#     try:
#         response = model.generate_content(context_prompt)
#         return response.text.strip()
#     except Exception as e:
#         return "Error generating response: {str(e)}"
#
#
# # def chatbot_home(request):
# #     """
# #     Render the chatbot homepage.
# #     """
# #     return render(request, 'chatbot/index.html')
#
#
# # def chatbot_response(request):
# #
# #     """
# #     Process user messages and return chatbot responses.
# #     """
# #     if request.method == "POST":
# #         kk = request.POST.get('message', '')
# #         print(kk, "oooooooooooooooo")
# #         user_message = request.POST.get('message', '').strip()
# #         print(user_message,"kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
# #         if not user_message:
# #             return JsonResponse({'response': 'Please enter a valid question.'})
# #
# #         # Generate a response from Gemini
# #         gemini_response = generate_gemini_response(user_message)
# #         return JsonResponse({'response': gemini_response})
# #
# #     return JsonResponse({'response': 'Invalid request method.'})
# import textwrap
# import google.generativeai as genai
# from django.http import JsonResponse
# from django.shortcuts import render
#
# # Configure Google Gemini API
# GOOGLE_API_KEY = 'AIzaSyCl3OkF02hWTyZMo82-lXYZMufC6vWapH4'
# genai.configure(api_key=GOOGLE_API_KEY)
#
# # Select a Generative Model
# model = None
# for m in genai.list_models():
#     if 'generateContent' in m.supported_generation_methods:
#         print("Using model: {m.name}")
#         model = genai.GenerativeModel('gemini-1.5-flash')
#         break
#
# from django.http import JsonResponse
# import json
#
# def chatbot_response(request):
#     """
#     Process user messages and return chatbot responses.
#     """
#     if request.method == "POST":
#         try:
#             print(request.body)
#             # Parse the incoming JSON data
#             data = json.loads(request.body)
#             print(data)
#             user_message = data.get('message', '').strip()
#
#             print(user_message, "Received message")
#
#             if not user_message:
#                 return JsonResponse({'response': 'Please enter a valid question.'})
#
#             # Generate a response from Gemini (you would need to implement this function)
#             try:
#                 response = model.generate_content(user_message)
#                 return response.text.strip()
#             except Exception as e:
#                 return "Error generating response: {str(e)}"
#             return JsonResponse({'response': gemini_response})
#
#         except json.JSONDecodeError:
#             # If JSON is not valid, return an error response
#             return JsonResponse({'response': 'Invalid JSON format.'})
#
#     return JsonResponse({'response': 'Invalid request method.'})
#
#

import json
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Configure Google Gemini API
GOOGLE_API_KEY = 'AIzaSyB_G0I9odde2-IwZHB1EgHGmBTKaFvSf6Y'  # Replace with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)

model = None
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print("Using model: {m.name}")
        model = genai.GenerativeModel('gemini-1.5-flash')
        break

def generate_gemini_response(prompt):
    """
    Generate a response using the Gemini model with a context about Sreepathy College.
    """
    context_prompt = " {prompt}"
    try:
        response = model.generate_content(context_prompt)
        return response.text.strip()
    except Exception as e:
        return "Error generating response: {str(e)}"

# Initialize Gemini Model
model = genai.GenerativeModel('gemini-1.5-flash')


@csrf_exempt  # Allows POST requests without CSRF token (Only for testing, secure in production)
def chatbot_response(request):
    """
    Handles user input and generates a response from the Gemini API.
    """
    if request.method == 'POST':
        try:
            # Parse JSON request body
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()

            if not user_message:
                return JsonResponse({'response': 'Please enter a valid question.'})

            # Generate response from Gemini
            gemini_response = model.generate_content(user_message)

            # Ensure response is always JSON formatted
            return JsonResponse({'response': gemini_response.text.strip()})

        except json.JSONDecodeError:
            return JsonResponse({'response': 'Invalid JSON format.'}, status=400)
        except Exception as e:
            return JsonResponse({'response': 'Error: {str(e)}'}, status=500)

    return JsonResponse({'response': 'Invalid request method. Use POST.'}, status=405)


def workbot_response(txt):

    user_message = txt

    if not user_message:
        return JsonResponse({'response': 'Please enter a valid question.'})

    # Generate response from Gemini
    gemini_response = model.generate_content(  user_message
)

    print(gemini_response.text.strip())
    res=gemini_response.text.strip()
    res1=res.split('calorie')
    tcal=0
    for i in res1:
        try:
            tcal+=float(i.split(' ')[-1])
        except Exception as e:
            try:
                tcal += float(i.split(' ')[-2])
            except Exception as e:
                print(e)

    print("tcal",tcal)
    # Ensure response is always JSON formatted
    return res,tcal


@csrf_exempt  # Allows POST requests without CSRF token (Only for testing, secure in production)
def chatbot_response(request):
    """
    Handles user input and generates a response from the Gemini API.
    """
    if request.method == 'POST':
        try:
            # Parse JSON request body
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()

            if not user_message:
                return JsonResponse({'response': 'Please enter a valid question.'})

            # Generate response from Gemini
            gemini_response = model.generate_content(user_message)

            # Ensure response is always JSON formatted
            print({'response': gemini_response.text.strip(),"task":"ok"})
            return JsonResponse({'response': gemini_response.text.strip(),"task":"ok"})

        except json.JSONDecodeError:
            return JsonResponse({'response': 'Invalid JSON format.'}, status=400)
        except Exception as e:
            return JsonResponse({'response': 'Error: {str(e)}'}, status=500)

    return JsonResponse({'response': 'Invalid request method. Use POST.'}, status=405)


def dietbot_response(txt):

    user_message = txt

    if not user_message:
        return JsonResponse({'response': 'Please enter a valid question.'})

    # Generate response from Gemini
    gemini_response = model.generate_content(  user_message
)

    print(gemini_response.text.strip())

    # Ensure response is always JSON formatted
    return gemini_response.text.strip()


def getbmi(request):
    lid=request.POST["lid"]
    obx = user_table.objects.filter(LOGIN=lid)

    if len(obx) > 0:
        return JsonResponse(
            {'status': 'ok', "height": obx[0].height, "weight": obx[0].weight})
    else:
        return JsonResponse({'status': 'not ok', })



def forgot_password_flutter(request):
    try:
        username = request.POST['username']
        s = login_table.objects.get(user_name=username)

        # If user is not found or doesn't exist, return an invalid response
        if s is None:
            return JsonResponse({"status": "Invalid username"})
        else:
            # Fetch the Organization associated with the Login object
            try:
                user = user_table.objects.get(LOGIN=s)
                email_address = user.email  # Assuming email is in Organization model
            except user_table.DoesNotExist:
                return JsonResponse({"status": "Email not available"})

            if not email_address:
                return JsonResponse({"status": "Email not available"})

            # Create the email content
            subject = 'BOOST Password Reset'
            message = f"Your password is: {s.password}"
            from_email = 'sanjaykrishna107@gmail.com'

            try:
                # Send the email with the password to the user's email address
                send_mail(subject, message, from_email, [email_address])
                return JsonResponse({"status": "ok"})
            except Exception as e:
                print(f"Error sending email: {str(e)}")
                return JsonResponse({"status": "Email sending failed"})
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({"status": "Error occurred"})


def forgot_password_web(request):
    if request.method == 'POST':
        username = request.POST['username']
        s = login_table.objects.get(user_name=username)
        user = user_table.objects.get(LOGIN=s)
        email_address = user.email


        subject = 'BOOST Password Reset'
        message = f"Your password is: {s.password}"
        from_email = 'sanjaykrishna107@gmail.com'

        send_mail(subject, message, from_email, [email_address])
        return HttpResponse('''<script>alert('Password Sent Successfully');window.location='/'</script>''')
    return render(request, 'forgot_password.html')



def change_password(request):
    old = request.POST['current_password']
    lid = request.POST['id']
    new = request.POST['new_password']
    confirm = request.POST['confirm_password']

    if login_table.objects.filter(id=lid,password=old).exists():
        if new == confirm:
            a = login_table.objects.get(id=lid, password=old)
            a.password = confirm
            a.save()
            return JsonResponse({'status':'ok'})
        else:
            return JsonResponse({'status': 'not ok'})
    else:
        return JsonResponse({'status': 'not ok'})

def web_change_password(request):
    if request.method == 'POST':
        current = request.POST['current']
        new = request.POST['new']
        confirm = request.POST['confirm']

        if login_table.objects.filter(id=request.session['lid'], password=current).exists():
            if new == confirm:
                a = login_table.objects.get(id=request.session['lid'], password=current)
                a.password = confirm
                a.save()
                return HttpResponse('''<script>alert('Password Changed Successfully');window.location='/home_page'</script>''')
            else:
                return HttpResponse('''<script>alert('New and Confirm Password mismatch');window.location='/web_change_password'</script>''')
        else:
            return HttpResponse('''<script>alert('No Data Found');window.location='/home_page'</script>''')
    return render(request, 'change_password.html')

from .gemini import analyze_food_image
def upload_image(request):
        print(request.FILES)
        if request.method == 'POST':
            print(request.FILES)
            print(request.POST)
            img = request.FILES['image']
            fs = FileSystemStorage()
            fn = fs.save(img.name, img)

            path = r"C:\Users\sanja\PycharmProjects\BOOST\media/" + fn
            res=check(path)



            print("==================")

            print(res)
            res=analyze_food_image(res)
            # result = subprocess.run(
            #     [r'C:\Users\user\AppData\Local\Programs\Python\Python36\python',
            #      r'C:\Users\sanja\Downloads\Food_robo_yolov8n\Food_robo_yolov8n\main.py'],
            #     # Replace with your script or command
            #     input=path.encode('utf-8')
            #
            # )
            # file1 = open(r"C:\Users\user\PycharmProjects\lungabnormality\sample.txt", "r")
            # print("Output of Readlines after writing")
            # print()
            # ss = file1.readlines()
            # print(ss, "false", str(ss[0]) == "false")
            # try:
            #     if str(ss[0]) == "false":
            #         print("True")
            #         request.session["predicting"] = fn
            #         return JsonResponse({'status': 'ok', 'message1': "Invalid Image"})
            # except:
            #     pass
            #
            # res1 = prediction_function1(r"C:\Users\user\PycharmProjects\lungabnormality\media/" + fn)
            # print(res1)
            return JsonResponse({'status': 'ok', 'message1': res})

        else:
            return JsonResponse({'status': 'error', 'message1': 'Invalid request method. Use POST.'})


def user_home_page(request):
    return render(request,'user/userindex.html')
    # return render(request,'user/home.html')

def view_user_excercise_information(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('Logged Out!,Login again to avail services.');window.location='/'</script>''')
    ob = Excercise.objects.filter(USER__LOGIN=request.session['lid'])
    for i in ob:
        if i.excercise=='plank':
            i.Count=i.Count//30
    return render(request, 'user/view_excercise_information.html',{'data':ob})

def excercises(request):
    if request.session['lid']=='':
        return HttpResponse('''<script>alert('Logged Out!,Login again to avail services.');window.location='/'</script>''')
    return render(request,'user/excercise_types.html')


import subprocess

def biceps(request):
    result=subprocess.run(
        [r'C:\Users\sanja\AppData\Local\Programs\Python\Python310\python',r'C:\Users\sanja\OneDrive\Desktop\workout\core\core\bicep_model\predictionfile.py'],
        input=str(request.session['lid']).encode('utf-8')
    )
    return render(request,'user/excercise_types.html')

def lunges(request):
    result=subprocess.run(
        [r'C:\Users\sanja\AppData\Local\Programs\Python\Python310\python',r'C:\Users\sanja\OneDrive\Desktop\workout\core\core\lunge_model\predict_lunge.py'],
        input=str(request.session['lid']).encode('utf-8')
    )
    return render(request,'user/excercise_types.html')

def plank(request):
    result=subprocess.run(
        [r'C:\Users\sanja\AppData\Local\Programs\Python\Python310\python',r'C:\Users\sanja\OneDrive\Desktop\workout\core\core\plank_model\predict_plank.py'],
        input=str(request.session['lid']).encode('utf-8')
    )
    return render(request,'user/excercise_types.html')

def squat(request):
    result=subprocess.run(
        [r'C:\Users\sanja\AppData\Local\Programs\Python\Python310\python',r'C:\Users\sanja\OneDrive\Desktop\workout\core\core\squat_model\predict_sqat.py'],
        input=str(request.session['lid']).encode('utf-8')
    )
    return render(request,'user/excercise_types.html')

def update_count(request):
    lid=request.GET['lid']
    etype=request.GET['type']
    ob=Excercise.objects.filter(USER__LOGIN__id=lid,date=datetime.datetime.today(),excercise=etype)
    if len(ob)==0:
        ob=Excercise()
        ob.USER = user_table.objects.get(LOGIN__id=lid)
        ob.date = datetime.datetime.today()
        ob.excercise = etype
        ob.Count = 1
        ob.save()
    else:
        ob = ob[0]

        ob.Count += 1
        ob.save()
    return JsonResponse({"task":"ok"})