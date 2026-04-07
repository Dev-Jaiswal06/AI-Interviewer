from app.models import Interview, CodingSession, CodingProblem
from app import db
import json


class RecommendationEngine:
    def __init__(self):
        self.recommendations = []
    
    def get_recommendations(self, user_id):
        interviews = Interview.query.filter_by(
            user_id=user_id,
            status='completed'
        ).all()
        
        coding_sessions = CodingSession.query.filter_by(
            user_id=user_id
        ).all()
        
        recommendations = []
        
        recommendations.extend(self._interview_recommendations(interviews))
        recommendations.extend(self._coding_recommendations(coding_sessions))
        recommendations.extend(self._general_recommendations(interviews, coding_sessions))
        
        recommendations.sort(key=lambda x: x['priority'], reverse=True)
        
        return recommendations[:10]
    
    def _interview_recommendations(self, interviews):
        recs = []
        
        if not interviews:
            recs.append({
                'type': 'interview',
                'title': 'Start Your First Mock Interview',
                'description': 'Take a mock interview to assess your current skills and get personalized feedback.',
                'priority': 10,
                'action': 'start_interview'
            })
            return recs
        
        total_score = sum(i.overall_score for i in interviews) / len(interviews)
        
        if total_score < 50:
            recs.append({
                'type': 'interview',
                'title': 'Focus on Technical Fundamentals',
                'description': 'Your technical answers need improvement. Review basic programming concepts and data structures.',
                'priority': 9,
                'action': 'practice_technical'
            })
        
        if total_score < 70:
            recs.append({
                'type': 'interview',
                'title': 'Improve Answer Structure',
                'description': 'Use the STAR method for behavioral questions. Structure technical answers with examples.',
                'priority': 7,
                'action': 'review_star_method'
            })
        
        scores_by_type = {}
        for interview in interviews:
            itype = interview.interview_type
            if itype not in scores_by_type:
                scores_by_type[itype] = []
            scores_by_type[itype].append(interview.overall_score)
        
        for itype, scores in scores_by_type.items():
            avg = sum(scores) / len(scores)
            if avg < 60:
                recs.append({
                    'type': 'interview',
                    'title': f'Practice More {itype.title()} Questions',
                    'description': f'Your {itype} interview score is {avg:.1f}%. Focus on improving this area.',
                    'priority': 8,
                    'action': f'practice_{itype}'
                })
        
        return recs
    
    def _coding_recommendations(self, sessions):
        recs = []
        
        if not sessions:
            recs.append({
                'type': 'coding',
                'title': 'Start Coding Practice',
                'description': 'Practice coding problems to improve your problem-solving skills.',
                'priority': 10,
                'action': 'start_coding'
            })
            return recs
        
        avg_score = sum(s.score for s in sessions) / len(sessions) if sessions else 0
        
        failed_sessions = [s for s in sessions if s.score < 50]
        if failed_sessions:
            recs.append({
                'type': 'coding',
                'title': 'Review Failed Problems',
                'description': f'You have {len(failed_sessions)} problems with low scores. Review solutions and try again.',
                'priority': 9,
                'action': 'review_problems'
            })
        
        problem_scores = {}
        for session in sessions:
            pid = session.problem_id
            if pid not in problem_scores:
                problem_scores[pid] = []
            problem_scores[pid].append(session.score)
        
        for pid, scores in problem_scores.items():
            avg = sum(scores) / len(scores)
            if avg < 50 and len(scores) >= 2:
                problem = CodingProblem.query.get(pid)
                if problem:
                    recs.append({
                        'type': 'coding',
                        'title': f'Revisit: {problem.title}',
                        'description': f'You have attempted this {len(scores)} times with average score {avg:.1f}%. Review the concepts.',
                        'priority': 8,
                        'action': f'practice_problem_{pid}'
                    })
        
        if avg_score >= 70:
            recs.append({
                'type': 'coding',
                'title': 'Challenge Yourself',
                'description': 'Your coding skills are good! Try harder problems to further improve.',
                'priority': 6,
                'action': 'increase_difficulty'
            })
        
        return recs
    
    def _general_recommendations(self, interviews, sessions):
        recs = []
        
        if len(interviews) < 3 and len(sessions) < 5:
            recs.append({
                'type': 'general',
                'title': 'Consistency is Key',
                'description': 'Practice regularly. Try to complete at least 2-3 interviews and 10 coding problems per week.',
                'priority': 7,
                'action': 'create_schedule'
            })
        
        total_practice = len(interviews) + len(sessions)
        if total_practice >= 10:
            avg_score = 0
            if interviews:
                avg_score += sum(i.overall_score for i in interviews) / len(interviews)
            if sessions:
                avg_score += sum(s.score for s in sessions) / len(sessions)
            
            if avg_score >= 75:
                recs.append({
                    'type': 'general',
                    'title': 'Ready for Real Interviews',
                    'description': 'Your practice scores are good. Start applying to real companies!',
                    'priority': 5,
                    'action': 'apply_jobs'
                })
        
        recs.append({
            'type': 'general',
            'title': 'Focus on Communication',
            'description': 'While technical skills matter, clear communication during interviews is equally important.',
            'priority': 6,
            'action': 'improve_communication'
        })
        
        return recs
    
    def get_personalized_plan(self, user_id):
        recommendations = self.get_recommendations(user_id)
        
        plan = {
            'week_1': [],
            'week_2': [],
            'week_3': [],
            'week_4': []
        }
        
        priority_recs = [r for r in recommendations if r['priority'] >= 8]
        
        for i, rec in enumerate(priority_recs[:4]):
            week_key = f'week_{(i % 4) + 1}'
            plan[week_key].append(rec)
        
        if len(plan['week_1']) == 0:
            plan['week_1'].append({
                'type': 'general',
                'title': 'Assessment Week',
                'description': 'Complete initial assessments to establish baseline.',
                'action': 'take_assessment'
            })
        
        return plan
