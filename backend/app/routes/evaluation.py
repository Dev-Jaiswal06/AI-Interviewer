from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Interview, PerformanceMetrics
from app.services.answer_evaluator import AnswerEvaluator
from app.services.performance_analyzer import PerformanceAnalyzer
import json

evaluation_bp = Blueprint('evaluation', __name__)


@evaluation_bp.route('/answer', methods=['POST'])
@jwt_required()
def evaluate_answer():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        interview_id = data.get('interview_id')
        question_id = data.get('question_id')
        user_answer = data.get('answer', '')
        
        interview = Interview.query.filter_by(
            id=interview_id,
            user_id=int(user_id)
        ).first()
        
        if not interview:
            return jsonify({'error': 'Interview not found'}), 404
        
        questions = json.loads(interview.questions) if interview.questions else []
        answers = json.loads(interview.answers) if interview.answers else {}
        
        ideal_answer = ''
        for q in questions:
            if str(q['id']) == str(question_id):
                ideal_answer = q.get('ideal_answer', '')
                break
        
        evaluator = AnswerEvaluator()
        evaluation = evaluator.evaluate(user_answer, ideal_answer)
        
        scores = json.loads(interview.scores) if interview.scores else {}
        scores[str(question_id)] = evaluation
        interview.scores = json.dumps(scores)
        
        interview.overall_score = sum(
            s.get('score', 0) for s in scores.values()
        ) / len(scores) if scores else 0
        
        db.session.commit()
        
        return jsonify({
            'question_id': question_id,
            'evaluation': evaluation,
            'overall_score': interview.overall_score
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to evaluate answer: {str(e)}'}), 500


@evaluation_bp.route('/interview/<int:interview_id>', methods=['POST'])
@jwt_required()
def evaluate_interview(interview_id):
    try:
        user_id = get_jwt_identity()
        
        interview = Interview.query.filter_by(
            id=interview_id,
            user_id=int(user_id)
        ).first()
        
        if not interview:
            return jsonify({'error': 'Interview not found'}), 404
        
        questions = json.loads(interview.questions) if interview.questions else []
        answers = json.loads(interview.answers) if interview.answers else {}
        
        evaluator = AnswerEvaluator()
        scores = {}
        total_score = 0
        
        for q in questions:
            q_id = str(q['id'])
            user_ans = answers.get(q_id, {}).get('answer', '')
            ideal_ans = q.get('ideal_answer', '')
            
            evaluation = evaluator.evaluate(user_ans, ideal_ans)
            scores[q_id] = evaluation
            total_score += evaluation.get('score', 0)
        
        interview.scores = json.dumps(scores)
        interview.overall_score = total_score / len(questions) if questions else 0
        interview.status = 'completed'
        
        db.session.commit()
        
        return jsonify({
            'interview_id': interview_id,
            'scores': scores,
            'overall_score': interview.overall_score
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to evaluate interview: {str(e)}'}), 500


@evaluation_bp.route('/analysis/<int:interview_id>', methods=['GET'])
@jwt_required()
def get_analysis(interview_id):
    try:
        user_id = get_jwt_identity()
        
        interview = Interview.query.filter_by(
            id=interview_id,
            user_id=int(user_id)
        ).first()
        
        if not interview:
            return jsonify({'error': 'Interview not found'}), 404
        
        analyzer = PerformanceAnalyzer()
        analysis = analyzer.analyze(interview)
        
        return jsonify({
            'analysis': analysis
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to analyze: {str(e)}'}), 500


@evaluation_bp.route('/metrics', methods=['GET'])
@jwt_required()
def get_metrics():
    try:
        user_id = get_jwt_identity()
        
        metrics = PerformanceMetrics.query.filter_by(
            user_id=int(user_id)
        ).order_by(PerformanceMetrics.created_at.desc()).all()
        
        return jsonify({
            'metrics': [m.to_dict() for m in metrics]
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get metrics: {str(e)}'}), 500
