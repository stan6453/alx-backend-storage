#!/usr/bin/env python3
"""
Write a Python function that returns all students sorted by average score:
 * Prototype: def top_students(mongo_collection):
 * mongo_collection will be the pymongo collection object
 * The top must be ordered
 * The average score must be part of each item returns with key = averageScore
"""


def top_students(mongo_collection):
    """returns all students sorted by average score:"""
    students = mongo_collection.find()

    # Calculate average scores for each student
    for student in students:
        topics = student.get('topics')
        total_score = sum(topic.get('score') for topic in topics)
        average_score = total_score / len(topics)
        student['averageScore'] = average_score

    # Sort students by average score in descending order
    sorted_students = sorted(students, key=lambda s: s['averageScore'], reverse=True)

    return sorted_students