# [LAN] Run with Gunicorn + Uvicorn workers
ip -4 addr | grep -oP '(?<=inet\s)\d+(\.\d+){3}' | sed 's/^/http:\/\//;s/$/:8080/'
source virt/bin/activate
gunicorn -k uvicorn.workers.UvicornWorker -w 1 -b 0.0.0.0:8080 app:app