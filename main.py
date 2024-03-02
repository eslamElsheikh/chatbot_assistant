import os
from dotenv import load_dotenv
import google.generativeai as genai
from typing import List
import os
import google.generativeai as genai

load_dotenv()



THERAPIST_INTRO = """Your name is Dr. Sanchez. You are an expert in psychotherapy, especially DBT.
                      You hold all the appropriate medical licenses to provide advice.
                      You have been helping individuals with their stress, depression and anxiety for over 20 years.
                      From young adults to older people. Your task is now to give the best advice to individuals seeking help managing their symptoms.
                      You must ALWAYS ask questions BEFORE you answer so that you can better hone in on what the questioner is really trying to ask.
                      You must treat me as a mental health patient.
                      Your response format should focus on reflection and asking clarifying questions.
                      You may interject or ask secondary questions once the initial greetings are done.
                      Exercise patience."""


def initialize_model() -> genai.GenerativeModel:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    return genai.GenerativeModel("gemini-pro")


def construct_message(message: str, role: str = 'user') -> dict:
  return {
    'role': role,
    'parts': [
      {'text': message}
    ]
  }

def get_model_response(model: genai.GenerativeModel, conversation: List[dict]) -> dict:
  response = model.generate_content(conversation)
  response.resolve()

  return construct_message(response.text, 'model')

def print_conversation(conversation: List[dict]):
  for message in conversation:
    print(f"{message['role']}: {message['parts'][0]['text']}")
  print('-' * 20)

def main():
    model = initialize_model()
    conversation = [construct_message(THERAPIST_INTRO)]

    while True:
        response = get_model_response(model, conversation)
        conversation.append(response)
        print_conversation(conversation)

        user_input = input("> ")
        if user_input.lower() in ['quit', 'exit']:
            break

        conversation.append(construct_message(user_input))


if __name__ == "__main__":
    main()