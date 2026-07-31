#المشروع النهائي  
import re  
from collections import deque
from camel_tools.utils.dediac import dediac_ar 
from camel_tools.disambig.mle import MLEDisambiguator
#MLEDisambiguator وظيفتها ازالة الغموض الصرفي  
 

class ArabicNLPipeline: 
    def __init__(self, scheme="atbtok", split=True):
        self._scheme = scheme
        self._split = split
        #عشان امن المستخم يبث فيا من برا 
        
        self._mle = MLEDisambiguator.pretrained() 
        
        # هاي الميثود عرفتها هون عشان اسرع شغل هاي الدالة تبعتي 
        self._remove_pluses_regex = re.compile(r'(_\+|\+_)+')
        
        #جهزت القاموس الي رح اشتغل عليه 
        self._diac_type = {
            'atbtok': self._default_dediac,
            'bwtok': self._bwtok_dediac
        }
    
    #ازالة التشكيل 
    def _default_dediac(self, tok):
        return dediac_ar(tok) 

    def _bwtok_dediac(self, tok): 
        # تصحيح 3: إزالة الأقواس الزائدة حول المدخلات لتصبح دالة sub صحيحة
        return self._remove_pluses_regex.sub(r'\g<1>', dediac_ar(tok).strip("+_")) 
    
    #Noise Removel 
    def _remove_noise(self, text): 
        #URLs
        text = re.sub(r'http\S+|www\S+', '', text) 
        
        #ارقام واحرف عربيه شيل 
        text = re.sub(r'[a-zA-Z0-9]', '', text)
        
        #هون رموز غريبه         
        text = re.sub(r'[^\w\s\u0600-\u06FF]', ' ', text)        
        
        #مسافات         
        text = re.sub(r'\s+', ' ', text).strip()
        #هون حطيت strip عشان اشيل المسافات من بداية ونهايه النص  
        return text  

    #normalize 
    def _normalize(self, text): 
        text = re.sub(r'[أإآ]', 'ا', text)
        
        text = re.sub(r'ـ', '', text) 
        
        text = re.sub(r'ة', 'ه', text)
        return text 

    def _simple_tokenize(self, text): 
        #كوني فوق انا شايل الشغلات الزايده هون بقدر اقسم ع المسافات 
        return text.split() 
    
    def _morphological_process(self, words):  
        disambig_words = self._mle.disambiguate(words) 
        
        result = deque() 
        
        for disambig_word in disambig_words:
            scored_analyses = disambig_word.analyses
            
            if len(scored_analyses) > 0:
                analysis = scored_analyses[0].analysis
                tok = analysis.get(self._scheme, None)
                
                if tok is None or tok == 'NOAN':
                    tok = disambig_word.word
                    result.append(self._diac_type[self._scheme](tok))

                elif self._split:
                    tok = self._diac_type[self._scheme](tok)
                    result.extend(tok.split("_"))
                
                else:
                    clean_tok = self._diac_type[self._scheme](tok)
                    result.append(clean_tok)
            else: 
                result.append(disambig_word.word)
                
        return list(result)
    
    def process(self, raw_text): 
        if not raw_text or not isinstance(raw_text, str): 
            return [] 
        
        cleand_text = self._remove_noise(raw_text)
        
        normalized_text = self._normalize(cleand_text)
        
        word_list = self._simple_tokenize(normalized_text)
        
        final_tokens = self._morphological_process(word_list) 
        
        return final_tokens  
    
        
if __name__ == "__main__": 
    my_pipeline = ArabicNLPipeline(scheme='atbtok', split=True) 
    
    dirty_text = "مرحـــبـــاً! وسيلعبون بسياراتهم 🚙 غداً في شارع 99... https://test.com"
    print(dirty_text)
    
    final_result = my_pipeline.process(dirty_text) 
    
    print(final_result)