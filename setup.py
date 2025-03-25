from setuptools import setup, find_packages

setup(
    name="fastapi_author",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0,<0.69.0",
        "uvicorn>=0.15.0,<0.16.0",
        "sqlalchemy>=1.4.23,<1.5.0",
        "pydantic>=1.8.0,<2.0.0",
        "python-jose[cryptography]>=3.3.0,<3.4.0",
        "passlib[bcrypt]>=1.7.4,<1.8.0",
        "python-multipart>=0.0.5,<0.0.6",
        "psycopg2-binary>=2.9.1,<2.10.0",
        "python-dotenv>=0.19.0,<0.20.0",
        "starlette>=0.14.2,<0.15.0",
        "httpx>=0.23.0,<0.24.0",
        "requests>=2.26.0,<2.27.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.5,<6.3.0",
            "pytest-cov>=2.12.1,<2.13.0",
            "flake8>=3.9.2,<3.10.0",
            "black>=21.7b0,<21.8b0",
            "isort>=5.9.3,<5.10.0",
        ],
    },
    python_requires=">=3.8",
) 