from fastai.vision.all import load_learner

learn = load_learner(r"C:\Users\mcgourthyn\Pictures\images\model.pkl")
image_path = (r"C:\Users\mcgourthyn\Pictures\images\download.jpg")
pred, pred_idx, probs = learn.predict(image_path)

print(f"Prediction: {pred}")
print(f"Prediction Index: {pred_idx}")
print(f"Probabilities: {probs[pred_idx]}")