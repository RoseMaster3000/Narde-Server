# Overview

This is the dedicated server source code for the [Narde Unity Game](https://github.com/liormushiev/Narde).

# Setup

### Download
If you have not already, install the following
* Install Python `paru python` or download [here](https://www.python.org/downloads/)
* Install git `paru git` or download [here](https://git-scm.com/downloads)
* Install git LFS `paru git-lfs` or download [here](https://git-lfs.github.com/)
* Clone this repo `git clone git@github.com:RoseMaster3000/Narde-Server.git`

### Install
1. First time setup `source setup.sh`
2. Run `source test.sh` for development
3. Run `source run.sh` for production

### Testing with Postman
1. Install Postman `paru postman-bin` or download [here](https://www.postman.com/downloads/)
2. From `Workspaces`, click `New` in the left side-bar
3. Choose `Websocket Request`
4. Change dropdown from `Raw` to `Socket.io`
5. Connect, test events, etc.

# Server Deployment
### Initialization
1. Proofread `deploy/narde.service`, modify as needed
2. Install Gunicorn service `source deploy/gunicorn.sh`
3. Proofread `deploy/nginx.conf`, modify as needed
4. Install NginX with `source deploy/nginx.sh`
5. (optional) Install SSL (https://) with `source deploy/certbot.sh`
6. (optional) Install Firewall with `source deploy/firewall.sh`

### Maintenance
* Start Server `source deploy/start.sh`
* Stop Server `source deploy/stop.sh`
* Update server `source deploy/update.sh`

### VPS Providers
* PythonAnywhere does not [support Socket.io](https://www.pythonanywhere.com/forums/topic/27932/)
* Low End [Hostinger](https://www.hostinger.com/vps-hosting) ($4/month)
* High End [Google Cloud Platform](https://console.cloud.google.com/) ($30+/month)

# Credits

### Documentation
* [Python Socket.io - Transport Protocol](https://python-socketio.readthedocs.io/en/latest/server.html) 
* [SQLite3 - Database](https://docs.python.org/3/library/sqlite3.html)
* [TrueSkill - Matchmaking Algorithm](https://trueskill.org/)
* [Uvicorn - ASGI Server](https://www.uvicorn.org/)
* [Gunicorn - WSGI Server](https://docs.gunicorn.org/en/stable/design.html)
* [NginX - Reverse Proxy Server](https://socket.io/docs/v3/reverse-proxy/#nginx) 

### Author
| Shahrose Kasim |             |
|----------------|-------------|
|*[shahros3@gmail.com](mailto:shahros3@gmail.com)*|[shahrose.com](http://shahrose.com)|
|*[rosemaster3000@gmail.com](mailto:rosemaster3000@gmail.com)*|[florasoft.live](https://florasoft.live) |
|*[RoseMaster#3000](https://discordapp.com/users/122224041296789508)*|[discord.com](https://discord.com/)|