# how command appears in systemd.service file
/home/Narde-Server/virt/bin/gunicorn -k uvicorn.workers.UvicornWorker -w 1 -b localhost:8000 app:app