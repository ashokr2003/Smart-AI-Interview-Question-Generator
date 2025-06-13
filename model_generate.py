# #model_generator
# import os
# import re
# from groq import Groq
# from dotenv import load_dotenv

# load_dotenv()

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))
# MODEL = os.getenv("GROQ_MODEL", "llama3-8b-8192")  # default model fallback

# def generate_questions(job_role, topic, keywords, num_questions=5):
#     prompt = (
#         f"Generate {num_questions} unique and relevant interview questions for a {job_role} role "
#         f"focused on {topic}. Use these keywords: {', '.join(keywords)}.\n"
#         f"Number each question in the format Q1, Q2, ..., Q{num_questions}. Only return questions. No explanations."
#     )

#     try:
#         response = client.chat.completions.create(
#             model=MODEL,
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.7,
#         )

#         content = response.choices[0].message.content.strip()
#         print("🧾 LLM Output:\n", content)

#         # Extract questions in order
#         pattern = r'^Q\d+[\.\:\-\)]\s*(.+)'

#         questions = re.findall(pattern, content, flags=re.MULTILINE)

#         # Return list of questions (no explanations)
#         return questions if questions else None

#     except Exception as e:
#         print(f"❌ Error generating questions: {e}")
#         return None

#model_generator
import os
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = os.getenv("GROQ_MODEL", "llama3-8b-8192")  # default model fallback

def generate_questions(job_role, topic, keywords, num_questions=5, difficulty="Intermediate"):
    prompt = (
        f"Generate {num_questions} unique and relevant interview questions for a {job_role} role "
        f"focused on {topic}. Use these keywords: {', '.join(keywords)}.\n"
        f"Use these keywords if relevant: {', '.join(keywords)}.\n"
        f"Only return the questions. No explanations. No numbering."
    )

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        content = response.choices[0].message.content.strip()
        print("🧾 LLM Output:\n", content)

        # Split lines, clean out empty lines and existing Q1/Q2/Q3 numbering if present
        raw_lines = content.split("\n")
        cleaned_questions = []
        for line in raw_lines:
            line = line.strip()
            if not line:
                continue
            # Remove leading Q1., Q2:, etc., if they exist
            match = re.match(r"^Q\d+[\.\:\-\)]\s*(.+)", line)
            question = match.group(1) if match else line
            cleaned_questions.append(question)

        return cleaned_questions[:num_questions] if cleaned_questions else None

    except Exception as e:
        print(f"❌ Error generating questions: {e}")
        return None

    # prompt = (
    #     f"Generate {num_questions} unique and relevant interview questions for a {job_role} role "
    #     f"focused on {topic}. Use these keywords: {', '.join(keywords)}.\n"
    #     f"Number each question in the format Q1, Q2, ..., Q{num_questions}. Only return questions. No explanations."
    # )

    # try:
    #     response = client.chat.completions.create(
    #         model=MODEL,
    #         messages=[{"role": "user", "content": prompt}],
    #         temperature=0.7,
    #     )

    #     content = response.choices[0].message.content.strip()
    #     print("🧾 LLM Output:\n", content)

    #     # Extract questions in order
    #     pattern = r'^Q\d+[\.\:\-\)]\s*(.+)'

    #     questions = re.findall(pattern, content, flags=re.MULTILINE)

    #     # Return list of questions (no explanations)
    #     return questions if questions else None

    # except Exception as e:
    #     print(f"❌ Error generating questions: {e}")
    #     return None

