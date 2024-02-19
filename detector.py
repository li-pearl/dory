from imageai.Detection import ObjectDetection  
#Import ObjectDetection class from the ImageAI library.
detector = ObjectDetection()  #create an instance of the class ObjectDetection
model_path = "./models/yolo-tiny.h5"
input_path = "./input/1.jpg"
output_path = "./output/newimage.jpg"  #specify the path from our input image, output image, and model.
detector.setModelTypeAsTinyYOLOv3()   #Using the pre-trained TinyYOLOv3 model, and hence we will use the setModelTypeAsTinyYOLOv3() function to load our model.
detector.setModelPath(model_path)  #function which accepts a string which contains the path to the pre-trained model.
detector.loadModel()  #Loads the model from the path specified above using the setModelPath() class method.
detection = detector.detectObjectsFromImage(input_image=input_path, output_image_path=output_path)  #function returns a dictionary which contains the names and percentage probabilities of all the objects detected in the image.
for eachItem in detection:
    print(eachItem["name"] , " : ", eachItem["percentage_probability"])  #The dictionary items can be accessed by traversing through each item in the dictionary.