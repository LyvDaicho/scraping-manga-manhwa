from dotenv import load_dotenv
import os


def main() -> None:
    load_dotenv()
    log_level = os.getenv("LOG_LEVEL", "INFO")
    timeout = os.getenv("REQUEST_TIMEOUT", "15")

    print("Tracker lancé")
    print(f"LOG_LEVEL={log_level}")
    print(f"REQUEST_TIMEOUT={timeout}")


if __name__ == "__main__":
    main()