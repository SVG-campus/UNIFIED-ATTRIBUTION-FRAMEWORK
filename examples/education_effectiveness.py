"""
Education Course Effectiveness Attribution
===========================================
Analyze impact of courses on student outcomes
"""

import numpy as np
import pandas as pd
from collections import defaultdict


def generate_education_data(n_students=500):
    """Generate synthetic education data"""

    np.random.seed(42)

    # Course catalog
    courses = {
        'Core': ['Math_101', 'English_101', 'Science_101'],
        'STEM': ['Math_201', 'Physics', 'Computer_Science', 'Statistics'],
        'Humanities': ['History', 'Philosophy', 'Psychology', 'Economics'],
        'Skills': ['Writing', 'Communication', 'Critical_Thinking']
    }

    all_courses = []
    for category_courses in courses.values():
        all_courses.extend(category_courses)

    # Generate student enrollments
    data = pd.DataFrame(0, index=range(n_students), columns=all_courses)

    for i in range(n_students):
        # Core courses (most students take)
        for course in courses['Core']:
            if np.random.random() < 0.85:
                data.loc[i, course] = 1

        # STEM courses
        n_stem = np.random.randint(0, 3)
        stem_choices = np.random.choice(courses['STEM'], n_stem, replace=False)
        for course in stem_choices:
            data.loc[i, course] = 1

        # Humanities courses
        n_hum = np.random.randint(0, 3)
        hum_choices = np.random.choice(courses['Humanities'], n_hum, replace=False)
        for course in hum_choices:
            data.loc[i, course] = 1

        # Skills courses
        n_skills = np.random.randint(0, 2)
        skill_choices = np.random.choice(courses['Skills'], n_skills, replace=False)
        for course in skill_choices:
            data.loc[i, course] = 1

    # Generate GPA based on courses
    gpa = 2.0 + np.random.normal(0, 0.3, n_students)

    # Course effects on GPA
    for course in all_courses:
        course_effect = 0.0

        # Core courses boost
        if course in courses['Core']:
            course_effect = 0.3

        # STEM courses (higher boost)
        elif course in courses['STEM']:
            course_effect = 0.4
            # Math courses especially important
            if 'Math' in course:
                course_effect = 0.5

        # Humanities courses
        elif course in courses['Humanities']:
            course_effect = 0.25

        # Skills courses (multiplicative)
        elif course in courses['Skills']:
            course_effect = 0.35

        gpa += data[course] * course_effect

    # Add synergy effects
    # Math + Computer Science synergy
    gpa += (data['Math_201'] & data['Computer_Science']) * 0.3

    # Writing + any humanities synergy
    for hum_course in courses['Humanities']:
        gpa += (data['Writing'] & data[hum_course]) * 0.2

    # Clip GPA to realistic range
    gpa = np.clip(gpa, 0.0, 4.0)
    data['GPA'] = gpa

    # Success metric (GPA >= 3.0)
    data['Success'] = (gpa >= 3.0).astype(int)

    return data, courses


def analyze_education_effectiveness():
    """Analyze course effectiveness"""

    print("="*70)
    print("EDUCATION EFFECTIVENESS ATTRIBUTION")
    print("="*70)

    # Generate data
    print("\nGenerating student course data...")
    data, courses = generate_education_data(n_students=1000)

    all_courses = []
    for category_courses in courses.values():
        all_courses.extend(category_courses)

    print(f"Students: {len(data):,}")
    print(f"Average GPA: {data['GPA'].mean():.2f}")
    print(f"Success rate (GPA >= 3.0): {data['Success'].mean():.1%}")

    # Enrollment statistics
    print("\nCourse Enrollment:")
    for category, category_courses in courses.items():
        print(f"\n  {category}:")
        for course in category_courses:
            enrollment = data[course].sum()
            rate = data[course].mean()
            print(f"    {course:20s}: {enrollment:4d} ({rate:.1%})")

    # Course attribution
    print("\n" + "="*70)
    print("COURSE ATTRIBUTION ANALYSIS")
    print("="*70)

    attribution = {}
    course_impact = {}

    for course in all_courses:
        # Students who took this course
        with_course = data[data[course] == 1]['GPA']
        without_course = data[data[course] == 0]['GPA']

        if len(with_course) > 0 and len(without_course) > 0:
            impact = with_course.mean() - without_course.mean()
            course_impact[course] = impact
            attribution[course] = max(0, impact)
        else:
            course_impact[course] = 0.0
            attribution[course] = 0.0

    # Normalize attribution
    total = sum(attribution.values())
    if total > 0:
        attribution = {c: v/total for c, v in attribution.items()}

    print("\nCourse Impact on GPA:")
    print("-"*70)
    for course, impact in sorted(course_impact.items(), 
                                 key=lambda x: x[1], reverse=True):
        attr = attribution.get(course, 0)
        print(f"  {course:20s}: +{impact:5.3f} GPA | "
              f"Attribution: {attr:.4f} ({attr*100:.2f}%)")

    # Category analysis
    print("\n" + "="*70)
    print("CATEGORY IMPACT")
    print("="*70)

    category_attribution = defaultdict(float)
    for category, category_courses in courses.items():
        for course in category_courses:
            category_attribution[category] += attribution.get(course, 0)

    print("\nImpact by Course Category:")
    for category, total_attr in sorted(category_attribution.items(), 
                                       key=lambda x: x[1], reverse=True):
        print(f"  {category:15s}: {total_attr:.4f} ({total_attr*100:.2f}%)")

    # Success factors
    print("\n" + "="*70)
    print("SUCCESS FACTORS")
    print("="*70)

    print("\nSuccess Rate by Course Count:")
    course_counts = data[all_courses].sum(axis=1)
    for count in range(course_counts.min(), min(course_counts.max() + 1, 10)):
        students = data[course_counts == count]
        if len(students) > 0:
            success_rate = students['Success'].mean()
            avg_gpa = students['GPA'].mean()
            print(f"  {count:2d} courses: {len(students):3d} students | "
                  f"Success: {success_rate:.1%} | Avg GPA: {avg_gpa:.2f}")

    # Recommendations
    print("\n" + "="*70)
    print("RECOMMENDATIONS")
    print("="*70)

    top_3_courses = sorted(course_impact.items(), 
                           key=lambda x: x[1], reverse=True)[:3]

    print("\n1. Most Impactful Courses (expand offerings):")
    for i, (course, impact) in enumerate(top_3_courses, 1):
        print(f"   {i}. {course}: +{impact:.3f} GPA impact")

    print(f"\n2. Recommended course load: "
          f"{int(data[data['Success']==1][all_courses].sum(axis=1).mean())} courses")

    # Find underutilized high-impact courses
    high_impact = [c for c, imp in course_impact.items() if imp > 0.3]
    low_enrollment = [c for c in high_impact if data[c].mean() < 0.3]

    if low_enrollment:
        print(f"\n3. Underutilized high-impact courses:")
        for course in low_enrollment:
            print(f"   - {course}: {data[course].mean():.1%} enrollment, "
                  f"+{course_impact[course]:.3f} GPA")

    return attribution, data


if __name__ == "__main__":
    attribution, data = analyze_education_effectiveness()

    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)