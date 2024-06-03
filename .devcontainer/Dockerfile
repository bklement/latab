FROM 442864304639.dkr.ecr.eu-west-1.amazonaws.com/python:latest

COPY --chown=vscode:vscode requirements.txt ./
RUN python3.12 -m pip install -r requirements.txt && sudo rm requirements.txt
