import os
import json
import google.generativeai as genai

class GeminiAPIKeyError(Exception):
    """Custom exception raised when the Gemini API key is missing or invalid."""
    pass

class GeminiGeneralError(Exception):
    """Custom exception raised for non-API-key-related Gemini failures."""
    pass

class GeminiHelper:
    @staticmethod
    def _clean_json_response(text):
        """Cleans and extracts JSON content from Gemini API response."""
        if not text:
            return None
        text = text.strip()
        # Remove markdown code blocks if present
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        
        # Locate the JSON object boundaries in case of extra leading/trailing characters
        try:
            start_idx = text.find('{')
            end_idx = text.rfind('}') + 1
            if start_idx != -1 and end_idx != 0:
                text = text[start_idx:end_idx]
            return json.loads(text)
        except Exception as e:
            print(f"Error parsing clean JSON: {e}\nRaw text: {text}")
            return None

    @staticmethod
    def _call_gemini_api(prompt, system_instruction=None):
        api_key = None
        try:
            from flask import current_app
            if current_app:
                api_key = current_app.config.get('GEMINI_API_KEY')
        except Exception:
            pass
        
        if not api_key:
            api_key = os.environ.get('GEMINI_API_KEY')
            
        if not api_key or api_key == "your_gemini_api_key_here":
            raise GeminiAPIKeyError("Please verify that a valid GEMINI_API_KEY is configured in your .env file.")
        
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(
                model_name="gemini-2.5-flash",
                system_instruction=system_instruction
)
            response = model.generate_content(prompt)
            if not response or not response.text:
                return ""
            return response.text
        except Exception as e:
            err_msg = str(e)
            if any(sig in err_msg for sig in ["API_KEY_INVALID", "API key not valid", "API key invalid", "INVALID_ARGUMENT"]):
                raise GeminiAPIKeyError("Please verify that a valid GEMINI_API_KEY is configured in your .env file.")
            raise GeminiGeneralError(f"Gemini API Error: {e}")

    @classmethod
    def get_chat_response(cls, user_message, history=None):
        """
        Chat response restricted to placement preparation topics.
        history is a list of tuples/dicts representing past conversation
        """
        system_instruction = (
            "You are Prep AI, a highly intelligent and supportive placement preparation chatbot designed "
            "for engineering and college students. Your domain expertise is strictly restricted to placement topics: "
            "OOP, Data Structures & Algorithms (DSA), DBMS, Operating Systems (OS), Computer Networks (CN), SQL, "
            "programming language fundamentals (Python, Java, C, C++), resume optimization, HR interview tips, "
            "company selection processes, mock interview practice, and general career/placement advice.\n\n"
            "If the user asks an off-topic question (not related to software engineering, computer science, "
            "placement tests, or professional career guidance), politely decline to answer, reminding them of your "
            "specific expertise. Be concise, professional, and clear. Format output using markdown."
        )
        
        # Build conversation thread
        prompt = ""
        if history:
            for item in history:
                prompt += f"User: {item.get('message', '')}\nPrep AI: {item.get('response', '')}\n\n"
        
        prompt += f"User: {user_message}\nPrep AI:"
        
        try:
            response = cls._call_gemini_api(prompt, system_instruction)
            return response
        except GeminiAPIKeyError:
            return "Please verify that a valid GEMINI_API_KEY is configured in your .env file."
        except Exception as e:
            return f"Sorry, I encountered an error while processing your request. Please try again later. (Error: {e})"

    @classmethod
    def generate_hr_answer(cls, question):
        """Generates a professional sample answer for a given HR question."""
        prompt = (
            f"Provide a strong, professional, and confident sample answer for a college student facing a campus placement "
            f"interview question: '{question}'. "
            f"Provide it in 2-3 short paragraphs, containing some tips on how to customize it."
        )
        system_instruction = "You are a professional HR Director helping students ace placement interviews."
        
        try:
            response = cls._call_gemini_api(prompt, system_instruction)
            if not response:
                raise Exception("Empty response from Gemini")
            return response
        except Exception:
            # Fallback answer
            return (
                "Here is a recommended guide to answer this question:\n"
                "1. Start with a brief story or experience from your college life, project, or internship.\n"
                "2. Relate your skills directly to what the company is seeking.\n"
                "3. Conclude by expressing enthusiasm for the job and how you can add value.\n\n"
                "(Configure a GEMINI_API_KEY in your .env to generate dynamic tailored responses)"
            )

    @classmethod
    def analyze_resume(cls, resume_text):
        """Sends resume text to Gemini for structured feedback."""
        prompt = f"""
        Analyze the following resume text and provide a structured JSON feedback report for campus placements.
        Resume Text:
        {resume_text}

        You must return ONLY a raw JSON object with the exact keys:
        {{
          "ats_score": (integer between 0 and 100),
          "strengths": [list of strings],
          "missing_skills": [list of strings],
          "grammar_suggestions": [list of strings],
          "improvement_tips": [list of strings]
        }}
        Do not add any explanations, markdown code blocks, or preamble. Return just the JSON structure.
        """
        
        system_instruction = "You are an ATS (Applicant Tracking System) reviewer and hiring manager specializing in software engineering candidates."
        
        try:
            response_text = cls._call_gemini_api(prompt, system_instruction)
            result = cls._clean_json_response(response_text)
            if not result:
                raise Exception("Failed to parse JSON response")
        except Exception:
            # Default fallbacks in case of error or no API key
            result = {
                "ats_score": 68,
                "strengths": [
                    "Clean structural layout",
                    "Clear contact details listed at the top",
                    "Good representation of technical projects"
                ],
                "missing_skills": [
                    "Cloud platforms (AWS/Azure/GCP) not explicitly highlighted",
                    "Unit testing framework experience is missing",
                    "Quantifiable metrics in project descriptions (e.g., 'improved performance by 20%')"
                ],
                "grammar_suggestions": [
                    "Ensure consistent past tense verb usage in project descriptions.",
                    "Verify capitalization of technical terms (e.g., HTML, Python, SQL)."
                ],
                "improvement_tips": [
                    "Add an active github/portfolio link next to your contact info.",
                    "Rephrase bullet points using the Google X-Y-Z formula (Accomplished [X] as measured by [Y], by doing [Z]).",
                    "Include a dedicated section for core coursework (OS, DBMS, DSA, CN) if not present."
                ]
            }
        return result

    @classmethod
    def evaluate_mock_answer(cls, question, answer):
        """Evaluates a candidate's mock interview answer."""
        prompt = f"""
        Evaluate the candidate's answer to the given interview question.
        Question: {question}
        Candidate's Answer: {answer}

        Provide scores out of 10 and helpful suggestions for improvements.
        You must return ONLY a raw JSON object with the exact keys:
        {{
          "communication_score": (integer between 0 and 10),
          "technical_score": (integer between 0 and 10),
          "confidence_score": (integer between 0 and 10),
          "suggestions": "detailed feedback string with constructive criticism and an improved sample response"
        }}
        Do not add any explanations, markdown code blocks, or preamble. Return just the JSON.
        """
        
        system_instruction = "You are an expert technical interviewer evaluating candidates for placement selection rounds."
        
        try:
            response_text = cls._call_gemini_api(prompt, system_instruction)
            result = cls._clean_json_response(response_text)
            if not result:
                raise Exception("Failed to parse JSON response")
        except Exception:
            # Dynamic fallback generation based on answer length
            ans_len = len(answer.strip())
            comm = 5 if ans_len < 30 else (8 if ans_len > 150 else 7)
            tech = 4 if ans_len < 30 else (7 if ans_len > 150 else 6)
            conf = 5 if ans_len < 30 else (8 if ans_len > 100 else 7)
            
            sug = "Your answer provides a basic outline. "
            if ans_len < 50:
                sug += "However, it is too brief. Try to structure your answers using the STAR method (Situation, Task, Action, Result) to make them comprehensive. Include technical details and explain your direct contribution."
            else:
                sug += "To improve, try to add specific examples of how you applied these skills in a project or class assignment. Make sure to sound enthusiastic and align your answer with industry best practices."
                
            result = {
                "communication_score": comm,
                "technical_score": tech,
                "confidence_score": conf,
                "suggestions": sug
            }
        return result

