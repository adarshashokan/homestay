import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///homestay.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET = os.environ.get('JWT_SECRET', 'jwt-secret-key')
    S3_BUCKET = os.environ.get('S3_BUCKET', '')
    AWS_REGION = os.environ.get('AWS_REGION', 'ap-south-1')
