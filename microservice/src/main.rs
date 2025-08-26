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

    let addr = SocketAddr::from(([127, 0, 0, 1], 8080));
    println!("Server running on http://{}", addr);

    // Bind TCP listener
    let listener = TcpListener::bind(addr).await.unwrap();

    // Start the Axum server
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
