FROM node:12 AS builder
WORKDIR /out
COPY package.json .
COPY yarn.lock .
RUN yarn install
COPY . .
RUN yarn build

FROM nginx:1.19-alpine
COPY --from=builder /out/build /usr/share/nginx/html