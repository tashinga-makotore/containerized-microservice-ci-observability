import sys

import httpx


HEALTH_URL = "http://127.0.0.1:8000/health"
TIMEOUT_SECONDS = 5.0


def check_health():
    try:
        response = httpx.get(
            HEALTH_URL,
            timeout=TIMEOUT_SECONDS,
        )

        response.raise_for_status()

        data = response.json()

        if data.get("status") != "healthy":
            print(
                "[UNHEALTHY] Service responded, "
                "but health status is not healthy."
            )
            return False

        print(
            f"[HEALTHY] {HEALTH_URL} "
            f"returned HTTP {response.status_code}"
        )

        return True

    except httpx.RequestError as error:
        print(
            f"[UNHEALTHY] Could not connect to service: {error}"
        )
        return False

    except httpx.HTTPStatusError as error:
        print(
            "[UNHEALTHY] Service returned "
            f"HTTP {error.response.status_code}"
        )
        return False

    except ValueError:
        print(
            "[UNHEALTHY] Service returned invalid JSON."
        )
        return False


if __name__ == "__main__":
    is_healthy = check_health()

    if is_healthy:
        sys.exit(0)

    sys.exit(1)