FROM golang:1.18-alpine as build

WORKDIR /app

COPY go.mod ./
COPY go.sum ./

RUN go mod download

COPY ./*.go ./
COPY ./src ./src
COPY ./pkg ./pkg

RUN go build -o /collector

FROM alpine:3.14.1

WORKDIR /usr/app

COPY --from=build /collector /collector

ENTRYPOINT ["/collector"]