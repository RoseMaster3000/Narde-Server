# How command appears in service file (/etc/systemd/system/narde.service)
source virt/bin/activate
gunicorn -k uvicorn.workers.UvicornWorker -w 1 -b localhost:8080 app:app