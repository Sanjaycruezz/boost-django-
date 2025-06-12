from ultralytics import YOLO
import google.generativeai as genai

# Configure YOLO model
yolo_model = YOLO(r"C:\Users\sanja\Downloads\Food_robo_yolov8n\Food_robo_yolov8n\runs\detect\train\weights\best.pt")

# Configure Gemini
GOOGLE_API_KEY = 'AIzaSyBNiIWvapx55xyr3trTuTKhZkk8HPt0y3g'
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Gemini model
gemini_model = None
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        break


def get_detected_foods(image_path):
    results = yolo_model(image_path)
    detected_foods = []

    for result in results:
        for box in result.boxes:
            class_name = result.names[int(box.cls[0])]
            detected_foods.append(class_name)
    print("detected foods================")
    print(detected_foods)
    return detected_foods


def generate_health_advice(foods):
    # Create a prompt for Gemini that includes the detected foods
    foods_list = ", ".join(foods)
    prompt = f"""I have eaten the following food: {foods_list}. 
    Please provide:
    START DIRECTLY FROM THE POINTS MENTIONED TO BE ANSWERED FROM DWN HERE
    1. the calorie of the food consumed  with its name
    2. identify the different items in it and display the nutritional content of it
    3. display these details in a very structured and easy to understand manner
    4. an example of how it is to be displayed
                    BURGER
    Calorie-
    fats- 
    protien
    carbs-
    other nutrients etc in the same order
    remove unnecessary introductory sentences i only require the the nutritional content of the food image uploaded so keep that in mind
    provide proper highlighted texts and write down the nutrietional content one by one and increase the overall readability of the content"""

    response = gemini_model.generate_content(prompt)
    return response.text


def analyze_food_image(image_path):

    health_advice = generate_health_advice([image_path])
    print("\nAnalysis Results:")
    return(health_advice)


# if __name__ == '__main__':
#     image_path = r"C:\Users\sanja\Downloads\Food_robo_yolov8n\Food_robo_yolov8n\food2.jpg"
#     res = analyze_food_image(image_path)