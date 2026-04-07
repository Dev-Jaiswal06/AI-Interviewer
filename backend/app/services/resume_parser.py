import io
import base64
import re

try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None


class ResumeParser:
    def __init__(self):
        self.skill_keywords = {
            'programming_languages': [
                'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'go', 'rust',
                'php', 'swift', 'kotlin', 'typescript', 'scala', 'r', 'matlab'
            ],
            'web_technologies': [
                'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express',
                'django', 'flask', 'spring', 'asp.net', 'ruby on rails'
            ],
            'databases': [
                'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
                'cassandra', 'oracle', 'sqlite', 'firebase'
            ],
            'tools': [
                'git', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'jenkins',
                'terraform', 'ansible', 'jira', 'confluence'
            ],
            'ml_ai': [
                'machine learning', 'deep learning', 'tensorflow', 'pytorch',
                'nlp', 'computer vision', 'scikit-learn', 'pandas', 'numpy',
                'opencv', 'keras', 'hugging face'
            ],
            'concepts': [
                'agile', 'scrum', 'devops', 'ci/cd', 'microservices', 'rest api',
                'graphql', 'oauth', 'jwt', 'docker', 'linux'
            ]
        }
    
    def extract_text_from_base64(self, base64_string):
        if not base64_string:
            return ""
        
        try:
            if ',' in base64_string:
                base64_string = base64_string.split(',')[1]
            
            pdf_bytes = base64.b64decode(base64_string)
            pdf_file = io.BytesIO(pdf_bytes)
            
            if PdfReader is None:
                return "PDF parsing not available. Install PyPDF2."
            
            reader = PdfReader(pdf_file)
            text = ""
            
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
            
        except Exception as e:
            return f"Error extracting PDF: {str(e)}"
    
    def extract_skills(self, text):
        if not text:
            return []
        
        text_lower = text.lower()
        found_skills = []
        
        for category, skills in self.skill_keywords.items():
            for skill in skills:
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, text_lower):
                    found_skills.append({
                        'skill': skill,
                        'category': category
                    })
        
        return found_skills
    
    def extract_experience(self, text):
        experience_patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience|exp)',
            r'(?:work|job|employment)\s*(?:experience)?:?\s*(\d+)\s*(?:years?|yrs?)',
        ]
        
        for pattern in experience_patterns:
            match = re.search(pattern, text.lower())
            if match:
                return int(match.group(1))
        
        return 0
    
    def extract_education(self, text):
        education_keywords = [
            'bachelor', 'master', 'phd', 'btech', 'mtech', 'bsc', 'msc',
            'engineering', 'computer science', 'information technology'
        ]
        
        text_lower = text.lower()
        education = []
        
        for keyword in education_keywords:
            if keyword in text_lower:
                education.append(keyword)
        
        return list(set(education))
    
    def extract_name(self, text):
        lines = text.split('\n')
        if lines:
            first_line = lines[0].strip()
            if len(first_line) < 50 and not any(char.isdigit() for char in first_line):
                return first_line
        return "Name not found"
    
    def extract_email(self, text):
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(email_pattern, text)
        return match.group(0) if match else None
    
    def extract_phone(self, text):
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        match = re.search(phone_pattern, text)
        return match.group(0) if match else None
    
    def parse_resume(self, base64_string):
        text = self.extract_text_from_base64(base64_string)
        
        return {
            'text': text,
            'name': self.extract_name(text),
            'email': self.extract_email(text),
            'phone': self.extract_phone(text),
            'skills': self.extract_skills(text),
            'experience_years': self.extract_experience(text),
            'education': self.extract_education(text)
        }
