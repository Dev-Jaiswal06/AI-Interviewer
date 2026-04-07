import json


class PerformanceAnalyzer:
    def __init__(self):
        self.thresholds = {
            'excellent': 80,
            'good': 60,
            'average': 40,
            'poor': 0
        }
    
    def analyze(self, interview):
        scores = json.loads(interview.scores) if interview.scores else {}
        questions = json.loads(interview.questions) if interview.questions else []
        answers = json.loads(interview.answers) if interview.answers else {}
        
        analysis = {
            'overall_score': interview.overall_score,
            'readiness_level': self._get_readiness_level(interview.overall_score),
            'section_scores': self._calculate_section_scores(scores, questions),
            'strengths': self._identify_strengths(scores),
            'weak_areas': self._identify_weak_areas(scores),
            'detailed_analysis': self._detailed_analysis(scores, questions, answers)
        }
        
        return analysis
    
    def _get_readiness_level(self, score):
        if score >= self.thresholds['excellent']:
            return 'Excellent'
        elif score >= self.thresholds['good']:
            return 'Good'
        elif score >= self.thresholds['average']:
            return 'Average'
        else:
            return 'Needs Improvement'
    
    def _calculate_section_scores(self, scores, questions):
        section_scores = {
            'technical': {'total': 0, 'count': 0, 'questions': []},
            'hr': {'total': 0, 'count': 0, 'questions': []},
            'problem_solving': {'total': 0, 'count': 0, 'questions': []}
        }
        
        for q_id, q_data in scores.items():
            q_score = q_data.get('score', 0)
            q_type = q_data.get('type', 'technical')
            
            if q_type in section_scores:
                section_scores[q_type]['total'] += q_score
                section_scores[q_type]['count'] += 1
                section_scores[q_type]['questions'].append({
                    'id': q_id,
                    'score': q_score
                })
        
        for section in section_scores:
            if section_scores[section]['count'] > 0:
                section_scores[section]['average'] = (
                    section_scores[section]['total'] / 
                    section_scores[section]['count']
                )
            else:
                section_scores[section]['average'] = 0
        
        return section_scores
    
    def _identify_strengths(self, scores):
        strengths = []
        
        for q_id, q_data in scores.items():
            if q_data.get('score', 0) >= 75:
                strengths.append({
                    'question_id': q_id,
                    'score': q_data.get('score', 0),
                    'similarity': q_data.get('similarity', 0)
                })
        
        strengths.sort(key=lambda x: x['score'], reverse=True)
        return strengths[:5]
    
    def _identify_weak_areas(self, scores):
        weak_areas = []
        
        for q_id, q_data in scores.items():
            if q_data.get('score', 0) < 50:
                weak_areas.append({
                    'question_id': q_id,
                    'score': q_data.get('score', 0),
                    'feedback': q_data.get('feedback', 'Needs improvement')
                })
        
        weak_areas.sort(key=lambda x: x['score'])
        return weak_areas[:5]
    
    def _detailed_analysis(self, scores, questions, answers):
        analysis = []
        
        for q in questions:
            q_id = str(q['id'])
            q_data = scores.get(q_id, {})
            
            if q_data:
                analysis.append({
                    'question': q.get('question_text', ''),
                    'your_answer': answers.get(q_id, {}).get('answer', 'Not answered'),
                    'ideal_answer': q.get('ideal_answer', ''),
                    'score': q_data.get('score', 0),
                    'feedback': q_data.get('feedback', ''),
                    'strengths': q_data.get('strengths', []),
                    'improvements': q_data.get('improvements', [])
                })
        
        return analysis
    
    def generate_summary(self, analysis):
        summary = {
            'overall': analysis['readiness_level'],
            'key_strengths': [],
            'areas_to_improve': [],
            'next_steps': []
        }
        
        for section, data in analysis['section_scores'].items():
            if data.get('average', 0) >= 70:
                summary['key_strengths'].append(
                    f"Good performance in {section.replace('_', ' ')}"
                )
            elif data.get('average', 0) < 50:
                summary['areas_to_improve'].append(
                    f"Need to focus on {section.replace('_', ' ')}"
                )
        
        if analysis['overall_score'] < 60:
            summary['next_steps'].append("Practice more interview questions")
            summary['next_steps'].append("Review fundamental concepts")
        
        if analysis['weak_areas']:
            summary['next_steps'].append(
                "Focus on topics where you scored below 50%"
            )
        
        return summary
