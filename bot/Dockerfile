FROM node:8-alpine

RUN apk update && apk upgrade \
 && apk add --no-cache git \
 && apk add --no-cache tzdata

RUN yarn global add coffee-script

WORKDIR /hubot
#COPY scripts/ scripts/
COPY package.json package.json

ENV HUBOT_LOG_LEVEL='debug'
ENV HUBOT_ADAPTER='rocketchat'
ENV HUBOT_NAME='dockerbot'
ENV ROCKETCHAT_URL='rocketchat:3000'
ENV ROCKETCHAT_ROOM=''
ENV LISTEN_ON_ALL_PUBLIC='true'
ENV RESPOND_TO_DM='true'
ENV ROCKETCHAT_USER='dockerbot'
ENV ROCKETCHAT_PASSWORD='dockerbot'
ENV ANNOUNCE_ALLOWED_ROOMS='all'
ENV COMMAND_ALLOWED_ROOMS='all'

RUN yarn install
CMD yarn start
