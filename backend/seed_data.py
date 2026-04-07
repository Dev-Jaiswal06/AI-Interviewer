from app import create_app, db
from app.models import CodingProblem, QuestionBank
import json


def seed_coding_problems():
    problems = [
        {
            'title': 'Two Sum',
            'description': '''Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

Example:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].''',
            'difficulty': 'easy',
            'problem_type': 'arrays',
            'starter_code': '''def two_sum(nums, target):
    # Your code here
    pass

# Test
print(two_sum([2,7,11,15], 9))''',
            'test_cases': json.dumps([
                {'input': '[2,7,11,15]\n9', 'expected_output': '[0, 1]'},
                {'input': '[3,2,4]\n6', 'expected_output': '[1, 2]'},
                {'input': '[3,3]\n6', 'expected_output': '[0, 1]'}
            ]),
            'solution': '''def two_sum(nums, target):
    prev_map = {}
    for i, n in enumerate(nums):
        diff = target - n
        if diff in prev_map:
            return [prev_map[diff], i]
        prev_map[n] = i
    return []''',
            'hints': 'Use a hashmap to store previously seen numbers and their indices.',
            'points': 10
        },
        {
            'title': 'Valid Parentheses',
            'description': '''Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

Example:
Input: s = "()[]{}"
Output: true''',
            'difficulty': 'easy',
            'problem_type': 'strings',
            'starter_code': '''def is_valid(s):
    # Your code here
    pass

# Test
print(is_valid("()[]{}"))''',
            'test_cases': json.dumps([
                {'input': '()', 'expected_output': 'True'},
                {'input': '()[]{}', 'expected_output': 'True'},
                {'input': '(]', 'expected_output': 'False'}
            ]),
            'solution': '''def is_valid(s):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    for char in s:
        if char in mapping:
            if not stack or stack.pop() != mapping[char]:
                return False
        else:
            stack.append(char)
    return len(stack) == 0''',
            'hints': 'Use a stack to keep track of opening brackets.',
            'points': 10
        },
        {
            'title': 'Reverse Linked List',
            'description': '''Given the head of a singly linked list, reverse the list, and return the reversed list.

Example:
Input: head = [1,2,3,4,5]
Output: [5,4,3,2,1]''',
            'difficulty': 'medium',
            'problem_type': 'linked_lists',
            'starter_code': '''class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head):
    # Your code here
    pass''',
            'test_cases': json.dumps([
                {'input': '[1,2,3,4,5]', 'expected_output': '[5,4,3,2,1]'},
                {'input': '[1,2]', 'expected_output': '[2,1]'},
                {'input': '[]', 'expected_output': '[]'}
            ]),
            'solution': '''def reverse_list(head):
    prev = None
    current = head
    while current:
        next_temp = current.next
        current.next = prev
        prev = current
        current = next_temp
    return prev''',
            'hints': 'Use three pointers: previous, current, and next.',
            'points': 20
        },
        {
            'title': 'Binary Search',
            'description': '''Given an array of integers nums which is sorted in ascending order, and an integer target, write a function to search target in nums.

If target exists, then return its index. Otherwise, return -1.

You must write an algorithm with O(log n) runtime complexity.

Example:
Input: nums = [-1,0,3,5,9,12], target = 9
Output: 4''',
            'difficulty': 'easy',
            'problem_type': 'search',
            'starter_code': '''def search(nums, target):
    # Your code here
    pass

# Test
print(search([-1,0,3,5,9,12], 9))''',
            'test_cases': json.dumps([
                {'input': '[-1,0,3,5,9,12]\n9', 'expected_output': '4'},
                {'input': '[-1,0,3,5,9,12]\n2', 'expected_output': '-1'}
            ]),
            'solution': '''def search(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1''',
            'hints': 'Use two pointers and calculate middle index each iteration.',
            'points': 10
        },
        {
            'title': 'Maximum Subarray',
            'description': '''Given an integer array nums, find the subarray with the largest sum, and return its sum.

Example:
Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6
Explanation: The subarray [4,-1,2,1] has the largest sum 6.''',
            'difficulty': 'medium',
            'problem_type': 'arrays',
            'starter_code': '''def max_subarray(nums):
    # Your code here
    pass

# Test
print(max_subarray([-2,1,-3,4,-1,2,1,-5,4]))''',
            'test_cases': json.dumps([
                {'input': '[-2,1,-3,4,-1,2,1,-5,4]', 'expected_output': '6'},
                {'input': '[1]', 'expected_output': '1'},
                {'input': '[5,4,-1,7,8]', 'expected_output': '23'}
            ]),
            'solution': '''def max_subarray(nums):
    max_sum = nums[0]
    current_sum = nums[0]
    for num in nums[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    return max_sum''',
            'hints': 'Use Kadane\'s algorithm - track current sum and maximum sum.',
            'points': 20
        },
        {
            'title': 'Climbing Stairs',
            'description': '''You are climbing a staircase. It takes n steps to reach the top.

Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

Example:
Input: n = 3
Output: 3
Explanation: There are three ways to climb to the top:
1. 1 step + 1 step + 1 step
2. 1 step + 2 steps
3. 2 steps + 1 step''',
            'difficulty': 'easy',
            'problem_type': 'dynamic_programming',
            'starter_code': '''def climb_stairs(n):
    # Your code here
    pass

# Test
print(climb_stairs(3))''',
            'test_cases': json.dumps([
                {'input': '3', 'expected_output': '3'},
                {'input': '2', 'expected_output': '2'},
                {'input': '4', 'expected_output': '5'}
            ]),
            'solution': '''def climb_stairs(n):
    if n <= 2:
        return n
    a, b = 1, 2
    for i in range(3, n + 1):
        a, b = b, a + b
    return b''',
            'hints': 'This follows Fibonacci sequence. dp[i] = dp[i-1] + dp[i-2]',
            'points': 10
        },
        {
            'title': 'Merge Two Sorted Lists',
            'description': '''You are given the heads of two sorted linked lists list1 and list2.

Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists.

Return the head of the merged linked list.

Example:
Input: list1 = [1,2,4], list2 = [1,3,4]
Output: [1,1,2,3,4,4]''',
            'difficulty': 'easy',
            'problem_type': 'linked_lists',
            'starter_code': '''class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def merge_two_lists(list1, list2):
    # Your code here
    pass''',
            'test_cases': json.dumps([
                {'input': '[1,2,4]\n[1,3,4]', 'expected_output': '[1,1,2,3,4,4]'},
                {'input': '[]\n[]', 'expected_output': '[]'}
            ]),
            'solution': '''def merge_two_lists(list1, list2):
    dummy = ListNode()
    current = dummy
    while list1 and list2:
        if list1.val <= list2.val:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next
        current = current.next
    current.next = list1 or list2
    return dummy.next''',
            'hints': 'Use a dummy node to simplify edge cases.',
            'points': 10
        },
        {
            'title': 'Longest Common Subsequence',
            'description': '''Given two strings text1 and text2, return the length of their longest common subsequence.

A subsequence is a sequence that can be derived from another sequence by deleting some or no elements without changing the order of the remaining elements.

Example:
Input: text1 = "abcde", text2 = "ace"
Output: 3
Explanation: The longest common subsequence is "ace" and its length is 3.''',
            'difficulty': 'hard',
            'problem_type': 'strings',
            'starter_code': '''def longest_common_subsequence(text1, text2):
    # Your code here
    pass

# Test
print(longest_common_subsequence("abcde", "ace"))''',
            'test_cases': json.dumps([
                {'input': 'abcde\nace', 'expected_output': '3'},
                {'input': 'abc\nabc', 'expected_output': '3'},
                {'input': 'abc\ndef', 'expected_output': '0'}
            ]),
            'solution': '''def longest_common_subsequence(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]''',
            'hints': 'Use dynamic programming with 2D array.',
            'points': 30
        }
    ]
    
    for p in problems:
        existing = CodingProblem.query.filter_by(title=p['title']).first()
        if not existing:
            problem = CodingProblem(**p)
            db.session.add(problem)
    
    db.session.commit()
    print(f"Added {len(problems)} coding problems")


def seed_questions():
    questions = [
        {'category': 'technical', 'subcategory': 'python', 'question_text': 'Explain Python decorators.', 'ideal_answer': 'Decorators modify function behavior without changing code.', 'keywords': '["decorator", "function", "wrapper", "@"]', 'difficulty': 'medium'},
        {'category': 'technical', 'subcategory': 'general', 'question_text': 'What is the difference between SQL and NoSQL?', 'ideal_answer': 'SQL is relational, NoSQL is non-relational/flexible schema.', 'keywords': '["relational", "schema", "flexible"]', 'difficulty': 'medium'},
        {'category': 'hr', 'subcategory': 'behavioral', 'question_text': 'Tell me about yourself.', 'ideal_answer': 'Professional background, key achievements, and goals.', 'keywords': '["background", "achievements", "goals"]', 'difficulty': 'easy'},
        {'category': 'hr', 'subcategory': 'behavioral', 'question_text': 'Why should we hire you?', 'ideal_answer': 'Skills match, enthusiasm, and value addition.', 'keywords': '["skills", "enthusiasm", "value"]', 'difficulty': 'easy'},
    ]
    
    for q in questions:
        existing = QuestionBank.query.filter_by(question_text=q['question_text']).first()
        if not existing:
            question = QuestionBank(**q)
            db.session.add(question)
    
    db.session.commit()
    print(f"Added {len(questions)} interview questions")


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        seed_coding_problems()
        seed_questions()
        print("Database seeded successfully!")
