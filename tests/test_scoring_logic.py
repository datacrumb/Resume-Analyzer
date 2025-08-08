from typing import Dict, List
from src.ai.resume_analyzer import ResumeAnalyzer

class ScoringLogicTester:
    """Test scoring logic without API calls"""
    
    def __init__(self):
        self.analyzer = ResumeAnalyzer()
    
    def test_prompt_generation(self):
        """Test that prompts are generated correctly"""
        print("Testing prompt generation...")
        
        # Test data
        resume_content = "Software Engineer with 5 years experience in Python and React"
        job_description = "We need a Python developer"
        requirements = "Python, React, 2+ years experience"
        resume_url = "https://example.com/resume.pdf"
        
        # Test system prompt creation
        system_prompt = self.analyzer._create_system_prompt()
        
        # Test user prompt creation
        user_prompt = self.analyzer._create_user_prompt(
            resume_content=resume_content,
            job_description=job_description,
            requirements=requirements,
            resume_url=resume_url
        )
        
        # Verify system prompt contains required elements
        system_required_elements = [
            "expert HR recruiter",
            "ANALYSIS FRAMEWORK",
            "SCORING CRITERIA",
            "overall_score",
            "reasoning"
        ]
        
        # Verify user prompt contains required elements
        user_required_elements = [
            "JOB DESCRIPTION:",
            "JOB REQUIREMENTS:",
            "RESUME CONTENT:",
            "RESUME SOURCE:"
        ]
        
        missing_system_elements = []
        for element in system_required_elements:
            if element not in system_prompt:
                missing_system_elements.append(element)
        
        missing_user_elements = []
        for element in user_required_elements:
            if element not in user_prompt:
                missing_user_elements.append(element)
        
        if missing_system_elements:
            print(f"❌ Missing elements in system prompt: {missing_system_elements}")
            return False
        elif missing_user_elements:
            print(f"❌ Missing elements in user prompt: {missing_user_elements}")
            return False
        else:
            print("✅ Prompt generation test passed")
            print(f"   System prompt length: {len(system_prompt)} characters")
            print(f"   User prompt length: {len(user_prompt)} characters")
            return True
    
    def test_score_extraction(self):
        """Test score extraction from AI responses"""
        print("\nTesting score extraction...")
        
        test_cases = [
            # Valid responses with overall_score
            ('{"overall_score": "95%", "reasoning": "Perfect fit"}', {"score": "95%", "reasoning": "Perfect fit"}),
            ('{"overall_score": "85%", "reasoning": "Good match"}', {"score": "85%", "reasoning": "Good match"}),
            ('{"overall_score": "65%", "reasoning": "Partial match"}', {"score": "65%", "reasoning": "Partial match"}),
            ('{"overall_score": "35%", "reasoning": "Poor match"}', {"score": "35%", "reasoning": "Poor match"}),
            ('{"overall_score": "15%", "reasoning": "Irrelevant"}', {"score": "15%", "reasoning": "Irrelevant"}),
            ('{"overall_score": "OVERQUALIFIED", "reasoning": "Too experienced for this role"}', {"score": "OVERQUALIFIED", "reasoning": "Too experienced for this role"}),
            
            # Responses with detailed breakdown (should still extract overall_score and reasoning)
            ('{"overall_score": "85%", "technical_skills_match": "90%", "experience_relevance": "85%", "soft_skills_cultural_fit": "80%", "education_certifications": "85%", "career_progression": "80%", "reasoning": "Strong candidate"}', {"score": "85%", "reasoning": "Strong candidate"}),
            ('{"overall_score": "OVERQUALIFIED", "technical_skills_match": "95%", "experience_relevance": "100%", "soft_skills_cultural_fit": "90%", "education_certifications": "100%", "career_progression": "100%", "reasoning": "Overqualified for junior role"}', {"score": "OVERQUALIFIED", "reasoning": "Overqualified for junior role"}),
            
            # Invalid responses
            ("Invalid response", {"score": "", "reasoning": "No JSON found"}),
            ('{"overall_score": "150%", "reasoning": "Too high"}', {"score": "", "reasoning": "Too high"}),  # Invalid percentage
            ('{"overall_score": "-20%", "reasoning": "Too low"}', {"score": "", "reasoning": "Too low"}),  # Invalid percentage
            ('{"overall_score": "abc", "reasoning": "Invalid format"}', {"score": "", "reasoning": "Invalid format"}),  # Invalid format
            
            # Missing fields
            ('{"reasoning": "No score provided"}', {"score": "", "reasoning": "No score provided"}),
            ('{"overall_score": "85%"}', {"score": "85%", "reasoning": ""}),
            
            # JSON with markdown formatting
            ('```json\n{"overall_score": "90%", "reasoning": "Great fit"}\n```', {"score": "90%", "reasoning": "Great fit"}),
            ('```python\n{"overall_score": "75%", "reasoning": "Good match"}\n```', {"score": "75%", "reasoning": "Good match"}),
        ]
        
        passed = 0
        total = len(test_cases)
        
        for response, expected in test_cases:
            actual = self.analyzer._extract_score_from_response(response)
            if actual == expected:
                print(f"✅ '{response[:50]}...' -> {actual}")
                passed += 1
            else:
                print(f"❌ '{response[:50]}...' -> {actual} (expected {expected})")
        
        print(f"Score extraction: {passed}/{total} tests passed")
        return passed == total
    
    def test_cv_scenarios(self):
        """Test CV scenario analysis without API calls"""
        print("\nTesting CV scenario analysis...")
        
        scenarios = {
            "perfect_fit": {
                "cv": "Senior Software Engineer with 5 years Python, React, SQL experience",
                "job": "Python Developer needed",
                "requirements": "Python, React, SQL, 2+ years",
                "expected_range": (9, 10)
            },
            "overqualified": {
                "cv": "Principal Engineer with 15 years experience, PhD in Computer Science",
                "job": "Junior Python Developer needed",
                "requirements": "Python, React, SQL, 1+ years",
                "expected_range": (7, 9)
            },
            "partial_fit": {
                "cv": "Junior Developer with basic Python knowledge",
                "job": "Python Developer needed", 
                "requirements": "Python, React, SQL, 2+ years",
                "expected_range": (5, 7)
            },
            "irrelevant": {
                "cv": "Chef with 10 years cooking experience",
                "job": "Python Developer needed",
                "requirements": "Python, React, SQL, 2+ years", 
                "expected_range": (1, 2)
            }
        }
        
        for scenario, data in scenarios.items():
            print(f"\nTesting {scenario}:")
            print(f"CV: {data['cv']}")
            print(f"Job: {data['job']}")
            print(f"Requirements: {data['requirements']}")
            print(f"Expected range: {data['expected_range']}")
            
            # This would normally call the API, but we're just testing the structure
            system_prompt = self.analyzer._create_system_prompt()
            user_prompt = self.analyzer._create_user_prompt(
                resume_content=data['cv'],
                job_description=data['job'],
                requirements=data['requirements']
            )
            
            print(f"✅ Prompts generated successfully (System: {len(system_prompt)} chars, User: {len(user_prompt)} chars)")
        
        return True

def main():
    """Run scoring logic tests"""
    tester = ScoringLogicTester()
    
    print("🧪 SCORING LOGIC TESTS")
    print("=" * 50)
    
    tests = [
        ("Prompt Generation", tester.test_prompt_generation),
        ("Score Extraction", tester.test_score_extraction),
        ("CV Scenarios", tester.test_cv_scenarios)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error in {test_name}: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    print(f"Success Rate: {(passed/total)*100:.1f}%")

if __name__ == "__main__":
    main() 