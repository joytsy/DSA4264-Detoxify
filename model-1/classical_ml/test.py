# Assuming 'detector.py' is in the same folder
from detector import Detector

detector = Detector()
prompt = "i love the weather"
prediction = detector.predict(prompt)
print(f"Predicted class: {prediction}")

# "today is a beautiful day" - No Hate/Toxic
# "i dont like everything around me" - Toxic 1
# "You're such a loser!" - Toxic 2
# "you are a hypocrite, the drama you cause is unbearable. i will destroy all your belonging." - Toxic 3
# "it is expected that immigrants are impatient" - Hate 1
# "Jews are the cause of everything!" - Hate 2
# "People like the LGBTQ+ are piece of thrash, if they dont leave immediately i will hit them with a bat" - Hate 3
