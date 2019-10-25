from flask import Flask,request,jsonify
app = Flask(__name__)

@app.route('/',methods=['GET','POST']) # decorator
def summarizer():
    
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize,sent_tokenize
    from nltk.stem.snowball import SnowballStemmer
    import nltk
    import requests
    import json
    #text=request.json.get('text')   
    #text = request.get_json('text')
    text=request.json.get('text')
    #text=str(input('Give your input here: \n'))
   
    stemmer = SnowballStemmer("english")
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text)

    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        word = stemmer.stem(word)
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    sentences = sent_tokenize(text)
    sentenceValue = dict()

    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq
    '''for sent,val in sentenceValue.items():
        print(sent,"\n value is ",val,'\n')'''

    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]

    # Average value of a sentence from original text
    average = int(sumValues / len(sentenceValue))

    
    summary = 'Summary: '
    for sentence in sentences:
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)):
            summary += " " + sentence

    from heapq import nlargest
    top10sent=nlargest(10,sentenceValue,key=sentenceValue.get)
    n=0
    top10=[]
    for topsent in top10sent:
        n+=1
        print('\n Top Statement number ',n,'\n','~*~*'*6,'\n\n',topsent,'\n','---'*20,'\n')
         
    return jsonify(summary)
   
    #return jsonify({'summ':summary})
    #return jsonify('summ':request.json.get(summary))   

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, use_reloader=False)# we may also add port number here " port='' "
    #app.run()

'''
print(request.json.get('title'))
return jsonify({'task': request.json.get('title')})
        '''    
'''
import requests
url = 'http://127.0.0.1:5000/'
r = requests.post(url,json={'text':text_data})
print(r.json())'''
