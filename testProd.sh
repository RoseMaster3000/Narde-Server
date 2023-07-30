# How command appears in service file (/etc/systemd/system/narde.service)
/home/Narde-Server/virt/bin/gunicorn -k uvicorn.workers.UvicornWorker -w 1 -b localhost:8000 app:app