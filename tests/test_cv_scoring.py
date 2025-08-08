import json
from typing import Dict, List
from src.ai.resume_analyzer import ResumeAnalyzer
from src.utils.logger import setup_logger

class CVScoringTester:
    """Test CV scoring accuracy with different scenarios"""
    
    def __init__(self):
        self.analyzer = ResumeAnalyzer()
        self.logger = setup_logger("cv_scoring_test")
        
        # Test job details (Software Engineer position)
        self.job_description = """
        We are looking for a Software Engineer to join our development team.
        You will be responsible for developing and maintaining web applications,
        working with modern technologies like Python, JavaScript, and React.
        You will collaborate with cross-functional teams to deliver high-quality software.
        """
        
        self.job_requirements = """
        - 2+ years of experience in software development
        - Proficiency in Python and JavaScript
        - Experience with React or similar frontend frameworks
        - Knowledge of databases (SQL/NoSQL)
        - Understanding of REST APIs
        - Git version control
        - Agile development methodologies
        """
    
    def create_test_cv(self, cv_type: str) -> str:
        """Create test CV content based on type"""
        cvs = {
            "perfect_fit": """
            SOFTWARE ENGINEER
            John Doe
            john.doe@email.com | +1-555-0123
            
            EXPERIENCE
            Software Engineer at TechCorp (2022-Present)
            - Developed full-stack web applications using Python, JavaScript, and React
            - Built REST APIs and integrated with SQL and MongoDB databases
            - Collaborated with cross-functional teams using Agile methodologies
            - Used Git for version control and code management
            - Improved application performance by 40%
            
            Software Developer at StartupXYZ (2021-2022)
            - Created responsive web applications with React and Node.js
            - Implemented database schemas and optimized queries
            - Worked in Agile environment with daily standups
            
            SKILLS
            - Python, JavaScript, React, Node.js
            - SQL, MongoDB, PostgreSQL
            - REST APIs, GraphQL
            - Git, Docker, AWS
            - Agile, Scrum, JIRA
            
            EDUCATION
            Bachelor of Science in Computer Science
            University of Technology (2021)
            """,
            
            "partial_fit": """
            SOFTWARE DEVELOPER
            Jane Smith
            jane.smith@email.com | +1-555-0456
            
            EXPERIENCE
            Junior Developer at SmallTech (2023-Present)
            - Built basic web applications using HTML, CSS, and JavaScript
            - Worked with simple databases and basic APIs
            - Assisted senior developers with code reviews
            
            SKILLS
            - HTML, CSS, JavaScript (basic)
            - Python (beginner level)
            - Basic understanding of databases
            - Some experience with Git
            
            EDUCATION
            Associate Degree in Information Technology
            Community College (2023)
            """,
            
            "irrelevant": """
            EXECUTIVE CHEF
            Chef Michael Johnson
            chef.michael@restaurant.com | +1-555-0789
            
            EXPERIENCE
            Head Chef at Gourmet Restaurant (2018-Present)
            - Managed kitchen staff of 15 people
            - Created seasonal menus and managed food costs
            - Oversaw food safety and quality standards
            - Trained junior chefs in culinary techniques
            
            Sous Chef at Fine Dining (2015-2018)
            - Prepared high-end dishes and managed kitchen operations
            - Coordinated with front-of-house staff
            - Maintained inventory and supplier relationships
            
            SKILLS
            - French, Italian, and Asian cuisines
            - Menu planning and cost management
            - Kitchen management and staff training
            - Food safety and sanitation
            - Wine pairing and beverage management
            
            EDUCATION
            Culinary Arts Degree
            Institute of Culinary Education (2015)
            """,
            
            "overqualified": """
            SENIOR SOFTWARE ENGINEER
            Dr. Sarah Chen
            sarah.chen@tech.com | +1-555-0321
            
            EXPERIENCE
            Senior Software Engineer at BigTech (2018-Present)
            - Led development of large-scale distributed systems
            - Architected microservices using Kubernetes and Docker
            - Mentored 10+ junior developers and conducted technical interviews
            - Implemented CI/CD pipelines and DevOps practices
            - Reduced system latency by 60% through optimization
            
            Principal Engineer at StartupUnicorn (2015-2018)
            - Built scalable backend systems handling 1M+ users
            - Designed database architectures and data pipelines
            - Led technical decisions and architecture reviews
            - Managed team of 8 engineers
            
            Senior Developer at TechGiant (2012-2015)
            - Developed enterprise applications and APIs
            - Led code reviews and technical discussions
            - Mentored junior developers and conducted training sessions
            
            SKILLS
            - Python, Java, Go, JavaScript, TypeScript
            - React, Angular, Vue.js, Node.js
            - Kubernetes, Docker, AWS, GCP, Azure
            - Microservices, REST APIs, GraphQL, gRPC
            - SQL, NoSQL, Redis, Elasticsearch
            - CI/CD, DevOps, Terraform, Ansible
            - System design, architecture, performance optimization
            - Team leadership, mentoring, technical interviewing
            
            EDUCATION
            Ph.D. in Computer Science - Stanford University (2012)
            Master of Science in Computer Science - MIT (2010)
            Bachelor of Science in Computer Science - UC Berkeley (2008)
            """
        }
        
        return cvs.get(cv_type, "")
    
    def test_cv_scoring(self) -> Dict[str, Dict]:
        """Run comprehensive CV scoring tests"""
        results = {}
        
        test_cases = [
            ("perfect_fit", "Perfect Fit CV", "90%", "100%"),  # Should score >90%
            ("overqualified", "Overqualified CV", "OVERQUALIFIED", "OVERQUALIFIED"), # Should return OVERQUALIFIED
            ("partial_fit", "Partial Fit CV", "50%", "70%"),   # Should score 50-70%
            ("irrelevant", "Irrelevant CV", "0%", "20%"),     # Should score <20%
        ]
        
        for cv_type, description, min_expected, max_expected in test_cases:
            self.logger.info(f"\n{'='*50}")
            self.logger.info(f"Testing: {description}")
            self.logger.info(f"Expected Score Range: {min_expected}-{max_expected}")
            self.logger.info(f"{'='*50}")
            
            cv_content = self.create_test_cv(cv_type)
            if not cv_content:
                self.logger.error(f"No CV content found for type: {cv_type}")
                continue
            
                         try:
                 result = self.analyzer.analyze_resume(
                     resume_content=cv_content,
                     job_description=self.job_description,
                     requirements=self.job_requirements,
                     resume_url=f"test://{cv_type}_cv.pdf"
                 )
                 
                 # Determine if score is within expected range
                 score_value = result['score']
                if min_expected == "OVERQUALIFIED" and max_expected == "OVERQUALIFIED":
                    is_in_range = score_value == "OVERQUALIFIED"
                else:
                    # Extract percentage numbers for comparison
                    score_num = int(score_value.replace('%', '')) if score_value != "OVERQUALIFIED" else 0
                    min_num = int(min_expected.replace('%', ''))
                    max_num = int(max_expected.replace('%', ''))
                    is_in_range = min_num <= score_num <= max_num
                
                status = "✅ PASS" if is_in_range else "❌ FAIL"
                
                result = {
                    "score": score_value,
                    "reasoning": result.get('reasoning', 'No reasoning'),
                    "expected_range": f"{min_expected}-{max_expected}",
                    "is_in_range": is_in_range,
                    "status": status,
                    "cv_type": cv_type,
                    "description": description
                }
                
                results[cv_type] = result
                
                                 self.logger.info(f"Actual Score: {score_value}")
                 self.logger.info(f"Status: {status}")
                 
                 if not is_in_range:
                     self.logger.warning(f"Score {score_value} is outside expected range {min_expected}-{max_expected}")
                
            except Exception as e:
                self.logger.error(f"Error testing {cv_type}: {e}")
                results[cv_type] = {
                    "score": None,
                    "error": str(e),
                    "status": "❌ ERROR",
                    "cv_type": cv_type,
                    "description": description
                }
        
        return results
    
    def generate_report(self, results: Dict[str, Dict]) -> str:
        """Generate a comprehensive test report"""
        report = []
        report.append("🔍 CV SCORING TEST REPORT")
        report.append("=" * 50)
        
        total_tests = len(results)
        passed_tests = sum(1 for r in results.values() if r.get("status") == "✅ PASS")
        failed_tests = sum(1 for r in results.values() if r.get("status") == "❌ FAIL")
        error_tests = sum(1 for r in results.values() if r.get("status") == "❌ ERROR")
        
        report.append(f"Total Tests: {total_tests}")
        report.append(f"Passed: {passed_tests}")
        report.append(f"Failed: {failed_tests}")
        report.append(f"Errors: {error_tests}")
        report.append(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        report.append("")
        
        for cv_type, result in results.items():
            report.append(f"📋 {result['description']}")
            report.append(f"   Type: {cv_type}")
            report.append(f"   Score: {result.get('score', 'N/A')}")
            report.append(f"   Expected: {result.get('expected_range', 'N/A')}")
            report.append(f"   Status: {result['status']}")
            
            if result.get("error"):
                report.append(f"   Error: {result['error']}")
            
            report.append("")
        
        return "\n".join(report)

def main():
    """Run CV scoring tests"""
    tester = CVScoringTester()
    
    print("Starting CV Scoring Tests...")
    print("This will test AI scoring accuracy with different CV types.")
    print("Note: This will use OpenAI API calls and may incur costs.\n")
    
    results = tester.test_cv_scoring()
    report = tester.generate_report(results)
    
    print("\n" + "="*60)
    print(report)
    print("="*60)
    
    # Save detailed results to file
    with open("cv_scoring_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed results saved to: cv_scoring_results.json")

if __name__ == "__main__":
    main() 