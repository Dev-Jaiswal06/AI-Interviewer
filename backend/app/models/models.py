from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    interviews = db.relationship('Interview', backref='user', lazy=True, cascade='all, delete-orphan')
    coding_sessions = db.relationship('CodingSession', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'full_name': self.full_name,
            'phone': self.phone,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Interview(db.Model):
    __tablename__ = 'interviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    interview_type = db.Column(db.String(50), nullable=False)  # 'technical', 'hr', 'mixed'
    has_resume = db.Column(db.Boolean, default=False)
    resume_text = db.Column(db.Text)
    detected_skills = db.Column(db.Text)  # JSON string of skills
    questions = db.Column(db.Text)  # JSON string of questions
    answers = db.Column(db.Text)  # JSON string of user answers
    scores = db.Column(db.Text)  # JSON string of scores
    overall_score = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(50), default='in_progress')  # 'in_progress', 'completed'
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'interview_type': self.interview_type,
            'has_resume': self.has_resume,
            'overall_score': self.overall_score,
            'status': self.status,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }


class CodingSession(db.Model):
    __tablename__ = 'coding_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    problem_id = db.Column(db.Integer, db.ForeignKey('coding_problems.id'), nullable=False)
    language = db.Column(db.String(50), nullable=False)
    code = db.Column(db.Text)
    stdin = db.Column(db.Text)
    stdout = db.Column(db.Text)
    expected_output = db.Column(db.Text)
    actual_output = db.Column(db.Text)
    test_cases_passed = db.Column(db.Integer, default=0)
    total_test_cases = db.Column(db.Integer, default=0)
    execution_time = db.Column(db.Float)
    memory_used = db.Column(db.Float)
    score = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(50), default='pending')  # 'pending', 'running', 'completed', 'error'
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    problem = db.relationship('CodingProblem', backref='sessions')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'problem_id': self.problem_id,
            'language': self.language,
            'test_cases_passed': self.test_cases_passed,
            'total_test_cases': self.total_test_cases,
            'score': self.score,
            'status': self.status,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None
        }


class CodingProblem(db.Model):
    __tablename__ = 'coding_problems'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)  # 'easy', 'medium', 'hard'
    problem_type = db.Column(db.String(50))  # 'arrays', 'strings', 'trees', 'graphs', etc.
    starter_code = db.Column(db.Text)
    test_cases = db.Column(db.Text)  # JSON string of test cases
    solution = db.Column(db.Text)
    hints = db.Column(db.Text)
    points = db.Column(db.Integer, default=10)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'difficulty': self.difficulty,
            'problem_type': self.problem_type,
            'starter_code': self.starter_code,
            'hints': self.hints,
            'points': self.points
        }


class PerformanceMetrics(db.Model):
    __tablename__ = 'performance_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    metric_type = db.Column(db.String(50), nullable=False)  # 'technical', 'communication', 'coding', etc.
    score = db.Column(db.Float, default=0.0)
    max_score = db.Column(db.Float, default=100.0)
    percentage = db.Column(db.Float, default=0.0)
    details = db.Column(db.Text)  # JSON string with detailed metrics
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'metric_type': self.metric_type,
            'score': self.score,
            'max_score': self.max_score,
            'percentage': self.percentage,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class QuestionBank(db.Model):
    __tablename__ = 'question_bank'
    
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)  # 'technical', 'hr', 'behavioral'
    subcategory = db.Column(db.String(100))  # 'python', 'java', 'communication', etc.
    question_text = db.Column(db.Text, nullable=False)
    ideal_answer = db.Column(db.Text)
    keywords = db.Column(db.Text)  # JSON string of important keywords
    difficulty = db.Column(db.String(20), default='medium')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
            'subcategory': self.subcategory,
            'question_text': self.question_text,
            'ideal_answer': self.ideal_answer,
            'difficulty': self.difficulty
        }
