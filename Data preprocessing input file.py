import nltk
import spacy
import re
import pandas as pd
nlp = spacy.load('en_core_web_sm')
def extract_names(txt):
    person_names = []
    for sent in nltk.sent_tokenize(txt):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label') and chunk.label() == 'PERSON':
                person_names.append(
                    ' '.join(chunk_leave[0] for chunk_leave in chunk.leaves())
                )
    return person_names[0]


PHONE_REG = re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
 
def extract_phone_number(resume_text):
    phone = re.findall(PHONE_REG, resume_text)
 
    if phone:
        number = ''.join(phone[0])
 
        if resume_text.find(number)  >= 0 and len(number) < 16:
            return number
    return None


EMAIL_REG = re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')
 
def extract_emails(resume_text):
    return re.findall(EMAIL_REG, resume_text)

db = pd.read_csv('finalskills.csv')['skills'].to_list()

def extract_skills(input_text):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(input_text)
    

    filtered_tokens = [w for w in word_tokens if w not in stop_words]

    filtered_tokens = [w for w in word_tokens if w.isalpha()]

    bigrams_trigrams = list(map(' '.join, nltk.everygrams(filtered_tokens, 2, 3)))
 

    found_skills = set()


    for token in filtered_tokens:
        if token.lower() in db:
            found_skills.add(token)
 
    for ngram in bigrams_trigrams:
        if ngram.lower() in db:
            found_skills.add(ngram)
    return found_skills


RESERVED_WORDS = [
    'school',
    'college',
    'university',
    'academy',
    'faculty',
    'degree',
    'institute',]
 
def extract_education(input_text):
    organizations = []
 

    for sent in nltk.sent_tokenize(input_text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label') and chunk.label() == 'ORGANIZATION':
                organizations.append(' '.join(c[0] for c in chunk.leaves()))
 
   
    education = set()
    for org in organizations:
        for word in RESERVED_WORDS:
            if org.lower().find(word) >= 0:
                education.add(org)
file_path = 'resall.csv'


df = pd.read_csv(file_path)

l=[]
for index, row in df.iterrows():
 
    resume_text = row['text']
    name = extract_names(resume_text)
    print(name)
    email = extract_emails(resume_text)
    print(email)
    phone = extract_phone_number(resume_text)
    print(phone)
    skills = extract_skills(resume_text)
   
    s=''
    for i in skills:
        s+=i+' '
    education = extract_education(resume_text)
    print(education)
    l.append([name,email,phone,s])
df=pd.DataFrame(l,columns=['name','email','phone','skills'])
df.to_csv('extract.csv')





