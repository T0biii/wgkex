FROM gcr.io/bazel-public/bazel:7.0.2 AS builder

WORKDIR /wgkex
COPY wgkex ./wgkex

RUN ["bazel", "build", "//wgkex/broker:app"]
RUN ["bazel", "build", "//wgkex/worker:app"]

FROM python:3.11.8-slim-bookworm
WORKDIR /wgkex

COPY --from=builder /wgkex/bazel-7.0.2 /wgkex/

COPY entrypoint /entrypoint

EXPOSE 5000

ENTRYPOINT ["/entrypoint"]
CMD ["broker"]
