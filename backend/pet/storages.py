import os

from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class PublicS3Storage(S3Boto3Storage):
    def url(self, name, parameters=None, expire=None):
        original_url = super().url(name, parameters=parameters, expire=expire)
        return original_url.replace(
            settings.STORAGES["default"]["OPTIONS"]["endpoint_url"],
            os.getenv("S3_PUBLIC_ENDPOINT"),
        )
