from apscheduler.schedulers.background import BackgroundScheduler
from .alerts_cleanup import delete_expired_alerts
from .alerts_ingest import fetch_and_store_alerts

def start_scheduler():
  scheduler = BackgroundScheduler()
  scheduler.add_job(fetch_and_store_alerts, "interval", minutes=15)
  scheduler.add_job(delete_expired_alerts, "interval", hours=1)
  scheduler.start()