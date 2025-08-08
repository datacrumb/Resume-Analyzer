import openai
from typing import Optional
from ..utils.config import OPENAI_API_KEY, AI_MODEL, AI_MAX_TOKENS, AI_TEMPERATURE

class ResumeAnalyzer:
    """Handles AI analysis of resumes"""
    
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        openai.api_key = OPENAI_API_KEY
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
    
    def analyze_resume(self, resume_content: str, job_description: str, requirements: str, resume_url: str = None) -> dict:
        """
        Analyze resume using OpenAI and return score and reasoning as a dictionary
        
        Args:
            resume_content: Extracted resume content
            job_description: Job description from Jobs sheet
            requirements: Job requirements from Jobs sheet
            resume_url: Optional resume URL for context
            
        Returns:
            Dictionary with 'score' (percentage string or "OVERQUALIFIED") and 'reasoning'
        """
        system_prompt = self._create_system_prompt()
        user_prompt = self._create_user_prompt(resume_content, job_description, requirements, resume_url)
        
        try:
            response = self.client.chat.completions.create(
                model=AI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=AI_MAX_TOKENS,
                temperature=AI_TEMPERATURE
            )
            
            response_text = response.choices[0].message.content
            return self._extract_score_from_response(response_text)
            
        except Exception as e:
            print(f"Error analyzing resume with AI: {e}")
            return {"score": "", "reasoning": "Error analyzing resume"}
    
    def _create_system_prompt(self) -> str:
        """Create the system prompt with analysis instructions and framework"""
        
        return """You are an expert HR recruiter with 15+ years of experience in talent acquisition and resume evaluation. Your task is to conduct a comprehensive, unbiased analysis of resumes against job requirements and provide detailed assessments.

        ANALYSIS FRAMEWORK:

        1. **COMPREHENSIVE EVALUATION FRAMEWORK:**
        - **Technical Skills Match (25% weight)**: Evaluate hard skills, tools, technologies, and technical competencies
        - **Experience Relevance (25% weight)**: Assess industry experience, role progression, and project complexity
        - **Soft Skills & Cultural Fit (20% weight)**: Leadership, communication, teamwork, adaptability
        - **Education & Certifications (15% weight)**: Degree relevance, certifications, continuous learning
        - **Career Progression (15% weight)**: Growth trajectory, responsibility increases, achievements

        2. **DETAILED SCORING CRITERIA:**
        - **Exceptional Fit (90-100%)**: Perfect alignment with all requirements, exceeds expectations
        - **Strong Fit (75-89%)**: Meets most requirements with some exceeding expectations
        - **Good Fit (60-74%)**: Meets core requirements with minor gaps
        - **Partial Fit (40-59%)**: Meets some requirements but has significant gaps
        - **Weak Fit (20-39%)**: Limited alignment, major skill/experience gaps
        - **Poor Fit (0-19%)**: Minimal relevance, completely different field
        - **OVERQUALIFIED**: Significantly overqualified for the role level

        3. **BIAS MITIGATION REQUIREMENTS:**
        - Focus ONLY on skills, experience, and qualifications relevant to the job
        - Ignore personal characteristics, age indicators, or demographic information
        - Evaluate transferable skills from different industries
        - Consider non-traditional career paths and alternative education paths
        - Assess potential for growth and learning ability

        4. **DETAILED ANALYSIS REQUIREMENTS:**
        - **Skills Gap Analysis**: Identify specific missing skills and their importance
        - **Experience Level Assessment**: Compare candidate's experience to role requirements
        - **Achievement Evaluation**: Assess quantifiable accomplishments and impact
        - **Growth Potential**: Evaluate learning ability and career trajectory
        - **Risk Assessment**: Identify potential concerns or red flags

        5. **CONTEXTUAL FACTORS TO CONSIDER:**
        - Industry trends and evolving skill requirements
        - Remote work capabilities and adaptability
        - Cultural fit with company values and work environment
        - Geographic considerations if relevant
        - Salary expectations alignment (if mentioned)

        RESPONSE FORMAT:
        Provide your analysis in the following JSON structure:

                {
                    "score": "X%" or "OVERQUALIFIED",
                    "technical_skills_match": "X%",
                    "experience_relevance": "X%", 
                    "soft_skills_cultural_fit": "X%",
                    "education_certifications": "X%",
                    "career_progression": "X%",
                    "reasoning": "Concise explanation of the overall assessment, including key factors that influenced the decision (max 2-3 sentences)"
                }

        EXAMPLE RESPONSES:

                Strong Candidate:
                {
                    "score": "85%",
                    "technical_skills_match": "90%",
                    "experience_relevance": "85%",
                    "soft_skills_cultural_fit": "80%",
                    "education_certifications": "85%",
                    "career_progression": "80%",
                    "reasoning": "Candidate demonstrates strong alignment with role requirements with relevant experience and technical skills. Minor gaps can be addressed through training."
                }

                Overqualified Candidate:
                {
                    "score": "OVERQUALIFIED",
                    "technical_skills_match": "95%",
                    "experience_relevance": "100%",
                    "soft_skills_cultural_fit": "90%",
                    "education_certifications": "100%",
                    "career_progression": "100%",
                    "reasoning": "Candidate is significantly overqualified for this junior role. Their experience level suggests they would be better suited for senior positions."
                }

        IMPORTANT NOTES:
        - Be objective and evidence-based in your assessment
        - Consider both current capabilities and growth potential
        - Provide actionable insights for hiring decisions
        - Include specific examples from the resume to support your evaluation
        - Consider the candidate's potential for success in the role, not just current fit
        - If resume content is limited (e.g., image-based PDF), evaluate based on available information and note limitations in reasoning
"""

    def _create_user_prompt(self, resume_content: str, job_description: str, requirements: str, resume_url: str = None) -> str:
        """Create the user prompt with the actual data to analyze"""
        # Truncate resume content to avoid token limits
        max_resume_chars = 50000
        if len(resume_content) > max_resume_chars:
            resume_content = resume_content[:max_resume_chars] + "... [Content truncated for length]"
        
        # Check if resume content is limited
        content_warning = ""
        if "PDF Resume" in resume_content and ("Text extraction limited" in resume_content or "Error during text extraction" in resume_content):
            content_warning = "\n\nIMPORTANT: This resume appears to be a PDF with limited text extraction (likely contains images or complex formatting). Please evaluate based on available information and note the limitation in your reasoning."
        
        return f"""Please analyze this resume against the job requirements:

                JOB DESCRIPTION:
                {job_description}

                JOB REQUIREMENTS:
                {requirements}

                RESUME CONTENT:
                {resume_content}{content_warning}

                RESUME SOURCE: {resume_url if resume_url else "Not provided"}

                Please provide your analysis in the specified JSON format.
        """
    
    def _extract_score_from_response(self, response_text: str) -> dict:
        """Extract all scores and reasoning from AI JSON response"""
        import re
        import json
        
        try:
            # Find JSON in response - look for opening brace
            brace_start = response_text.find('{')
            if brace_start == -1:
                return {"score": "", "reasoning": "No JSON found"}
            
            # Find the matching closing brace
            brace_count = 0
            json_end = -1
            for i, char in enumerate(response_text[brace_start:], brace_start):
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        json_end = i + 1
                        break
            
            if json_end == -1:
                # Malformed JSON - no matching closing brace
                return {"score": "", "reasoning": "Error parsing AI response"}
            
            # Extract and clean JSON string
            json_str = response_text[brace_start:json_end]
            json_str = re.sub(r'```\w*\s*', '', json_str)
            
            # Parse JSON
            try:
                result = json.loads(json_str)
            except json.JSONDecodeError:
                return {"score": "", "reasoning": "Error parsing AI response"}
            
            # Extract all fields with detailed breakdown
            extracted_result = {}
            
            # Map AI response fields to our internal fields
            field_mapping = {
                'score': 'score',
                'technical_skills_match': 'technical_skills_match',
                'experience_relevance': 'experience_relevance',
                'soft_skills_cultural_fit': 'soft_skills_cultural_fit',
                'education_certifications': 'education_certifications',
                'career_progression': 'career_progression',
                'reasoning': 'reasoning'
            }
            
            # Extract and validate each field
            for ai_field, our_field in field_mapping.items():
                value = result.get(ai_field, '')
                if value:
                    # Validate percentage scores (except reasoning and OVERQUALIFIED)
                    if our_field != 'reasoning' and value != "OVERQUALIFIED":
                        if isinstance(value, str) and value.endswith('%'):
                            try:
                                percentage = int(value.replace('%', ''))
                                if 0 <= percentage <= 100:
                                    extracted_result[our_field] = value
                                else:
                                    extracted_result[our_field] = ''  # Invalid percentage
                            except ValueError:
                                extracted_result[our_field] = ''  # Invalid format
                        else:
                            extracted_result[our_field] = ''  # Not a percentage
                    else:
                        # Reasoning or OVERQUALIFIED - no validation needed
                        extracted_result[our_field] = value
                else:
                    extracted_result[our_field] = ''
            
            # Ensure we have at least score and reasoning
            if 'score' not in extracted_result:
                extracted_result['score'] = ''
            if 'reasoning' not in extracted_result:
                extracted_result['reasoning'] = ''
            
            return extracted_result
            
        except Exception as e:
            print(f"Error parsing response: {e}")
            return {"score": "", "reasoning": "Error parsing AI response"} 

if __name__ == "__main__":
    print('hello')