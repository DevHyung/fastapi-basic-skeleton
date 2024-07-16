# fastapi-basic-skeleton
FastAPI basic skelecton 코드 <br>
- Pydantic V2 기준
- FastAPI 저자의 dir를 참고
- typing (python 3.9+) 사용

 
하였습니다.

---
# Env
> Python 3.11.x (3.9+ 추천)
---
# Usage 
```shell
$ git clone https://github.com/DevHyung/fastapi-basic-skeleton.git
$ pip install -r requirements.txt
```

# `.env` example
```
# Common ENV 
USER_ID=id_example
USER_PW=pw_exmaple

# Dev ENV 
DEV_URL=dev_url

# Prod ENV
PROD_URL=prod_url
```

# `streamlit` run example
```shell
#!/bin/bash
SCRIPT_PATH="main.py"

# 실행할 Streamlit 포트와 주소
PORT=40203
ADDRESS="0.0.0.0"

#nohup streamlit run $SCRIPT_PATH --server.port=$PORT --server.address=$ADDRESS > nohup.out 2>&1 &
streamlit run $SCRIPT_PATH --server.port=$PORT --server.address=$ADDRESS
echo "Streamlit server is running on http://$ADDRESS:$PORT"
```

# `ngrok` run example
```shell
$ ngrok http {PORT_HERE} --authtoken {TOKEN_HERE}
```

# `server` run example
```shell
$ nohup python main.py > ../logs/nohup.log 2>&1 &
```