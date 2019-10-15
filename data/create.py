import sys,os,json,re,random

f = open('dataset/train.json')
dtrain = json.loads(f.read())
f.close()

lines = []

random.seed(9911)

for idx,item in enumerate(dtrain):
    nnqt = item['NNQT_question']
    question = item['question']
    tokens = re.findall('\{.*?\}',nnqt)
    cleantokens = [re.sub('\W+',' ', token) for token in tokens]
    _tokensentence = ' '.join(cleantokens)
    tokensentence = re.sub(' +', ' ', _tokensentence)
    #perfect sentence pair
    lines.append((tokensentence,question,1.0))
    print((tokensentence,question,1.0))
    #less than perfect pairs
    s = ''
    for idx,chunk in enumerate(cleantokens):
        s += chunk
        lines.append((re.sub(' +', ' ', s),question,(idx+1)*1.0/float(len(cleantokens))))
        print((re.sub(' +', ' ', s),question,(idx+1)*1.0/float(len(cleantokens))))
    #0 match pair
    randidx = random.randint(0,len(dtrain))
    randnnqt = dtrain[randidx]['NNQT_question']
    randtokens = re.findall('\{.*?\}', randnnqt)
    if len(set(tokens) - (set(tokens) - set(randtokens))) == 0:
        cleanrandtokens = [re.sub('\W+',' ', token) for token in randtokens]
        _randtokensentence = ' '.join(cleanrandtokens)
        randtokensentence = re.sub(' +', ' ', _randtokensentence)
        lines.append((randtokensentence,question,0.0))
        print((randtokensentence,question,0.0))

f = open('lcq2train.tsv','w')
for line in lines:
    if None in line:
        continue
    f.write(line[0]+'\t'+line[1]+'\t'+str(line[2])+'\n')
f.close()
