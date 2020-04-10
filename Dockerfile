FROM ruby:2.7-alpine
LABEL maintainer="Liran Tal <liran.tal@gmail.com>"
LABEL description="Travis CLI in a docker container"

# Install required deps and cleanup space afterwards
RUN apk add --no-cache build-base git && \
    gem install travis && \
    rm -rf /var/lib/apt/lists/* /var/cache/apk/* \
    /usr/lib/ruby/gems/*/cache/* && \
    gem cleanup

ENTRYPOINT ["travis"]
CMD ["--help"]