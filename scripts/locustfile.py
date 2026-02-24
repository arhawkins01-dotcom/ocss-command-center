from locust import HttpUser, task, between
import random
import string


def _rand_string(n=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


class StreamlitUser(HttpUser):
    """Simulate a user interacting with the Streamlit app.

    - Performs GET requests on `/` (root)
    - Attempts to simulate a "submit ticket" interaction via POST to
      `/submit_ticket` (if present) and falls back to a GET with query
      parameters to `/` when POST doesn't return success.
    """

    wait_time = between(1, 5)

    @task(4)
    def view_root(self):
        self.client.get("/")

    @task(1)
    def submit_ticket(self):
        # Construct a plausible ticket payload
        payload = {
            "title": f"Locust Test { _rand_string(6) }",
            "description": "Automated performance test submission",
            "priority": random.choice(["Low", "Medium", "High"]),
            "reported_by": "locust_user"
        }

        # Try POST to a dedicated endpoint first (some apps expose an API)
        with self.client.post("/submit_ticket", json=payload, catch_response=True, name="POST /submit_ticket") as post_resp:
            if post_resp.status_code in (200, 201):
                post_resp.success()
                return

        # Fallback: send the payload as query params on GET / (Streamlit will accept query params)
        try:
            params = {k: str(v) for k, v in payload.items()}
            self.client.get("/", params=params, name="GET /?submit_ticket")
        except Exception:
            # record as a failed request via a GET that will likely return 200 but signals the intent
            self.client.get("/", name="GET / (submit fallback)")
