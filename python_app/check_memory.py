import psutil
import requests
import time

API_URL = "наш url"
MEMORY_USAGE_THRESHOLD = 90


def check_memory_usage():
    memory_percent = psutil.virtual_memory().percent

    return memory_percent


def send_alarm():
    try:
        response = requests.post(API_URL, json={"message": "Превышен порог памяти!"})
        response.raise_for_status()

        if response.status_code == 200:
            print("Alarm sent successfully!")
        else:
            print("Ошибка отправки уведомления!. Код ответа:", response.status_code)
    except Exception as e:
        print("Ошибка:", e)


def main():
    while True:
        memory_percent = check_memory_usage()
        print(f"Памяти использовано: {memory_percent} %")

        if memory_percent > MEMORY_THRESHOLD_PERCENT:
            send_alarm()

        time.sleep(60)


if __name__ == "__main__":
    main()
