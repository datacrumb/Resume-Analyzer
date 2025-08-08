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
        prompt = self._create_analysis_prompt(resume_content, job_description, requirements, resume_url)
        
        try:
            response = self.client.chat.completions.create(
                model=AI_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert HR recruiter who evaluates resumes objectively."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=AI_MAX_TOKENS,
                temperature=AI_TEMPERATURE
            )
            
            response_text = response.choices[0].message.content
            return self._extract_score_from_response(response_text)
            
        except Exception as e:
            print(f"Error analyzing resume with AI: {e}")
            return {"score": "", "reasoning": "Error analyzing resume"}
    
    def _create_analysis_prompt(self, resume_content: str, job_description: str, requirements: str, resume_url: str = None) -> str:
        """Create the analysis prompt for AI"""
        # Truncate resume content to avoid token limits (roughly 100,000 tokens max)
        max_resume_chars = 50000  # More conservative limit for very long resumes
        if len(resume_content) > max_resume_chars:
            resume_content = resume_content[:max_resume_chars] + "... [Content truncated for length]"
        
        # Check if resume content is limited (likely a PDF with images)
        content_warning = ""
        if "PDF Resume" in resume_content and ("Text extraction limited" in resume_content or "Error during text extraction" in resume_content):
            content_warning = "\n\nIMPORTANT: This resume appears to be a PDF with limited text extraction (likely contains images or complex formatting). Please evaluate based on available information and note the limitation in your reasoning."
        
        prompt = f"""
        You are an expert HR recruiter evaluating resumes for job positions. Please analyze this resume against the job requirements and provide a score in percentage.

        JOB DESCRIPTION:
        {job_description}

        JOB REQUIREMENTS:
        {requirements}

        RESUME CONTENT:
        {resume_content}{content_warning}
        """
        
        if resume_url:
            prompt += f"\nRESUME SOURCE: {resume_url}"
        
        prompt += """

        SCORING CRITERIA:
        - **Perfect Fit (>90%)**: Fully matches job requirements with relevant experience, skills, and qualifications
        - **Partial Fit (50-70%)**: Has some required skills but missing key qualifications or experience
        - **Poor Fit (20-49%)**: Limited relevant experience or skills, significant gaps
        - **Irrelevant (<20%)**: Completely unrelated field or experience, no transferable skills

        EVALUATION FACTORS:
        1. **Skills Match**: How well the candidate's skills align with job requirements
        2. **Experience Level**: Whether experience matches the role's seniority
        3. **Relevance**: How relevant the background is to the position
        4. **Qualifications**: Education and certifications alignment
        5. **Overqualification**: Whether the candidate is significantly overqualified

        Please provide your response in JSON format:
        {
            "score": "[percentage]%" or "OVERQUALIFIED",
            "reasoning": "[detailed explanation of the score]"
        }

        Example responses:
        {"score": "85%", "reasoning": "Strong match with required skills and experience level"}
        {"score": "OVERQUALIFIED", "reasoning": "Candidate has 15 years experience for a junior role"}
        """
        
        return prompt
    
    def _extract_score_from_response(self, response_text: str) -> dict:
        """Extract score and reasoning from AI JSON response"""
        import re
        import json
        
        try:
            # Use regex to find JSON object in the response
            json_pattern = r'\{[^{}]*"score"[^{}]*"reasoning"[^{}]*\}'
            match = re.search(json_pattern, response_text, re.DOTALL)
            
            if match:
                json_str = match.group(0)
                # Clean up the JSON string
                json_str = re.sub(r'```python\s*', '', json_str)
                json_str = re.sub(r'```json\s*', '', json_str)
                json_str = re.sub(r'```\s*', '', json_str)
                
                result = json.loads(json_str)
                
                # Validate the response
                if 'score' in result and 'reasoning' in result:
                    score = result['score']
                    reasoning = result['reasoning']
                    
                    # Validate score format
                    if score == "OVERQUALIFIED":
                        print("Candidate identified as OVERQUALIFIED")
                        return {"score": "OVERQUALIFIED", "reasoning": reasoning}
                    elif isinstance(score, str) and score.endswith('%'):
                        # Validate percentage
                        percentage_str = score.replace('%', '').strip()
                        try:
                            percentage = int(percentage_str)
                            if 0 <= percentage <= 100:
                                return {"score": score, "reasoning": reasoning}
                            else:
                                print(f"Invalid percentage: {percentage}")
                                return {"score": "", "reasoning": "Invalid score format"}
                        except ValueError:
                            print(f"Invalid percentage format: {score}")
                            return {"score": "", "reasoning": "Invalid score format"}
                    else:
                        print(f"Invalid score format: {score}")
                        return {"score": "", "reasoning": "Invalid score format"}
                else:
                    print("Missing score or reasoning in JSON response")
                    return {"score": "", "reasoning": "Missing required fields"}
            else:
                print("No JSON found in response")
                return {"score": "", "reasoning": "Could not parse AI response"}
                
        except (ValueError, IndexError, json.JSONDecodeError) as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Response text: {response_text}")
            return {"score": "", "reasoning": "Error parsing AI response"} 

if __name__ == "__main__":
    print('hello')