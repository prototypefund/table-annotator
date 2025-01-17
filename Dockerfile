# pull official base image
FROM node:16.13-alpine3.14

WORKDIR app

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# install app dependencies
COPY package.json yarn.lock /app/
RUN yarn install --silent --non-interactive

# add app
COPY tsconfig.json /app/
COPY src /app/src/
COPY public /app/public/

# start app
CMD ["yarn", "start"]