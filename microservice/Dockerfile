FROM rust as builder
WORKDIR /app
COPY Cargo.toml ./
COPY src ./src
RUN cargo build --release

FROM debian:bookworm-slim
WORKDIR /app
COPY --from=builder /app/target/release/microservice /usr/local/bin/microservice
EXPOSE 8080
CMD ["microservice"]
