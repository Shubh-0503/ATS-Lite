def parse_skills(skills_input) -> list[str]:
    if not skills_input:
        return []

    # Handle both string and list inputs
    if isinstance(skills_input, list):
        raw_skills = skills_input
    else:
        raw_skills = str(skills_input).split(',')

    seen = set()
    result = []
    for skill in raw_skills:
        cleaned = skill.strip().lower()
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            result.append(cleaned)

    return result


def calculate_match_score(job_skills_input, candidate_skills_input) -> dict:
    
    job_skills = parse_skills(job_skills_input)
    candidate_skills = parse_skills(candidate_skills_input)

    # Edge case: if job has no required skills, we can't evaluate
    if not job_skills:
        return {
            'score': 0.0,
            'matched': [],
            'missing': [],
            'extra': candidate_skills,
            'job_skills': job_skills,
            'candidate_skills': candidate_skills,
        }

    # Edge case: candidate listed no skills
    if not candidate_skills:
        return {
            'score': 0.0,
            'matched': [],
            'missing': job_skills,
            'extra': [],
            'job_skills': job_skills,
            'candidate_skills': candidate_skills,
        }

    job_set = set(job_skills)
    candidate_set = set(candidate_skills)

    matched = sorted(job_set & candidate_set)         # Intersection
    missing = sorted(job_set - candidate_set)         # Job needs but candidate lacks
    extra = sorted(candidate_set - job_set)           # Candidate has but job doesn't need

    score = round((len(matched) / len(job_skills)) * 100, 1)

    return {
        'score': score,
        'matched': matched,
        'missing': missing,
        'extra': extra,
        'job_skills': job_skills,
        'candidate_skills': candidate_skills,
    }


def get_score_label(score: float) -> str:
    
    if score == 100:
        return 'Perfect Match'
    elif score >= 76:
        return 'Strong Match'
    elif score >= 51:
        return 'Good Match'
    elif score >= 26:
        return 'Partial Match'
    else:
        return 'Poor Match'
