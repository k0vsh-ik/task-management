#!/bin/bash
set -euo pipefail

# ===============================
# Configuration
# ===============================
STACK_NAME="task-stack"
TEMPLATE_FILE="cloudformation.yml"
LOCALSTACK_CONTAINER="localstack-main"
BUCKET_NAME="task-frontend-bucket"
LAMBDA_NAME="task-backend-python-lambda"
FRONTEND_DIR="frontend"
DIST_DIR="$FRONTEND_DIR/dist"
CONTAINER_DIST_PATH="/tmp/dist"

# ===============================
# Start LocalStack
# ===============================
echo "🚀 Starting LocalStack..."
docker rm -f "$LOCALSTACK_CONTAINER" 2>/dev/null || true
docker run -d --name "$LOCALSTACK_CONTAINER" -p 4566:4566 \
    -e SERVICES=cloudformation,s3,lambda localstack/localstack

echo "⏳ Waiting for LocalStack to initialize..."
sleep 5

# ===============================
# Deploy CloudFormation stack (S3 bucket)
# ===============================
echo "📦 Deploying CloudFormation stack..."
docker cp "$TEMPLATE_FILE" "$LOCALSTACK_CONTAINER:/opt/code/localstack/"
docker exec "$LOCALSTACK_CONTAINER" awslocal cloudformation create-stack \
    --stack-name "$STACK_NAME" \
    --template-body "file:///opt/code/localstack/$TEMPLATE_FILE"

sleep 5

# ===============================
# Verify S3 bucket
# ===============================
echo "🔍 Verifying S3 bucket..."
docker exec "$LOCALSTACK_CONTAINER" awslocal s3 ls

# ===============================
# Create Python Lambda manually (for LocalStack)
# ===============================
echo "⚡ Creating Python Lambda manually..."
docker exec "$LOCALSTACK_CONTAINER" sh -c "\
echo 'def lambda_handler(event, context): return {\"statusCode\":200,\"body\":\"Hello from Python Lambda!\"}' > /tmp/lambda_function.py && \
zip /tmp/lambda.zip /tmp/lambda_function.py"

docker exec "$LOCALSTACK_CONTAINER" awslocal lambda create-function \
    --function-name "$LAMBDA_NAME" \
    --runtime python3.11 \
    --role arn:aws:iam::000000000000:role/lambda-role \
    --handler lambda_function.lambda_handler \
    --zip-file fileb:///tmp/lambda.zip || echo "⚠ Lambda already exists"

# Verify Lambda
echo "🔍 Verifying Lambda functions..."
docker exec "$LOCALSTACK_CONTAINER" awslocal lambda list-functions
docker exec "$LOCALSTACK_CONTAINER" awslocal lambda get-function --function-name "$LAMBDA_NAME"

# ===============================
# Build frontend
# ===============================
echo "🏗 Building frontend..."
cd "$FRONTEND_DIR" || { echo "❌ Folder $FRONTEND_DIR not found"; exit 1; }
npm install
npm run build
cd ..

# ===============================
# Copy dist/ to LocalStack container
# ===============================
echo "⬆ Copying dist/ to LocalStack container..."
docker cp "$DIST_DIR" "$LOCALSTACK_CONTAINER:$CONTAINER_DIST_PATH"

# ===============================
# Sync frontend files to S3
# ===============================
echo "⬆ Syncing frontend files to S3 bucket..."
docker exec "$LOCALSTACK_CONTAINER" awslocal s3 sync "$CONTAINER_DIST_PATH/" "s3://$BUCKET_NAME/" --delete

# ===============================
# Configure static website hosting
# ===============================
echo "🌐 Configuring S3 static website hosting..."
docker exec "$LOCALSTACK_CONTAINER" awslocal s3 website "s3://$BUCKET_NAME/" --index-document index.html

# ===============================
# Verify frontend availability
# ===============================
echo "🔍 Verifying frontend..."
docker exec "$LOCALSTACK_CONTAINER" curl -s "http://localhost:4566/$BUCKET_NAME/index.html" | head -n 10

echo "✅ CloudFormation, Lambda, and frontend successfully tested in LocalStack!"
echo "Frontend URL: http://localhost:4566/$BUCKET_NAME/index.html"
