FROM node:12.22-alpine
WORKDIR /usr/src/app
COPY package.json package-lock.json ./
RUN npm install && npm cache clean --force
ENV PATH /usr/src/app/node_modules/.bin:$PATH