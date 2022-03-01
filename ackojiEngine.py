from flask import Flask
from flask import request
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)


@app.route("/ackoji_engine", methods=['GET'])
def ackoji_engine():
    # req = request.get_json()
    msg = request.args.get('msg')
    #msg = req['msg']
    print("\nLOG:", msg, "\n")
    return ackoji_engine_helper(msg)


# Counts the number of sentences in the string
def sentenceCount(msg):
    count = 0
    end = False
    sentence_end = {'?', '!', '.'}
    for c in msg:
        # flag to make sure we don't count repeat occurences as separate sentences, e.g. "??"
        if c in sentence_end:
            if not end:
                end = True
                count += 1
            continue
        end = False
    return count

# standard sentiment analyzer with VADER
def analyze_sentiment(mail_text):
    analyzer = SentimentIntensityAnalyzer()
    sentence = mail_text.lower()
    sent_dict = analyzer.polarity_scores(sentence)
    return sent_dict['compound']

# returns flag phrases from configurable file
def get_flag_phrases(filename):
    with open(filename) as f:
        lines = f.readlines()
    flag_phrases = []
    for line in lines:
        flag_phrases.append(line)
    return flag_phrases

# Logic
def ackoji_engine_helper(mail_text):
    CRITICAL_COMPOUND = -0.1
    mail_text = mail_text.lower()
    flag_phrases = get_flag_phrases('flag_phrases.txt')
    questionable = False

    # check the flag phrases
    for phrase in flag_phrases:
        if phrase in mail_text:
            questionable = True

    # check sentiment
    compound = analyze_sentiment(mail_text)
    #print(str(compound))
    if (compound < CRITICAL_COMPOUND):
        questionable = True

    # check sentence count
    num_sentences = sentenceCount(mail_text)
    if num_sentences > 3:
        questionable = True

    # return based on 'questionable'
    if questionable:
        return "Review"
    else:
        return "Acknowledgement"

if __name__ == '__main__':
    print("!!!RUNNING1!!!")
    # print(ackoji_engine_helper("I will be there."))
    app.run(host='0.0.0.0', port=105)
