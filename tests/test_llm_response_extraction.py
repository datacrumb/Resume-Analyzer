#!/usr/bin/env python3
"""
Test script for LLM response extraction functionality
Tests the _extract_score_from_response method with various response formats
"""

import json
from src.ai.resume_analyzer import ResumeAnalyzer

class LLMResponseExtractionTester:
    """Test LLM response extraction with various formats"""
    
    def __init__(self):
        self.analyzer = ResumeAnalyzer()
    
    def test_valid_responses(self):
        """Test extraction from valid AI responses"""
        print("Testing valid AI responses...")
        
        test_cases = [
            {
                "name": "Perfect Fit Response",
                "response": '{"score": "95%", "reasoning": "Excellent match with all requirements"}',
                "expected": {
                    "score": "95%", 
                    "technical_skills_match": "",
                    "experience_relevance": "",
                    "soft_skills_cultural_fit": "",
                    "education_certifications": "",
                    "career_progression": "",
                    "reasoning": "Excellent match with all requirements"
                }
            },
            {
                "name": "Overqualified Response", 
                "response": '{"score": "OVERQUALIFIED", "reasoning": "Too experienced for this role"}',
                "expected": {
                    "score": "OVERQUALIFIED", 
                    "technical_skills_match": "",
                    "experience_relevance": "",
                    "soft_skills_cultural_fit": "",
                    "education_certifications": "",
                    "career_progression": "",
                    "reasoning": "Too experienced for this role"
                }
            },
            {
                "name": "Detailed Breakdown Response",
                "response": '{"score": "85%", "technical_skills_match": "90%", "experience_relevance": "85%", "soft_skills_cultural_fit": "80%", "education_certifications": "85%", "career_progression": "80%", "reasoning": "Strong candidate with minor gaps"}',
                "expected": {
                    "score": "85%", 
                    "technical_skills_match": "90%",
                    "experience_relevance": "85%",
                    "soft_skills_cultural_fit": "80%",
                    "education_certifications": "85%",
                    "career_progression": "80%",
                    "reasoning": "Strong candidate with minor gaps"
                }
            },
            {
                "name": "Markdown Formatted Response",
                "response": '```json\n{"score": "75%", "reasoning": "Good match with some gaps"}\n```',
                "expected": {
                    "score": "75%", 
                    "technical_skills_match": "",
                    "experience_relevance": "",
                    "soft_skills_cultural_fit": "",
                    "education_certifications": "",
                    "career_progression": "",
                    "reasoning": "Good match with some gaps"
                }
            }
        ]
        
        passed = 0
        total = len(test_cases)
        
        for test_case in test_cases:
            result = self.analyzer._extract_score_from_response(test_case["response"])
            if result == test_case["expected"]:
                print(f"✅ {test_case['name']}: PASS")
                passed += 1
            else:
                print(f"❌ {test_case['name']}: FAIL")
                print(f"   Expected: {test_case['expected']}")
                print(f"   Got: {result}")
        
        print(f"Valid responses: {passed}/{total} passed")
        return passed == total
    
    def test_invalid_responses(self):
        """Test extraction from invalid AI responses"""
        print("\nTesting invalid AI responses...")
        
        test_cases = [
            {
                "name": "No JSON",
                "response": "This is not a JSON response",
                "expected": {"score": "", "reasoning": "No JSON found"}
            },
            {
                "name": "Invalid Percentage",
                "response": '{"score": "150%", "reasoning": "Invalid score"}',
                "expected": {
                    "score": "", 
                    "technical_skills_match": "",
                    "experience_relevance": "",
                    "soft_skills_cultural_fit": "",
                    "education_certifications": "",
                    "career_progression": "",
                    "reasoning": "Invalid score"
                }
            },
            {
                "name": "Negative Percentage",
                "response": '{"score": "-20%", "reasoning": "Negative score"}',
                "expected": {
                    "score": "", 
                    "technical_skills_match": "",
                    "experience_relevance": "",
                    "soft_skills_cultural_fit": "",
                    "education_certifications": "",
                    "career_progression": "",
                    "reasoning": "Negative score"
                }
            },
            {
                "name": "Non-numeric Score",
                "response": '{"score": "abc", "reasoning": "Invalid format"}',
                "expected": {
                    "score": "", 
                    "technical_skills_match": "",
                    "experience_relevance": "",
                    "soft_skills_cultural_fit": "",
                    "education_certifications": "",
                    "career_progression": "",
                    "reasoning": "Invalid format"
                }
            },
            {
                "name": "Missing Score",
                "response": '{"reasoning": "No score provided"}',
                "expected": {
                    "score": "", 
                    "technical_skills_match": "",
                    "experience_relevance": "",
                    "soft_skills_cultural_fit": "",
                    "education_certifications": "",
                    "career_progression": "",
                    "reasoning": "No score provided"
                }
            },
            {
                "name": "Missing Reasoning",
                "response": '{"score": "85%"}',
                "expected": {
                    "score": "85%", 
                    "technical_skills_match": "",
                    "experience_relevance": "",
                    "soft_skills_cultural_fit": "",
                    "education_certifications": "",
                    "career_progression": "",
                    "reasoning": ""
                }
            }
        ]
        
        passed = 0
        total = len(test_cases)
        
        for test_case in test_cases:
            result = self.analyzer._extract_score_from_response(test_case["response"])
            if result == test_case["expected"]:
                print(f"✅ {test_case['name']}: PASS")
                passed += 1
            else:
                print(f"❌ {test_case['name']}: FAIL")
                print(f"   Expected: {test_case['expected']}")
                print(f"   Got: {result}")
        
        print(f"Invalid responses: {passed}/{total} passed")
        return passed == total
    
    def test_edge_cases(self):
        """Test extraction from edge cases"""
        print("\nTesting edge cases...")
        
        test_cases = [
            {
                "name": "Empty Response",
                "response": "",
                "expected": {"score": "", "reasoning": "No JSON found"}
            },
            {
                "name": "Malformed JSON",
                "response": '{"score": "85%", "reasoning": "Missing closing brace',
                "expected": {"score": "", "reasoning": "Error parsing AI response"}
            },
            {
                "name": "Nested JSON",
                "response": '{"data": {"score": "90%", "reasoning": "Nested"}}',
                "expected": {
                    "score": "", 
                    "technical_skills_match": "",
                    "experience_relevance": "",
                    "soft_skills_cultural_fit": "",
                    "education_certifications": "",
                    "career_progression": "",
                    "reasoning": ""
                }
            },
            {
                "name": "Multiple JSON Objects",
                "response": '{"score": "85%", "reasoning": "First"} {"score": "90%", "reasoning": "Second"}',
                "expected": {
                    "score": "85%", 
                    "technical_skills_match": "",
                    "experience_relevance": "",
                    "soft_skills_cultural_fit": "",
                    "education_certifications": "",
                    "career_progression": "",
                    "reasoning": "First"
                }
            }
        ]
        
        passed = 0
        total = len(test_cases)
        
        for test_case in test_cases:
            result = self.analyzer._extract_score_from_response(test_case["response"])
            if result == test_case["expected"]:
                print(f"✅ {test_case['name']}: PASS")
                passed += 1
            else:
                print(f"❌ {test_case['name']}: FAIL")
                print(f"   Expected: {test_case['expected']}")
                print(f"   Got: {result}")
        
        print(f"Edge cases: {passed}/{total} passed")
        return passed == total
    
    def test_prompt_structure(self):
        """Test that prompts are structured correctly"""
        print("\nTesting prompt structure...")
        
        # Test system prompt
        system_prompt = self.analyzer._create_system_prompt()
        
        # Test user prompt
        user_prompt = self.analyzer._create_user_prompt(
            resume_content="Test resume content",
            job_description="Test job description", 
            requirements="Test requirements",
            resume_url="https://example.com/resume.pdf"
        )
        
        # Check system prompt structure
        system_checks = [
            ("Contains analysis framework", "ANALYSIS FRAMEWORK" in system_prompt),
            ("Contains scoring criteria", "SCORING CRITERIA" in system_prompt),
            ("Contains response format", "RESPONSE FORMAT" in system_prompt),
            ("Contains score", "score" in system_prompt),
            ("Contains reasoning", "reasoning" in system_prompt)
        ]
        
        # Check user prompt structure
        user_checks = [
            ("Contains job description", "JOB DESCRIPTION:" in user_prompt),
            ("Contains job requirements", "JOB REQUIREMENTS:" in user_prompt),
            ("Contains resume content", "RESUME CONTENT:" in user_prompt),
            ("Contains resume source", "RESUME SOURCE:" in user_prompt)
        ]
        
        all_checks = system_checks + user_checks
        passed = sum(1 for _, check in all_checks if check)
        total = len(all_checks)
        
        for name, check in all_checks:
            status = "✅ PASS" if check else "❌ FAIL"
            print(f"   {name}: {status}")
        
        print(f"Prompt structure: {passed}/{total} checks passed")
        return passed == total

def main():
    """Run LLM response extraction tests"""
    tester = LLMResponseExtractionTester()
    
    print("🧪 LLM RESPONSE EXTRACTION TESTS")
    print("=" * 50)
    
    tests = [
        ("Valid Responses", tester.test_valid_responses),
        ("Invalid Responses", tester.test_invalid_responses), 
        ("Edge Cases", tester.test_edge_cases),
        ("Prompt Structure", tester.test_prompt_structure)
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