use axum::{
    extract::Json,
    response::{IntoResponse, Response},
    routing::post,
    Router,
};
use serde::{Deserialize, Serialize};
use std::net::SocketAddr;
use csv::WriterBuilder;
use tokio::net::TcpListener;
use tower_http::cors::{Any, CorsLayer};

#[derive(Debug, Deserialize, Serialize)]
struct Record {
    id: u32,
    title: String,
    description: String,
    status: String,
    created_at: String,
}

#[tokio::main]
async fn main() {
    // Configure CORS to allow all origins, methods, and headers (for testing)
    let cors = CorsLayer::new()
        .allow_origin(Any)
        .allow_methods(Any)
        .allow_headers(Any);

    // Build the application router
    let app = Router::new()
        .route("/convert", post(convert_to_csv))
        .layer(cors);

    let port = env::var("PORT").unwrap_or_else(|_| "8080".to_string());
    let addr: SocketAddr = format!("0.0.0.0:{}", port).parse().unwrap();
    println!("Server running on http://{}", addr);

    let listener = TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}

// Convert JSON records to CSV and return as attachment
async fn convert_to_csv(Json(records): Json<Vec<Record>>) -> Response {
    let mut wtr = WriterBuilder::new().from_writer(vec![]);

    for rec in records {
        wtr.serialize(rec).unwrap();
    }

    let data = String::from_utf8(wtr.into_inner().unwrap()).unwrap();

    (
        [
            (axum::http::header::CONTENT_TYPE, "text/csv"),
            (axum::http::header::CONTENT_DISPOSITION, "attachment; filename=\"data.csv\""),
        ],
        data,
    )
        .into_response()
}
