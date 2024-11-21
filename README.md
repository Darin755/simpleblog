## Simple Blog

```docker-compose build```

```docker-compose up -d```

Point your browser to port 8080


## Testing

 - install python3

 - run ```pip3 install -r requirements.txt```

 - run ```python3 app.py```

 - deploy ```gunicorn app:app -b 0.0.0.0:5000 -w 5``` (This runs 5 instances of the program and then load balances)
