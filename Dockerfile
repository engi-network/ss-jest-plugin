FROM docker.io/python:3.9

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key C99B11DEB97541F0
RUN apt-get -y update
RUN apt-get -yq install software-properties-common
RUN apt-get -y update
RUN apt-add-repository https://cli.github.com/packages
RUN apt-get -y update
RUN apt-get -yq install gh

RUN apt-get install -yq build-essential cmake pkg-config libicu-dev zlib1g-dev libcurl4-openssl-dev libssl-dev ruby-dev
RUN apt-get -y update
RUN gem install github-linguist

RUN apt-get -yq install apt-transport-https ca-certificates curl gnupg lsb-release
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \ 
    $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN apt-get -y update
RUN apt-get -yq install docker-ce docker-ce-cli containerd.io docker-compose-plugin

WORKDIR /code

COPY . .

RUN umask 077 && mkdir ~/.ssh && ssh-keyscan -H github.com > ~/.ssh/known_hosts
RUN --mount=type=ssh git clone git@github.com:engi-network/same-story-api
RUN pip install ./same-story-api
RUN --mount=type=ssh pip install -r requirements.txt