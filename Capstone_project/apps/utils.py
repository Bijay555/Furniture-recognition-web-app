from ibm_watson import VisualRecognitionV3, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from operator import itemgetter
import json
import os

def classify_image(api_key, classifier_id):
    # connect with the watson visual recognition account
    authenticator = IAMAuthenticator(api_key)

    visual_recognition = VisualRecognitionV3(version='2018-03-19', authenticator=authenticator)
    visual_recognition.set_service_url('https://gateway.watsonplatform.net/visual-recognition/api')
    
    img_path = "image-file"
    img_path_images = os.getcwd() + "/" + img_path
    test_file_names=[os.path.join(img_path_images, f) for f in os.listdir(img_path_images) if f.endswith(".jpg") or f.endswith(".png")]

    top_sorted_class_scores = []
    
    for img_name in test_file_names:
        try:
            
            with open(img_name, "rb") as image_file:
                # pass image to custom classifier, specify custom classifier using classifier_id here
                res_classification = visual_recognition.classify(
                images_file=image_file,
                threshold='0.1',
                classifier_ids=[classifier_id]).get_result()
            class_scores_img = []
            for img_class in res_classification["images"][0]["classifiers"][0]["classes"]:
                class_scores_img.append(img_class)
            sorted_class_scores = sorted(class_scores_img, key=itemgetter("score"), reverse=True)
            if len(sorted_class_scores) > 3:
                top_sorted_class_scores = sorted_class_scores[0:3]
            else:
                top_sorted_class_scores = sorted_class_scores
        except ApiException as ex:
            print(ex)
    return top_sorted_class_scores
