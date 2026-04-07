from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Interview, QuestionBank, CodingProblem
from app.services.resume_parser import ResumeParser
from app.services.question_generator import QuestionGenerator
import json
from datetime import datetime

interview_bp = Blueprint('interview', __name__)


@interview_bp.route('/start', methods=['POST'])
@jwt_required()
def start_interview():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        interview_type = data.get('interview_type', 'mixed')  # 'technical', 'hr', 'mixed'
        has_resume = data.get('has_resume', False)
        resume_file = data.get('resume_file')  # Base64 encoded PDF
        
        interview = Interview(
            user_id=int(user_id),
            interview_type=interview_type,
            has_resume=has_resume,
            status='in_progress'
        )
        
        if has_resume and resume_file:
            parser = ResumeParser()
            resume_text = parser.extract_text_from_base64(resume_file)
            interview.resume_text = resume_text
            
            skills = parser.extract_skills(resume_text)
            interview.detected_skills = json.dumps(skills)
        
        db.session.add(interview)
        db.session.commit()
        
        generator = QuestionGenerator()
        
        if has_resume and interview.detected_skills:
            skills = json.loads(interview.detected_skills)
            questions = generator.generate_skill_based_questions(skills, interview_type)
        else:
            questions = generator.generate_general_questions(interview_type)
        
        interview.questions = json.dumps(questions)
        db.session.commit()
        
        return jsonify({
            'interview_id': interview.id,
            'questions': questions,
            'message': 'Interview started successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to start interview: {str(e)}'}), 500


@interview_bp.route('/submit-answer', methods=['POST'])
@jwt_required()
def submit_answer():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        interview_id = data.get('interview_id')
        question_id = data.get('question_id')
        answer = data.get('answer', '')
        question_type = data.get('question_type', 'technical')  # 'technical', 'hr'
        
        interview = Interview.query.filter_by(
            id=interview_id,
            user_id=int(user_id)
        ).first()
        
        if not interview:
            return jsonify({'error': 'Interview not found'}), 404
        
        answers = json.loads(interview.answers) if interview.answers else {}
        answers[str(question_id)] = {
            'answer': answer,
            'question_type': question_type,
            'submitted_at': datetime.utcnow().isoformat()
        }
        interview.answers = json.dumps(answers)
        db.session.commit()
        
        return jsonify({
            'message': 'Answer submitted successfully',
            'question_id': question_id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to submit answer: {str(e)}'}), 500


@interview_bp.route('/complete', methods=['POST'])
@jwt_required()
def complete_interview():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        interview_id = data.get('interview_id')
        
        interview = Interview.query.filter_by(
            id=interview_id,
            user_id=int(user_id)
        ).first()
        
        if not interview:
            return jsonify({'error': 'Interview not found'}), 404
        
        interview.status = 'completed'
        interview.completed_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Interview completed successfully',
            'interview_id': interview_id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to complete interview: {str(e)}'}), 500


@interview_bp.route('/history', methods=['GET'])
@jwt_required()
def get_interview_history():
    try:
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        interviews = Interview.query.filter_by(
            user_id=int(user_id)
        ).order_by(Interview.started_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'interviews': [i.to_dict() for i in interviews.items],
            'total': interviews.total,
            'page': interviews.page,
            'pages': interviews.pages
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get history: {str(e)}'}), 500


@interview_bp.route('/<int:interview_id>', methods=['GET'])
@jwt_required()
def get_interview(interview_id):
    try:
        user_id = get_jwt_identity()
        
        interview = Interview.query.filter_by(
            id=interview_id,
            user_id=int(user_id)
        ).first()
        
        if not interview:
            return jsonify({'error': 'Interview not found'}), 404
        
        return jsonify({
            'interview': interview.to_dict(),
            'questions': json.loads(interview.questions) if interview.questions else [],
            'answers': json.loads(interview.answers) if interview.answers else {},
            'scores': json.loads(interview.scores) if interview.scores else {}
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get interview: {str(e)}'}), 500


@interview_bp.route('/questions/all', methods=['GET'])
@jwt_required()
def get_all_questions():
    try:
        category = request.args.get('category')
        
        query = QuestionBank.query
        if category:
            query = query.filter_by(category=category)
        
        questions = query.all()
        
        return jsonify({
            'questions': [q.to_dict() for q in questions]
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get questions: {str(e)}'}), 500


@interview_bp.route('/practice-questions', methods=['GET'])
@jwt_required()
def get_practice_questions():
    try:
        category = request.args.get('category', 'technical')
        difficulty = request.args.get('difficulty', 'medium')
        limit = request.args.get('limit', 10, type=int)
        
        questions = QuestionBank.query.filter_by(
            category=category,
            difficulty=difficulty
        ).limit(limit).all()
        
        if not questions:
            questions = QuestionBank.query.filter_by(
                category=category
            ).limit(limit).all()
        
        return jsonify({
            'questions': [q.to_dict() for q in questions]
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get practice questions: {str(e)}'}), 500
