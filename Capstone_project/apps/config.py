import os
class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    UPLOAD_FOLDER = "image-file"
    CSRF_ENABLED = True
    DEBUG = False
    
    # Enter your API Key and Custom Classifier ID below
    API_KEY = "tEfL-y2UDc0O_EdGRhnwQ_YgW4MLQTyOjdQWHyagZKQl"
    CLASSIFIER_ID = "furnitureclassifier_1867463515"
