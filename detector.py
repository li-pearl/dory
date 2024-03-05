import math
import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
import pyttsx3
import keyboard
import speech_recognition as sr
import RPi.GPIO as GPIO

engine = pyttsx3.init()

print("Setting Up GPIO pins")
GPIO.setmode(GPIO.BCM)
#Setting GPIO pin numbers for speak and quit buttons
speak_button = 14
quit_button = 15
#TODO: Add close range button for ease of use

labels = []
wanted_item = ""
closest_item = ""

def listen_recognize_and_find_closet_and_speak():
    recognizer = sr.Recognizer()
    translated_text = ""

    with sr.Microphone() as source:
        print("Say something while holding T:")
        keyboard.wait("T")  # Wait for the 'T' key to be pressed

        print("Listening...")
        audio = recognizer.listen(source)

    try:
        # Using Google Web Speech API to convert speech to text
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        translated_text = text
    except sr.UnknownValueError:
        print("Could not understand audio")
        translated_text = ""
    except sr.RequestError as e:
        print("Error with the speech recognition service; {0}".format(e))
        translated_text = ""
        
    split_text = translated_text.split()
    
    for item1 in split_text:
        for item2 in labels:
            if item1 == item2:
                wanted_item = item1
                
    closest_item = find_closest_object_from_label(wanted_item)
    
def convert_to_center_x(x, w):
    return x + (w / 2)
    
def convert_to_center_y(y, h):
    return y - (h / 2)

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2);
                
def find_closest_object_from_label(target_label):
    center_x = float('inf')
    center_y = float('inf')
    min_distance = float('inf')
    
    for label, box in zip(labels, bbox):
        if label == target_label:
            x, y, w, h = box
            center_x = convert_to_center_x(x, w)
            center_y = convert_to_center_y(y, h)
            
        for label, (other_center_x, other_center_y) in zip(labels, bbox):
            x2, y2, w2, h2 = box
            other_center_x = convert_to_center_x(x2, w2)
            other_center_y = convert_to_center_y(y2, h2)
            
            distance = calculate_distance(center_x, center_y, other_center_x, other_center_y)
            if distance < min_distance:
                min_distance = distance
                closest_item = label

    return closest_item

def speak(text):
    engine.say(text)
    engine.runAndWait()

video = cv2.VideoCapture(0)

def is_object_seen_close_range (wanted_item):#Used for close-range TODO: Update implementation
    for item in labels:
        if wanted_item == item:
            return True
    return False
     
process_this_frame = True
while True:   
     ret, frame = video.read()
  
     if process_this_frame:
          
        bbox, label, conf = cv.detect_common_objects(frame)
        output_image = draw_bbox(frame, bbox, label, conf)
          
        cv2.imshow("Household Object Detection", output_image)
          
        for item in label: #Can easily be repeated for multiple camera streams
            if item in labels:
                pass
            else:
                labels.append(item)
        
        if 0xFF == ord('t'):
            listen_recognize_and_find_closet_and_speak()
            
        if 0xFF == ord('c'):
            if is_object_seen_close_range(wanted_item) == True:
                speak("You should be able to see the, " + {wanted_item} + " now")
                    
        if cv2.waitKey(1) & 0xFF == ord('s'): #Used for testing purposes
            print("Speaking " + item)
            speak(item)
          
     process_this_frame = not process_this_frame
          
     if cv2.waitKey(1) & 0xFF == ord("q"):
          break


video.release()
cv2.destroyAllWindows()

# proximity_label = "s"

# i = 0
# new_sentence = []
# for label in labels:
#      if i==0:
#           new_sentence.append(f"There is a {label}, and, ")
#      else:
#           new_sentence.append(f"next to {proximity_label}")
#      i+=1
     
# print(" ".join(new_sentence))

