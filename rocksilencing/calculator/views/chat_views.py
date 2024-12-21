import json
import time
import logging
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from g4f.client import Client

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class G4FBot:
    def __init__(self):
        try:
            logger.info("Initializing G4F Bot")
            self.client = Client()
            self.max_retries = 3
            self.retry_delay = 1
        except Exception as e:
            logger.error(f"Error initializing bot: {str(e)}")
            raise

    def clean_response(self, text):
        """Очистка ответа от лишних символов форматирования"""
        # Удаляем HTML-теги
        text = re.sub(r"<[^>]+>", "", text)
        # Удаляем специальные символы Markdown
        text = re.sub(r"[*_`]", "", text)
        # Удаляем escape-последовательности
        text = text.replace("\\n", "\n").replace("\\t", "\t")
        # Удаляем множественные пробелы
        text = re.sub(r"\s+", " ", text)
        # Удаляем специфические артефакты
        text = re.sub(r"_[a-z]+_", "", text)
        text = re.sub(r"<code.*?</code>", "", text)
        text = re.sub(r"<em.*?</em>", "", text)
        # Очищаем начало и конец строки
        text = text.strip()
        return text

    def get_response(self, message):
        """Основной метод получения ответа с повторными попытками"""
        retries = 0
        while retries < self.max_retries:
            try:
                logger.info(f"Sending message to G4F: {message}")
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": message}],
                    temperature=0.7,
                    max_tokens=1000,
                )
                response_text = response.choices[0].message.content
                # Очищаем ответ перед логированием
                cleaned_response = self.clean_response(response_text)
                logger.info(f"Received response from G4F: {cleaned_response}")
                return cleaned_response
            except Exception as e:
                retries += 1
                if retries == self.max_retries:
                    error_msg = f"Error getting response from G4F after {self.max_retries} attempts: {str(e)}"
                    logger.error(error_msg)
                    return f"Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже. {str(e)}"
                logger.warning(
                    f"Attempt {retries} failed. Retrying in {self.retry_delay} seconds..."
                )
                time.sleep(self.retry_delay)


@csrf_exempt
def chat_api(request):
    logger.info(f"Received {request.method} request to chat_api")

    if request.method == "POST":
        try:
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                logger.error("Invalid JSON received")
                return JsonResponse(
                    {"status": "error", "message": "Неверный формат JSON"}, status=400
                )

            user_message = data.get("message", "").strip()
            if not user_message:
                logger.warning("Empty message received")
                return JsonResponse(
                    {"status": "error", "message": "Сообщение не может быть пустым"},
                    status=400,
                )

            bot = G4FBot()
            response_text = bot.get_response(user_message)

            if "Произошла ошибка" in response_text:
                return JsonResponse(
                    {"status": "error", "message": response_text}, status=500
                )

            return JsonResponse({"status": "success", "response": response_text})

        except Exception as e:
            logger.error(f"Unexpected error in chat_api: {str(e)}")
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse(
        {"status": "error", "message": "Метод не поддерживается"}, status=405
    )
