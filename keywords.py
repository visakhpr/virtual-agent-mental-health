import json

def extract_keywords(file_path):
    keywords = set()
    with open(file_path, 'r') as f:
        data = f.read()
        json_data = json.loads('[' + data.replace('}{', '},{') + ']')
        for obj in json_data:
            question = obj['Question']
            answer = obj['Answer']
            words = question.split() + answer.split()
            for word in words:
                if word.startswith('/'):
                    keywords.add(word)
                else:
                    word = word.strip(',.?!"\'()')
                    if word.isalpha() and len(word) > 2:
                        keywords.add(word.lower())
    return keywords

keywords = extract_keywords('/Users/visakhpr/Desktop/Rasa/github/cbs2/qa_json_files/visakh_1234567890.json')
print(keywords)

