FROM python

COPY --chown=vscode:vscode requirements.txt ./
RUN python3.12 -m pip install -r requirements.txt && sudo rm requirements.txt
