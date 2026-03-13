from deepface import DeepFace

def analyze_face(img_path):

    result = DeepFace.analyze(
        img_path,
        actions=['emotion']
    )

    return result

def confidence_score(emotion):

    if emotion == "happy" or emotion == "neutral":
        return 80

    elif emotion == "fear":
        return 40

    else:
        return 60