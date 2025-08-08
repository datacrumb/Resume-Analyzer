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
        
        # Test prompt creation
        prompt = self.analyzer._create_analysis_prompt(
            resume_content=resume_content,
            job_description=job_description,
            requirements=requirements,
            resume_url=resume_url
        )
        
        # Verify prompt contains all required elements
        required_elements = [
            "JOB DESCRIPTION:",
            "JOB REQUIREMENTS:",
            "RESUME CONTENT:",
            "RESUME SOURCE:",
            '"score": "[percentage]%"',
            '"reasoning": "[detailed explanation of the score]"'
        ]
        
        missing_elements = []
        for element in required_elements:
            if element not in prompt:
                missing_elements.append(element)
        
        if missing_elements:
            print(f"❌ Missing elements in prompt: {missing_elements}")
            return False
        else:
            print("✅ Prompt generation test passed")
            return True
    
    def test_score_extraction(self):
        """Test score extraction from AI responses"""
        print("\nTesting score extraction...")
        
        test_cases = [
            ('{"score": "95%", "reasoning": "Perfect fit"}', {"score": "95%", "reasoning": "Perfect fit"}),
            ('{"score": "85%", "reasoning": "Good match"}', {"score": "85%", "reasoning": "Good match"}),
            ('{"score": "65%", "reasoning": "Partial match"}', {"score": "65%", "reasoning": "Partial match"}),
            ('{"score": "35%", "reasoning": "Poor match"}', {"score": "35%", "reasoning": "Poor match"}),
            ('{"score": "15%", "reasoning": "Irrelevant"}', {"score": "15%", "reasoning": "Irrelevant"}),
            ('{"score": "OVERQUALIFIED", "reasoning": "Too experienced for this role"}', {"score": "OVERQUALIFIED", "reasoning": "Too experienced for this role"}),
            ('{"score": "overqualified", "reasoning": "Senior applying for junior position"}', {"score": "OVERQUALIFIED", "reasoning": "Senior applying for junior position"}),
            ("Invalid response", {"score": "", "reasoning": "Could not parse AI response"}),  # Should return empty score
            ('{"score": "150%", "reasoning": "Too high"}', {"score": "", "reasoning": "Invalid score format"}),  # Should return empty score for invalid
            ('{"score": "-20%", "reasoning": "Too low"}', {"score": "", "reasoning": "Invalid score format"}),  # Should return empty score for invalid
        ]
        
        passed = 0
        total = len(test_cases)
        
        for response, expected in test_cases:
            actual = self.analyzer._extract_score_from_response(response)
            if actual == expected:
                print(f"✅ '{response}' -> {actual}")
                passed += 1
            else:
                print(f"❌ '{response}' -> {actual} (expected {expected})")
        
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
            prompt = self.analyzer._create_analysis_prompt(
                resume_content=data['cv'],
                job_description=data['job'],
                requirements=data['requirements']
            )
            
            print(f"✅ Prompt generated successfully ({len(prompt)} characters)")
        
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