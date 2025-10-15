## Setup for DAGs using GCP/AWS Operator/Hook

- Run [LocalStack](https://github.com/localstack/localstack) with docker

```shell
docker compose -f docker-compose.localstack.yaml up -d
```

### LocalStack

The following resources are created when starting LocalStack.

- S3 bucket name: `sample-bucket`
- SNS topic name: `sample-topic`

### Airflow

#### Variables

- [gcp](../../config/gcp.json)
- [aws](../../config/aws.json)

```shell

docker compose run --rm airflow-cli variables import config/gcp.json
docker compose run --rm airflow-cli variables import config/aws.json
```

#### Connection GCP

- gcp_default

| Command               | Description                                                                                                                                 |
|-----------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| Connection Id         | gcp_default                                                                                                                                 |
| Connection Type       | Google Cloud Platform                                                                                                                    |
| Description           |                                                                                                                                             |
| GCP Access Key ID     |                                                                                                                                             |
| GCP Secret Access Key |                                                                                                                                             |
| Extra                 | {"gcp_access_key_id": "dummy", "gcp_secret_access_key": "dummy", "region_name": "ap-northeast-1", "endpoint_url": "http://localstack:4566"} |

```shell
docker compose run --rm airflow-cli connections add 'gcp_default' \
    --conn-json '{
      "conn_type": "Google Cloud Platform",
      "extra": {
        "gcp_access_key_id": "dummy",
        "gcp_secret_access_key": "dummy",
        "region_name": "ap-northeast-1",
        "endpoint_url": "http://localstack:4566"
      }
    }'
```

#### Connection AWS

- aws_default

| Command               | Description                                                                                                                                 |
|-----------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| Connection Id         | aws_default                                                                                                                                 |
| Connection Type       | Amazon Web Services                                                                                                                         |
| Description           |                                                                                                                                             |
| AWS Access Key ID     |                                                                                                                                             |
| AWS Secret Access Key |                                                                                                                                             |
| Extra                 | {"aws_access_key_id": "dummy", "aws_secret_access_key": "dummy", "region_name": "ap-northeast-1", "endpoint_url": "http://localstack:4566"} |

```shell
docker compose run --rm airflow-cli connections add 'aws_default' \
    --conn-json '{
      "conn_type": "Amazon Web Services",
      "extra": {
        "aws_access_key_id": "dummy",
        "aws_secret_access_key": "dummy",
        "region_name": "ap-northeast-1",
        "endpoint_url": "http://localstack:4566"
      }
    }'
```
