import re
import math
from collections import Counter


class AnswerEvaluator:
    def __init__(self):
        self.stop_words = {
            'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'must', 'shall',
            'can', 'need', 'dare', 'ought', 'used', 'to', 'of', 'in',
            'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into',
            'through', 'during', 'before', 'after', 'above', 'below',
            'between', 'under', 'again', 'further', 'then', 'once',
            'here', 'there', 'when', 'where', 'why', 'how', 'all',
            'each', 'few', 'more', 'most', 'other', 'some', 'such',
            'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
            'too', 'very', 'just', 'and', 'but', 'if', 'or', 'because',
            'until', 'while', 'this', 'that', 'these', 'those', 'it'
        }
    
    def preprocess(self, text):
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        words = text.split()
        words = [w for w in words if w not in self.stop_words and len(w) > 2]
        return words
    
    def tf(self, words):
        total = len(words)
        if total == 0:
            return {}
        counter = Counter(words)
        return {word: count / total for word, count in counter.items()}
    
    def idf(self, corpus):
        num_docs = len(corpus)
        idf_dict = {}
        all_words = set(word for doc in corpus for word in doc)
        
        for word in all_words:
            doc_count = sum(1 for doc in corpus if word in doc)
            idf_dict[word] = math.log((num_docs + 1) / (doc_count + 1)) + 1
        
        return idf_dict
    
    def tfidf(self, words, idf_dict):
        tf_vec = self.tf(words)
        return {word: tf_val * idf_dict.get(word, 0) for word, tf_val in tf_vec.items()}
    
    def cosine_similarity(self, vec1, vec2):
        common_words = set(vec1.keys()) & set(vec2.keys())
        
        if not common_words:
            return 0.0
        
        dot_product = sum(vec1[word] * vec2[word] for word in common_words)
        
        mag1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
        mag2 = math.sqrt(sum(v ** 2 for v in vec2.values()))
        
        if mag1 == 0 or mag2 == 0:
            return 0.0
        
        return dot_product / (mag1 * mag2)
    
    def keyword_matching(self, user_answer, ideal_answer):
        user_words = set(self.preprocess(user_answer))
        ideal_words = set(self.preprocess(ideal_answer))
        
        if not ideal_words:
            return 0.0
        
        matches = len(user_words & ideal_words)
        return matches / len(ideal_words)
    
    def length_penalty(self, user_answer, ideal_answer):
        ideal_len = len(ideal_answer.split())
        user_len = len(user_answer.split())
        
        if user_len == 0:
            return 0.0
        
        ratio = user_len / ideal_len
        
        if ratio < 0.3:
            return ratio * 0.5
        elif ratio > 1.5:
            return 1.0 - (ratio - 1.0) * 0.3
        else:
            return 1.0
    
    def evaluate(self, user_answer, ideal_answer):
        user_words = self.preprocess(user_answer)
        ideal_words = self.preprocess(ideal_answer)
        
        if not ideal_words:
            return {
                'score': 50,
                'feedback': 'No ideal answer provided for comparison.',
                'similarity': 0,
                'keyword_match': 0,
                'completeness': 0
            }
        
        if not user_words:
            return {
                'score': 0,
                'feedback': 'No answer provided. Please provide an answer to get evaluated.',
                'similarity': 0,
                'keyword_match': 0,
                'completeness': 0
            }
        
        corpus = [user_words, ideal_words]
        idf_dict = self.idf(corpus)
        
        user_tfidf = self.tfidf(user_words, idf_dict)
        ideal_tfidf = self.tfidf(ideal_words, idf_dict)
        
        similarity = self.cosine_similarity(user_tfidf, ideal_tfidf)
        keyword_score = self.keyword_matching(user_answer, ideal_answer)
        completeness = self.length_penalty(user_answer, ideal_answer)
        
        final_score = (
            similarity * 40 +
            keyword_score * 35 +
            completeness * 25
        )
        
        final_score = max(0, min(100, final_score))
        
        feedback = self._generate_feedback(
            final_score,
            similarity,
            keyword_score,
            completeness
        )
        
        return {
            'score': round(final_score, 2),
            'feedback': feedback,
            'similarity': round(similarity * 100, 2),
            'keyword_match': round(keyword_score * 100, 2),
            'completeness': round(completeness * 100, 2),
            'strengths': self._identify_strengths(similarity, keyword_score, completeness),
            'improvements': self._suggest_improvements(similarity, keyword_score, completeness, ideal_words)
        }
    
    def _generate_feedback(self, score, similarity, keyword, completeness):
        if score >= 90:
            return "Excellent answer! You covered all key points with good detail and structure."
        elif score >= 75:
            return "Good answer! You addressed most key points well. Minor improvements possible."
        elif score >= 60:
            return "Average answer. You covered some key points but could add more depth and detail."
        elif score >= 40:
            return "Below average. Consider covering more key concepts and providing specific examples."
        else:
            return "Needs significant improvement. Review the topic and try to cover the essential points more thoroughly."
    
    def _identify_strengths(self, similarity, keyword, completeness):
        strengths = []
        
        if similarity >= 0.6:
            strengths.append("Good conceptual understanding")
        if keyword >= 0.5:
            strengths.append("Used relevant technical terms")
        if completeness >= 0.7:
            strengths.append("Provided comprehensive answer")
        
        return strengths if strengths else ["Attempted to answer the question"]
    
    def _suggest_improvements(self, similarity, keyword, completeness, ideal_words):
        improvements = []
        
        if similarity < 0.5:
            improvements.append("Focus more on the core concepts and definitions")
        if keyword < 0.4:
            missing = list(set(ideal_words) - set(self.preprocess('')))
            if missing:
                improvements.append(f"Consider including these terms: {', '.join(missing[:5])}")
        if completeness < 0.5:
            improvements.append("Provide more detailed explanations with examples")
        
        if not improvements:
            improvements.append("Try to add more specific examples from your experience")
        
        return improvements
