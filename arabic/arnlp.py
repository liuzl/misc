import stanza
stanza.download('ar')
nlp = stanza.Pipeline(lang='ar')

import gensim
import re
import numpy as np
from nltk import ngrams
from util import *

model = gensim.models.Word2Vec.load('models/full_grams_cbow_100_wiki.mdl')

def cut(text, sentence=False):
    doc = nlp(text)
    ret = []
    for i, s in enumerate(doc.sentences):
        if sentence:
            ret.extend([{'sid':i+1,'id':w.id,'text':w.text,'lemma':w.lemma,'pos':w.upos} for w in s.words])
        else:
            ret.extend([{'text':w.text,'lemma':w.lemma,'pos':w.upos} for w in s.words])
    return ret

def ner(text, sentence=False):
    doc = nlp(text)
    ret = []
    for i, s in enumerate(doc.sentences):
        if sentence:
            ret.extend([{'sid':i+1,'text':e.text,'type':e.type,'start_char':e.start_char,'end_char':e.end_char} for e in s.ents])
        else:
            ret.extend([{'text':e.text,'type':e.type,'start_char':e.start_char,'end_char':e.end_char} for e in s.ents])
    return ret

def find_similar(word, topn=10):
    token = clean_str(word).replace(" ", "_")
    if token not in model.wv:
        return None
    return model.most_similar(token, topn=topn)

if __name__ == "__main__":
    text = '''شهدت نهاية الستينيات من القرن الماضي تكاتف كل من معهد ماساتشوستس للتقنية, شركة إيه تي أند تي (مختبرات بيل)، وشركة جنرال إلكتريك للعمل على نظام تشغيل تجريبي أُطلق عليه اسم مولتكس. كان يفترض بالنظام مولتكس أن يكون تفاعلياً ومتجاوباً مع مستخدمي النظام ناهيك عن الضرورة الأمنية للنظام من محاولات اختراق الملفات السرية التي يقوم بحفظها في مستودع الحفظ. رأى المشروع النور على شكل نظام تشغيل قابل للتطبيق إلا أن النظام أظهر أداءً '''
    print(cut(text))
    print(ner(text))
    print(find_similar('ﺎﺑﻭ ﺕﺮﻴﻜﻫ'))
