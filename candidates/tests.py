from django.test import TestCase
from candidates.utils import calculate_match_score, parse_skills, get_score_label


class SkillParsingTests(TestCase):

    def test_basic_parsing(self):
        result = parse_skills("Python, Django, REST API")
        self.assertEqual(result, ['python', 'django', 'rest api'])

    def test_case_insensitive(self):
        result = parse_skills("PYTHON, Django, python")
        self.assertEqual(result, ['python', 'django'])  # deduped

    def test_extra_spaces(self):
        result = parse_skills("  Python ,  Django  ")
        self.assertEqual(result, ['python', 'django'])

    def test_empty_string(self):
        self.assertEqual(parse_skills(""), [])

    def test_none_input(self):
        self.assertEqual(parse_skills(None), [])

    def test_list_input(self):
        result = parse_skills(['Python', 'Django'])
        self.assertEqual(result, ['python', 'django'])


class SkillMatchingTests(TestCase):

    def test_perfect_match(self):
        result = calculate_match_score("Python, Django", "Python, Django")
        self.assertEqual(result['score'], 100.0)
        self.assertEqual(result['missing'], [])

    def test_partial_match(self):
        result = calculate_match_score("Python, Django, Docker", "Python, Django")
        self.assertEqual(result['score'], round(2/3 * 100, 1))
        self.assertEqual(result['missing'], ['docker'])

    def test_no_match(self):
        result = calculate_match_score("Python, Django", "React, Node.js")
        self.assertEqual(result['score'], 0.0)

    def test_empty_job_skills(self):
        result = calculate_match_score("", "Python, Django")
        self.assertEqual(result['score'], 0.0)

    def test_empty_candidate_skills(self):
        result = calculate_match_score("Python, Django", "")
        self.assertEqual(result['score'], 0.0)
        self.assertEqual(result['missing'], ['django', 'python'])

    def test_case_insensitive_match(self):
        result = calculate_match_score("Python", "PYTHON")
        self.assertEqual(result['score'], 100.0)

    def test_extra_skills_not_penalized(self):
        result = calculate_match_score("Python", "Python, Django, React")
        self.assertEqual(result['score'], 100.0)
        self.assertIn('django', result['extra'])

    def test_score_labels(self):
        self.assertEqual(get_score_label(100), 'Perfect Match')
        self.assertEqual(get_score_label(80), 'Strong Match')
        self.assertEqual(get_score_label(60), 'Good Match')
        self.assertEqual(get_score_label(40), 'Partial Match')
        self.assertEqual(get_score_label(10), 'Poor Match')
