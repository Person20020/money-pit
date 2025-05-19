#!/bin/bash
source /home/kojii/money-pit/venv/bin/activate
cd /home/kojii/money-pit/website
gunicorn -w 2 -b 127.0.0.1:2004 --access-logfile /home/kojii/money-pit/logs/access.log --error-logfile /home/kojii/money-pit/logs/error.log app:app