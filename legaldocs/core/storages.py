import os
import boto3
from botocore.client import Config
from storages.backends.s3boto3 import S3Boto3Storage

class CustomS3Boto3Storage(S3Boto3Storage):
    """
    Custom S3 storage backend that handles internal container-to-container calls
    via AWS_S3_ENDPOINT_URL_INTERNAL and public-facing URL generation via
    AWS_S3_ENDPOINT_URL to ensure signature matches client host header.
    """
    def __init__(self, *args, **kwargs):
        endpoint_url_internal = os.getenv('AWS_S3_ENDPOINT_URL_INTERNAL')
        if endpoint_url_internal:
            kwargs['endpoint_url'] = endpoint_url_internal
        super().__init__(*args, **kwargs)
        
        # Instantiate a separate client for generating public URLs
        self.public_client = None
        endpoint_url_public = os.getenv('AWS_S3_ENDPOINT_URL')
        if endpoint_url_internal and endpoint_url_public:
            self.public_client = boto3.client(
                's3',
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key,
                region_name=self.region_name,
                endpoint_url=endpoint_url_public,
                config=Config(signature_version='s3v4')
            )

    def url(self, name, parameters=None, expire=None, http_method=None):
        if self.public_client:
            if expire is None:
                expire = self.querystring_expire
            
            clean_name = self._normalize_name(name)
            params = {
                'Bucket': self.bucket_name,
                'Key': clean_name,
            }
            if parameters:
                params.update(parameters)
                
            return self.public_client.generate_presigned_url(
                'get_object',
                Params=params,
                ExpiresIn=expire,
                HttpMethod=http_method or 'GET'
            )
            
        return super().url(name, parameters, expire, http_method)
