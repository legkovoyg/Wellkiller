import json
import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from g4f.client import Client

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class G4FBot:
    def __init__(self):
        try:
            logger.info("Initializing G4FBot")
            self.client = Client()
        except Exception as e:
            logger.error(f"Error initializing bot: {str(e)}")
            raise

    def get_response(self, message):
        try:
            logger.info(f"Sending message to G4F: {message}")

            response = self.client.chat.completions.create(
                model="gpt-4o-mini", messages=[{"role": "user", "content": message}]
            )

            response_text = response.choices[0].message.content
            logger.info(f"Received response from G4F: {response_text}")
            return response_text
        except Exception as e:
            logger.error(f"Error getting response from G4F: {str(e)}")
            return f"Произошла ошибка при обработке запроса: {str(e)}"


@csrf_exempt
def chat_api(request):
    logger.info(f"Received {request.method} request to chat_api")

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "").strip()

            if not user_message:
                return JsonResponse(
                    {"status": "error", "message": "Сообщение не может быть пустым"},
                    status=400,
                )

            bot = G4FBot()
            response_text = bot.get_response(user_message)

            return JsonResponse({"status": "success", "response": response_text})

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Неверный формат JSON"}, status=400
            )

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse(
        {"status": "error", "message": "Метод не поддерживается"}, status=405
    )
