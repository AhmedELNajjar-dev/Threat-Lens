import time
import groq
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL

client = Groq(api_key=GROQ_API_KEY)


def call_llm(prompt: str, max_retries: int = 5, initial_delay: float = 2.0) -> str:
    delay = initial_delay
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a cybersecurity malware analysis expert."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0
            )
            return response.choices[0].message.content
        except (groq.RateLimitError, groq.APIError) as e:
            if attempt == max_retries - 1:
                raise e
            print(f"[!] Groq API Rate Limit / Warning: {e}. Retrying in {delay:.1f}s (Attempt {attempt + 1}/{max_retries})...")
            time.sleep(delay)
            delay *= 2
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            print(f"[!] Groq API error: {e}. Retrying in {delay:.1f}s...")
            time.sleep(delay)
            delay *= 2

