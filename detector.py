#Pseudocode available in journal

import math
import random
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

#Non-raspberry Pi cameras can be set up and easily integrated like this
# camera_stream1 = ip of camera stream
# camera_stream2 = ip of camera stream2
 
#When using multiple streams of this sort this variable is easily implemented
#room = ""

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
    
    speak_general_instructions()
    
def find_closest_object_from_label(target_label):
    center_x = float('inf')
    center_y = float('inf')
    min_distance = float('inf')
    
    def convert_to_center_x(x, w):
        return x + (w / 2)
    
    def convert_to_center_y(y, h):
        return y - (h / 2)

    def calculate_distance(x1, y1, x2, y2):
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2);
                
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

def speak_general_instructions():
    #Basic string interpolation to create conversational TTS
    #Multiple sentence forms to be more natural
    #TODO: implement GPT4
    n = random.randomint(1,3)
    
    #Depending on if you are using camera stream information, the room the object is located in is easily implemented as follows
    #text_1 = "The, " + {wanted_item} + " is in the " + {room} + "and it's near or on the " + {closest_item}
    text_1 = "The ," + {wanted_item} + " is next to the " + {closest_item}
    text_2 = "Try checking for the, " + {wanted_item} + " near the " + {closest_item}
    text_3 = "You left your, " + {wanted_item} + "near the " + {closest_item}
    
    if n % 3 == 0:
        speak(text_1)
    elif n % 3 == 1:
        speak(text_2)
    elif n % 3 == 2:
        speak(text_3)

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