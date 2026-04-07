from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import CodingProblem, CodingSession
from app.services.judge0_service import Judge0Service
import json

coding_bp = Blueprint('coding', __name__)


@coding_bp.route('/problems', methods=['GET'])
@jwt_required()
def get_problems():
    try:
        difficulty = request.args.get('difficulty')
        problem_type = request.args.get('type')
        
        query = CodingProblem.query
        
        if difficulty:
            query = query.filter_by(difficulty=difficulty.lower())
        if problem_type:
            query = query.filter_by(problem_type=problem_type.lower())
        
        problems = query.all()
        
        return jsonify({
            'problems': [p.to_dict() for p in problems]
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get problems: {str(e)}'}), 500


@coding_bp.route('/problems/<int:problem_id>', methods=['GET'])
@jwt_required()
def get_problem(problem_id):
    try:
        problem = CodingProblem.query.get(problem_id)
        
        if not problem:
            return jsonify({'error': 'Problem not found'}), 404
        
        return jsonify({
            'problem': problem.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get problem: {str(e)}'}), 500


@coding_bp.route('/submit', methods=['POST'])
@jwt_required()
def submit_code():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        problem_id = data.get('problem_id')
        code = data.get('code', '')
        language = data.get('language', 'python')  # python, javascript, java, cpp
        
        problem = CodingProblem.query.get(problem_id)
        if not problem:
            return jsonify({'error': 'Problem not found'}), 404
        
        session = CodingSession(
            user_id=int(user_id),
            problem_id=problem_id,
            language=language,
            code=code,
            status='running'
        )
        db.session.add(session)
        db.session.commit()
        
        judge0 = Judge0Service()
        result = judge0.submit_code(code, language, problem)
        
        session.stdout = result.get('stdout', '')
        session.actual_output = result.get('actual_output', '')
        session.expected_output = result.get('expected_output', '')
        session.test_cases_passed = result.get('test_cases_passed', 0)
        session.total_test_cases = result.get('total_test_cases', 0)
        session.execution_time = result.get('execution_time', 0)
        session.memory_used = result.get('memory_used', 0)
        session.score = result.get('score', 0)
        session.status = result.get('status', 'completed')
        
        db.session.commit()
        
        return jsonify({
            'session_id': session.id,
            'result': result,
            'message': 'Code executed successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to submit code: {str(e)}'}), 500


@coding_bp.route('/sessions/<int:session_id>', methods=['GET'])
@jwt_required()
def get_session(session_id):
    try:
        user_id = get_jwt_identity()
        
        session = CodingSession.query.filter_by(
            id=session_id,
            user_id=int(user_id)
        ).first()
        
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        return jsonify({
            'session': session.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get session: {str(e)}'}), 500


@coding_bp.route('/sessions', methods=['GET'])
@jwt_required()
def get_user_sessions():
    try:
        user_id = get_jwt_identity()
        problem_id = request.args.get('problem_id', type=int)
        
        query = CodingSession.query.filter_by(user_id=int(user_id))
        
        if problem_id:
            query = query.filter_by(problem_id=problem_id)
        
        sessions = query.order_by(CodingSession.submitted_at.desc()).limit(50).all()
        
        return jsonify({
            'sessions': [s.to_dict() for s in sessions]
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get sessions: {str(e)}'}), 500


@coding_bp.route('/leaderboard', methods=['GET'])
@jwt_required()
def get_leaderboard():
    try:
        problem_id = request.args.get('problem_id', type=int)
        
        query = db.session.query(
            CodingSession.user_id,
            db.func.max(CodingSession.score).label('best_score'),
            db.func.count(CodingSession.id).label('attempts')
        ).group_by(CodingSession.user_id)
        
        if problem_id:
            query = query.filter(CodingSession.problem_id == problem_id)
        
        results = query.order_by(db.desc('best_score')).limit(20).all()
        
        leaderboard = []
        for r in results:
            user = db.session.get('User', r.user_id)
            leaderboard.append({
                'rank': len(leaderboard) + 1,
                'user_name': user.full_name if user else 'Anonymous',
                'best_score': r.best_score,
                'attempts': r.attempts
            })
        
        return jsonify({
            'leaderboard': leaderboard
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get leaderboard: {str(e)}'}), 500


@coding_bp.route('/test', methods=['POST'])
@jwt_required()
def test_code():
    try:
        data = request.get_json()
        
        code = data.get('code', '')
        language = data.get('language', 'python')
        stdin = data.get('stdin', '')
        
        judge0 = Judge0Service()
        result = judge0.run_code(code, language, stdin)
        
        return jsonify({
            'result': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to test code: {str(e)}'}), 500
