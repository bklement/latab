FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y sudo curl git software-properties-common zsh gcc g++ build-essential && rm -rf /var/lib/apt/lists/*
RUN add-apt-repository ppa:deadsnakes/ppa && apt update && apt install -y python3.12 python3.12-dev && rm /usr/lib/python3.*/EXTERNALLY-MANAGED && update-alternatives --install /usr/bin/python3 python /usr/bin/python3.12 1 && update-alternatives --set python /usr/bin/python3.12 && rm -rf /var/lib/apt/lists/*
RUN useradd -m  -s /bin/zsh developer && usermod -aG sudo developer && echo "developer ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/developer && chmod 044 /etc/sudoers.d/developer
USER developer:developer
WORKDIR /home/developer
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" 
RUN echo "export PATH=$PATH:/home/developer/.local/bin" >> ~/.zshrc && echo "alias ll=\"ls -al\"" >> ~/.zshrc && echo "alias python=\"python3.12\"" >> ~/.zshrc
COPY --chown=developer:developer .gitconfig /home/developer/.gitconfig
COPY --chown=developer:developer .gitignore /home/developer/.gitignore
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12
RUN python3.12 -m pip install --upgrade pip
RUN python3.12 -m pip install numpy astropy twine build
