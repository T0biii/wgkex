FROM gcr.io/bazel-public/bazel:7.0.2 AS builder

RUN apt-get update && apt-get install -y apt-transport-https curl gnupg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /wgkex

COPY BUILD WORKSPACE requirements.txt ./
COPY wgkex ./wgkex

RUN ["bazel-7.0.2", "build", "//wgkex/broker:app"]
RUN ["bazel-7.0.2", "build", "//wgkex/worker:app"]
RUN ["cp", "-rL", "bazel-bin", "bazel-7.0.2"]

FROM python:3.11.8-slim-bookworm
WORKDIR /wgkex

COPY --from=builder /wgkex/bazel-7.0.2 /wgkex/

COPY entrypoint /entrypoint

EXPOSE 5000

ENTRYPOINT ["/entrypoint"]
CMD ["broker"]
