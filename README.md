# Emotion Detector

Type in a sentence and this app tells you what emotions are hiding in it. It then explains the result in plain English and can even read that explanation out loud to you.

I built it with Python, TensorFlow and Streamlit, and trained it on Google's GoEmotions dataset.

---

## What it does

You paste in some text, press **Run Analysis**, and you get:

- The main emotion in your text, along with how sure the model is about it
- A short, easy-to-read summary of what that emotion means
- The overall tone of the message
- A few smaller emotions that might be sitting underneath the main one
- An audio version of the description, spoken in an Australian accent

A single sentence can carry more than one feeling at once, like being proud and thankful together. The app is built to pick up on that instead of forcing every message into one box.

---

## How it works

The app is split into a few simple parts:

1. **The screen (`UI/App.py`)**: This is what you see in the browser. It has a bold, blocky look with thick borders and bright yellow and red colours, and it works in both light and dark mode.
2. **The brain (`workflow.py`)**: It takes your text, turns it into numbers the model understands, and asks the trained model which emotions it can find.
3. **The explainer (`Report.py`)**: It turns the model's raw numbers into a friendly report card with a summary, a tone and a short description.
4. **The voice (`speech.py`)**: It uses Google's text-to-speech to read the description aloud.

---

## About the model

- **Data:** About 43,000 Reddit comments from Google's GoEmotions dataset, each labelled with one or more of 28 emotions. After removing duplicates, 43,227 unique examples were left to learn from.
- **Model:** A neural network that reads a sentence from both directions, front to back and back to front, so it understands the context around each word.
- **Handling uneven data:** Some emotions (like neutral or joy) show up far more often than others. To keep the model from ignoring the rare ones, I gave the rare emotions more weight while training.
- **Smarter cut-offs:** Normally a model says "yes, this emotion is present" when it is at least 50% sure. That didn't work well here, so I found a separate best cut-off for each emotion. This raised the F1 score from about 0.33 to **0.5143**, and the precision reached **0.4537**.

These scores are modest, and that is expected. Emotions in text are subjective, and even humans often disagree about them.

---

## Project layout

```
Sentimental Analysis/
├── Model/
│   ├── bigru_goemotions_model.keras    # the trained model
│   └── model_artifacts.pkl             # word dictionary, emotion names, cut-offs
├── UI/
│   └── App.py                          # the Streamlit app and its styling
├── workflow.py                         # loads the model and makes predictions
├── Report.py                           # builds the report card
├── speech.py                           # text to audio
└── requirements.txt                    # libraries needed
```

---

## Getting started

1. Clone the repository:
   ```
   git clone https://github.com/241980094-Umair/Sentimental-Analysis.git
   cd Sentimental-Analysis
   ```

2. Install the libraries:
   ```
   pip install -r requirements.txt
   ```

3. Check the file paths. In `workflow.py`, the model paths are currently set to a folder on my own computer (`D:\Sentimental Analysis\Model\...`). Change them to wherever the `Model` folder is on your machine.

4. Start the app:
   ```
   streamlit run UI/App.py
   ```

5. Your browser will open the app. Type something, press the button, and see what comes back.

Note that the audio feature needs an internet connection, since it relies on Google's speech service.

---

## Things to know

- The report cards only have hand-written explanations for a handful of emotions: pride, joy, admiration, gratitude, neutral and relief. Anything else gets a general, more neutral description.
- The model works best on short, casual English text, similar to what you'd find in Reddit comments.
- It can get things wrong. Sarcasm and jokes are especially tricky.

---

## Ideas for the future

- Write explanations for all 28 emotions
- Let people choose different voices and accents
- Add a chart showing every emotion's score
- Make the file paths work on any computer automatically

---

## Credits

- [GoEmotions dataset](https://github.com/google-research/google-research/tree/master/goemotions) by Google Research
- Built with TensorFlow, Streamlit and gTTS
