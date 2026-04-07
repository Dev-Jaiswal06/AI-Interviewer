import random
import uuid


class QuestionGenerator:
    def __init__(self):
        self.question_bank = self._load_question_bank()
    
    def _load_question_bank(self):
        return {
            'technical': {
                'python': [
                    {
                        'id': str(uuid.uuid4()),
                        'question': 'Explain the difference between a list and a tuple in Python.',
                        'ideal_answer': 'Lists are mutable (can be modified after creation) while tuples are immutable. Lists use more memory and have more built-in methods. Tuples are faster and can be used as dictionary keys.',
                        'keywords': ['mutable', 'immutable', 'list', 'tuple', 'memory', 'methods']
                    },
                    {
                        'id': str(uuid.uuid4()),
                        'question': 'What is a decorator in Python and how would you create one?',
                        'ideal_answer': 'A decorator is a function that takes another function as input and extends its behavior without explicitly modifying it. Created using @decorator_name syntax above the function definition.',
                        'keywords': ['function', 'wrapper', '@', 'syntax', 'behavior']
                    },
                    {
                        'id': str(uuid.uuid4()),
                        'question': 'Explain Python garbage collection.',
                        'ideal_answer': 'Python uses reference counting and a cyclic garbage collector. Reference counting tracks object references and automatically deletes objects with zero references. The cyclic GC detects and cleans up reference cycles.',
                        'keywords': ['reference counting', 'garbage collector', 'memory', 'cycles', 'automatic']
                    },
                    {
                        'id': str(uuid.uuid4()),
                        'question': 'What are Python metaclasses?',
                        'ideal_answer': 'Metaclasses are classes whose instances are classes. They control class creation and behavior. The default metaclass is type. Use __metaclass__ attribute or metaclass= keyword to specify.',
                        'keywords': ['class', 'type', '__metaclass__', 'creation', 'control']
                    },
                    {
                        'id': str(uuid.uuid4()),
                        'question': 'Explain Python GIL (Global Interpreter Lock).',
                        'ideal_answer': 'GIL is a mutex that protects access to Python objects, preventing multiple threads from executing Python bytecode simultaneously. This means CPU-bound programs dont benefit from multithreading in Python.',
                        'keywords': ['mutex', 'thread', 'cpu', 'multithreading', 'bytecode']
                    }
                ],
                'java': [
                    {
                        'id': str(uuid.uuid4()),
                        'question': 'What is the difference between JDK, JRE, and JVM?',
                        'ideal_answer': 'JVM executes bytecode. JRE provides runtime environment including JVM and libraries. JDK includes JRE plus development tools like compiler and debugger.',
                        'keywords': ['jvm', 'jre', 'jdk', 'bytecode', 'runtime', 'compiler']
                    },
                    {
                        'id': str(uuid.uuid4()),
                        'question': 'Explain the concept of multithreading in Java.',
                        'ideal_answer': 'Multithreading allows concurrent execution of two or more threads. Created using Thread class or Runnable interface. Synchronization is needed to prevent race conditions using synchronized keyword or locks.',
                        'keywords': ['thread', 'concurrent', 'synchronized', 'runnable', 'race condition']
                    },
                    {
                        'id': str(uuid.uuid4()),
                        'question': 'What is the difference between ArrayList and LinkedList?',
                        'ideal_answer': 'ArrayList uses dynamic array, provides fast random access O(1) but slow insertion/deletion O(n). LinkedList uses doubly linked list, provides fast insertion/deletion O(1) but slow random access O(n).',
                        'keywords': ['array', 'linked', 'random access', 'insertion', 'deletion', 'complexity']
                    }
                ],
                'javascript': [
                    {
                        'id': str(uuid.uuid4()),
                        'question': 'Explain the difference between let, const, and var.',
                        'ideal_answer': 'var is function-scoped and hoisted. let is block-scoped and not hoisted. const is block-scoped, not hoisted, and cannot be reassigned. Prefer const and let over var.',
                        'keywords': ['scoped', 'hoisted', 'block', 'function', 'reassign']
                    },
                    {
                        'id': str(uuid.uuid4()),
                        'question': 'What is the event loop in JavaScript?',
                        'ideal_answer': 'The event loop continuously checks the call stack and callback queue. If stack is empty, it pushes the next callback from queue to stack for execution. This allows async operations in single-threaded JS.',
                        'keywords': ['call stack', 'callback queue', 'async', 'single threaded', 'execution']
                    },
                    {
                        'id': str(uuid.uuid4()),
                        'question': 'Explain closures in JavaScript.',
                        'ideal_answer': 'A closure is a function that has access to variables from its outer (enclosing) scope even after the outer function has returned. Used for data privacy and creating factory functions.',
                        'keywords': ['function', 'scope', 'variable', 'outer', 'data privacy']
                    }
                ],
                'general': [
                    {
                        'id': str(uuid.uuid4()),
                        'question': 'What is the difference between SQL and NoSQL databases?',
                        'ideal_answer': 'SQL databases are relational, use structured schema with tables. Good for complex queries and transactions. NoSQL databases are non-relational, schema-less or flexible schema. Better for unstructured data and horizontal scaling.',
                        'keywords': ['relational', 'schema', 'tables', 'query', 'scaling', 'unstructured']
                    },
                    {
                        'id': str(uuid.uuid4()),
                        'question': 'Explain RESTful API design principles.',
                        'ideal_answer': 'REST uses HTTP methods (GET, POST, PUT, DELETE). Resources identified by URLs. Stateless communication. JSON format for data exchange. Proper HTTP status codes. Versioning for API updates.',
                        'keywords': ['http', 'methods', 'resource', 'url', 'stateless', 'json', 'status']
                    },
                    {
                        'id': str(uuid.uuid4()),
                        'question': 'What is the difference between authentication and authorization?',
                        'ideal_answer': 'Authentication verifies who you are (login credentials). Authorization determines what you can access (permissions/roles). Authentication comes first, then authorization.',
                        'keywords': ['verify', 'login', 'credentials', 'permissions', 'access', 'roles']
                    },
                    {
                        'id': str(uuid.uuid4()),
                        'question': 'Explain Git branching strategies.',
                        'ideal_answer': 'Common strategies: Git Flow (feature, develop, release, hotfix branches), GitHub Flow (simple: main + feature branches), trunk-based development. Choose based on release cycle and team size.',
                        'keywords': ['branch', 'feature', 'main', 'release', 'hotfix', 'merge']
                    },
                    {
                        'id': str(uuid.uuid4()),
                        'question': 'What is Docker and why is it used?',
                        'ideal_answer': 'Docker is a containerization platform. Containers package application with all dependencies ensuring consistent environment across development, testing, and production. Lightweight compared to VMs.',
                        'keywords': ['container', 'docker', 'dependencies', 'environment', 'deployment', 'lightweight']
                    }
                ]
            },
            'hr': [
                {
                    'id': str(uuid.uuid4()),
                    'question': 'Tell me about yourself.',
                    'ideal_answer': 'Structure: Current role/Summary → Key achievements → Why this role/company. Keep it 2-3 minutes, relevant to the position. Mention education, experience, and key skills.',
                    'keywords': ['education', 'experience', 'skills', 'achievements', 'relevant', 'position']
                },
                {
                    'id': str(uuid.uuid4()),
                    'question': 'What are your strengths and weaknesses?',
                    'ideal_answer': 'Strengths: Related to job requirements. Give specific examples. Weaknesses: Real but not critical to job. Show self-awareness and steps taken for improvement.',
                    'keywords': ['strength', 'weakness', 'improvement', 'self-awareness', 'example']
                },
                {
                    'id': str(uuid.uuid4()),
                    'question': 'Why do you want to work at this company?',
                    'ideal_answer': 'Research the company beforehand. Mention: Company values, products/innovation, culture, growth opportunities. Show genuine interest and alignment with your career goals.',
                    'keywords': ['research', 'values', 'culture', 'growth', 'career', 'interest']
                },
                {
                    'id': str(uuid.uuid4()),
                    'question': 'Where do you see yourself in 5 years?',
                    'ideal_answer': 'Show ambition but realism. Want to grow within the company, develop skills, take on more responsibility. Aligned with company growth and your career path.',
                    'keywords': ['growth', 'skills', 'responsibility', 'career', 'company', 'advance']
                },
                {
                    'id': str(uuid.uuid4()),
                    'question': 'How do you handle pressure and deadlines?',
                    'ideal_answer': 'Prioritize tasks, break large projects into smaller tasks. Use time management techniques. Communicate early if deadlines at risk. Stay calm and focused. Learn from stressful situations.',
                    'keywords': ['prioritize', 'time management', 'deadline', 'communicate', 'calm', 'focus']
                },
                {
                    'id': str(uuid.uuid4()),
                    'question': 'Tell me about a time you faced a challenge at work.',
                    'ideal_answer': 'Use STAR method: Situation → Task → Action → Result. Choose relevant example. Focus on actions you took and positive outcomes. Show problem-solving and resilience.',
                    'keywords': ['star', 'situation', 'task', 'action', 'result', 'challenge', 'problem solving']
                },
                {
                    'id': str(uuid.uuid4()),
                    'question': 'Why should we hire you?',
                    'ideal_answer': 'Highlight unique combination of skills, experience, and qualities. Show how you can add value. Match your strengths to job requirements. Show enthusiasm and commitment.',
                    'keywords': ['skills', 'experience', 'value', 'strengths', 'enthusiasm', 'commitment']
                },
                {
                    'id': str(uuid.uuid4()),
                    'question': 'How do you work in a team?',
                    'ideal_answer': 'Communication, collaboration, respecting others opinions. Share knowledge, help teammates. Handle conflicts professionally. Balance individual and team goals.',
                    'keywords': ['communication', 'collaboration', 'team', 'conflict', 'support', 'goals']
                }
            ],
            'problem_solving': [
                {
                    'id': str(uuid.uuid4()),
                    'question': 'How would you approach debugging a complex issue?',
                    'ideal_answer': '1. Reproduce the issue consistently. 2. Break down the problem. 3. Check logs and error messages. 4. Use debugging tools. 5. Isolate variables. 6. Test hypothesis. 7. Document and learn.',
                    'keywords': ['reproduce', 'break down', 'logs', 'debugging', 'test', 'hypothesis']
                },
                {
                    'id': str(uuid.uuid4()),
                    'question': 'Explain your problem-solving process.',
                    'ideal_answer': '1. Understand the problem clearly. 2. Identify constraints. 3. Brainstorm solutions. 4. Evaluate options. 5. Implement solution. 6. Test thoroughly. 7. Optimize if needed.',
                    'keywords': ['understand', 'constraints', 'brainstorm', 'evaluate', 'implement', 'test']
                }
            ]
        }
    
    def generate_skill_based_questions(self, skills, interview_type='mixed'):
        questions = []
        skill_names = [s['skill'].lower() for s in skills]
        
        if interview_type in ['technical', 'mixed']:
            for skill in skill_names:
                if skill in self.question_bank['technical']:
                    selected = random.sample(
                        self.question_bank['technical'][skill],
                        min(2, len(self.question_bank['technical'][skill]))
                    )
                    questions.extend(selected)
            
            if len(questions) < 5:
                general_tech = random.sample(
                    self.question_bank['technical']['general'],
                    min(5, len(self.question_bank['technical']['general']))
                )
                questions.extend(general_tech)
        
        if interview_type in ['hr', 'mixed']:
            hr_questions = random.sample(
                self.question_bank['hr'],
                min(3, len(self.question_bank['hr']))
            )
            questions.extend(hr_questions)
        
        problem_solving = random.sample(
            self.question_bank['problem_solving'],
            min(2, len(self.question_bank['problem_solving']))
        )
        questions.extend(problem_solving)
        
        random.shuffle(questions)
        return questions[:10]
    
    def generate_general_questions(self, interview_type='mixed'):
        questions = []
        
        if interview_type in ['technical', 'mixed']:
            general_tech = random.sample(
                self.question_bank['technical']['general'],
                min(5, len(self.question_bank['technical']['general']))
            )
            questions.extend(general_tech)
            
            for lang in ['python', 'java', 'javascript']:
                lang_questions = random.sample(
                    self.question_bank['technical'].get(lang, []),
                    min(2, len(self.question_bank['technical'].get(lang, [])))
                )
                questions.extend(lang_questions)
        
        if interview_type in ['hr', 'mixed']:
            hr_questions = random.sample(
                self.question_bank['hr'],
                min(4, len(self.question_bank['hr']))
            )
            questions.extend(hr_questions)
        
        problem_solving = random.sample(
            self.question_bank['problem_solving'],
            min(2, len(self.question_bank['problem_solving']))
        )
        questions.extend(problem_solving)
        
        random.shuffle(questions)
        return questions[:10]
