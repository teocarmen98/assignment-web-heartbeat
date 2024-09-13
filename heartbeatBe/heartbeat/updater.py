from apscheduler.schedulers.background import BackgroundScheduler
from .views import UrlAPIView

url_api_view = UrlAPIView()

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(url_api_view.refresh_data, 'interval', seconds=2 , max_instances=5)
    scheduler.start()