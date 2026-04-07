from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Interview, CodingSession, PerformanceMetrics
from app.services.recommendation_engine import RecommendationEngine
from datetime import datetime, timedelta
import json

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/overview', methods=['GET'])
@jwt_required()
def get_overview():
    try:
        user_id = get_jwt_identity()
        
        total_interviews = Interview.query.filter_by(user_id=int(user_id)).count()
        completed_interviews = Interview.query.filter_by(
            user_id=int(user_id),
            status='completed'
        ).count()
        
        coding_sessions = CodingSession.query.filter_by(user_id=int(user_id)).count()
        avg_coding_score = db.session.query(
            db.func.avg(CodingSession.score)
        ).filter(CodingSession.user_id == int(user_id)).scalar() or 0
        
        interviews = Interview.query.filter_by(
            user_id=int(user_id),
            status='completed'
        ).all()
        
        avg_interview_score = 0
        if interviews:
            avg_interview_score = sum(i.overall_score for i in interviews) / len(interviews)
        
        return jsonify({
            'total_interviews': total_interviews,
            'completed_interviews': completed_interviews,
            'coding_sessions': coding_sessions,
            'avg_coding_score': round(avg_coding_score, 2),
            'avg_interview_score': round(avg_interview_score, 2),
            'readiness_score': calculate_readiness_score(
                completed_interviews,
                avg_interview_score,
                avg_coding_score
            )
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get overview: {str(e)}'}), 500


@dashboard_bp.route('/performance', methods=['GET'])
@jwt_required()
def get_performance():
    try:
        user_id = get_jwt_identity()
        
        interviews = Interview.query.filter_by(
            user_id=int(user_id),
            status='completed'
        ).order_by(Interview.completed_at.desc()).limit(10).all()
        
        performance_trend = []
        for interview in interviews:
            performance_trend.append({
                'date': interview.completed_at.isoformat() if interview.completed_at else None,
                'score': interview.overall_score,
                'type': interview.interview_type
            })
        
        technical_score = 0
        hr_score = 0
        technical_count = 0
        hr_count = 0
        
        for interview in interviews:
            if interview.interview_type == 'technical':
                technical_score += interview.overall_score
                technical_count += 1
            elif interview.interview_type == 'hr':
                hr_score += interview.overall_score
                hr_count += 1
        
        return jsonify({
            'performance_trend': performance_trend,
            'technical_avg': round(technical_score / technical_count, 2) if technical_count > 0 else 0,
            'hr_avg': round(hr_score / hr_count, 2) if hr_count > 0 else 0,
            'total_completed': len(interviews)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get performance: {str(e)}'}), 500


@dashboard_bp.route('/strengths', methods=['GET'])
@jwt_required()
def get_strengths():
    try:
        user_id = get_jwt_identity()
        
        interviews = Interview.query.filter_by(
            user_id=int(user_id),
            status='completed'
        ).all()
        
        strength_areas = {
            'technical': [],
            'communication': [],
            'problem_solving': [],
            'coding': []
        }
        
        for interview in interviews:
            scores = json.loads(interview.scores) if interview.scores else {}
            for q_id, score_data in scores.items():
                if score_data.get('score', 0) >= 80:
                    strength_areas['technical'].append({
                        'question_id': q_id,
                        'score': score_data.get('score', 0)
                    })
        
        coding_sessions = CodingSession.query.filter_by(
            user_id=int(user_id)
        ).filter(CodingSession.score >= 80).all()
        
        for session in coding_sessions:
            strength_areas['coding'].append({
                'problem_id': session.problem_id,
                'score': session.score
            })
        
        return jsonify({
            'strengths': {
                'technical': len(strength_areas['technical']),
                'communication': len(strength_areas['communication']),
                'problem_solving': len(strength_areas['problem_solving']),
                'coding': len(strength_areas['coding'])
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get strengths: {str(e)}'}), 500


@dashboard_bp.route('/weaknesses', methods=['GET'])
@jwt_required()
def get_weaknesses():
    try:
        user_id = get_jwt_identity()
        
        interviews = Interview.query.filter_by(
            user_id=int(user_id),
            status='completed'
        ).all()
        
        weak_areas = {
            'technical': [],
            'communication': [],
            'problem_solving': [],
            'coding': []
        }
        
        for interview in interviews:
            scores = json.loads(interview.scores) if interview.scores else {}
            for q_id, score_data in scores.items():
                if score_data.get('score', 0) < 50:
                    weak_areas['technical'].append({
                        'question_id': q_id,
                        'score': score_data.get('score', 0)
                    })
        
        coding_sessions = CodingSession.query.filter_by(
            user_id=int(user_id)
        ).filter(CodingSession.score < 50).all()
        
        for session in coding_sessions:
            weak_areas['coding'].append({
                'problem_id': session.problem_id,
                'score': session.score
            })
        
        return jsonify({
            'weak_areas': weak_areas
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get weaknesses: {str(e)}'}), 500


@dashboard_bp.route('/recommendations', methods=['GET'])
@jwt_required()
def get_recommendations():
    try:
        user_id = get_jwt_identity()
        
        engine = RecommendationEngine()
        recommendations = engine.get_recommendations(int(user_id))
        
        return jsonify({
            'recommendations': recommendations
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get recommendations: {str(e)}'}), 500


@dashboard_bp.route('/dashboard-data', methods=['GET'])
@jwt_required()
def get_dashboard_data():
    try:
        user_id = get_jwt_identity()
        
        interviews = Interview.query.filter_by(
            user_id=int(user_id),
            status='completed'
        ).all()
        
        coding_sessions = CodingSession.query.filter_by(
            user_id=int(user_id)
        ).all()
        
        strengths = []
        weaknesses = []
        
        interview_scores = []
        for interview in interviews:
            interview_scores.append(interview.overall_score)
            scores = json.loads(interview.scores) if interview.scores else {}
            
            for q_id, score_data in scores.items():
                if score_data.get('score', 0) >= 70:
                    strengths.append({
                        'area': 'Interview Answer',
                        'score': score_data.get('score', 0)
                    })
                elif score_data.get('score', 0) < 50:
                    weaknesses.append({
                        'area': 'Interview Answer',
                        'score': score_data.get('score', 0),
                        'question_id': q_id
                    })
        
        for session in coding_sessions:
            if session.score >= 70:
                strengths.append({
                    'area': 'Coding',
                    'problem': session.problem_id,
                    'score': session.score
                })
            elif session.score < 50:
                weaknesses.append({
                    'area': 'Coding',
                    'problem': session.problem_id,
                    'score': session.score
                })
        
        avg_score = sum(interview_scores) / len(interview_scores) if interview_scores else 0
        
        return jsonify({
            'overall_score': round(avg_score, 2),
            'total_interviews': len(interviews),
            'total_coding_sessions': len(coding_sessions),
            'strengths': strengths[:5],
            'weak_areas': weaknesses[:5],
            'readiness_level': get_readiness_level(avg_score),
            'recent_interviews': [i.to_dict() for i in interviews[-5:]]
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get dashboard data: {str(e)}'}), 500


def calculate_readiness_score(completed, interview_avg, coding_avg):
    if completed == 0:
        return 0
    
    readiness = (interview_avg * 0.6 + coding_avg * 0.4) * min(completed / 5, 1)
    return round(readiness, 2)


def get_readiness_level(score):
    if score >= 80:
        return 'Excellent'
    elif score >= 60:
        return 'Good'
    elif score >= 40:
        return 'Average'
    else:
        return 'Needs Improvement'
