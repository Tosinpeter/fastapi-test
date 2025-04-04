bind = "0.0.0.0:8000"
workers = 4  # Adjust this based on CPU cores
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
