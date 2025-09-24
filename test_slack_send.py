from dotenv import load_dotenv; load_dotenv()
from deliver.slack import send_to_slack, review_card
import traceback

dummy = {"source":"reddit","title":"Button test","url":"https://reddit.com/r/programming/comments/abc123/test"}
blocks = review_card(dummy, "If you're hitting X, here’s a concrete fix.\n\n(One link max.)", interactive=True)
try:
    send_to_slack(blocks)
    print("sent")
except Exception as e:
    print("Error:", e)
    traceback.print_exc()
