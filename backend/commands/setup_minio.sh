#!/bin/sh

echo "Waiting for MinIO to be ready..."
sleep 5

echo "Configuring MinIO Client..."
mc alias set minio http://"$MINIO_HOST""$MINIO_ADDRESS" "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD"

if mc ls minio | grep -q "${MINIO_BUCKET_NAME}"; then
    echo "Bucket '${MINIO_BUCKET_NAME}' already exists. Skipping creation."
else
    echo "Creating bucket: ${MINIO_BUCKET_NAME}"
    mc mb minio/"${MINIO_BUCKET_NAME}"
fi

echo "Setting bucket policy to public..."
mc anonymous set download minio/"${MINIO_BUCKET_NAME}"

echo "Getting policy info..."
mc anonymous get minio/"${MINIO_BUCKET_NAME}"

echo "MinIO configuration completed!"
exit 0
