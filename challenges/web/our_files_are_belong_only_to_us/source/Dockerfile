FROM golang:1.15-alpine

WORKDIR /usr/local/go/src/
COPY ./main ./main
RUN cd main && go mod tidy && go mod vendor && go build -o magpiefs

FROM alpine:3.13.0
WORKDIR /app
COPY --from=0 /usr/local/go/src/main/magpiefs /app/magpiefs
COPY a_secret.bak /app/files/a_secret.bak
COPY ./files /app/files

RUN addgroup -S magpiegroup 
RUN adduser -S magpieuser -G magpiegroup
USER magpieuser

CMD ["/app/magpiefs", "/app/files"]
