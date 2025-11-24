from aws_cdk import (
    Stack,
    Duration,
    RemovalPolicy,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_s3_notifications as s3n,
)
from constructs import Construct


class LambdaCsvCopyStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Source bucket – odakle čita CSV
        src_bucket = s3.Bucket(
            self,
            "CsvSourceBucket",
            bucket_name="lazar-docker-source-bucket",
            versioned=False,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        # Destination bucket – gde upisuje CSV kopije
        dest_bucket = s3.Bucket(
            self,
            "CsvDestBucket",
            bucket_name="lazar-docker-dest-bucket",
            versioned=False,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        # Lambda funkcija iz Docker image-a
        fn = _lambda.DockerImageFunction(
            self,
            "CsvCopyFunction",
            code=_lambda.DockerImageCode.from_image_asset(
                directory="lambda_src",  # ovde su Dockerfile + app.py
            ),
            memory_size=512,
            timeout=Duration.seconds(30),
            environment={
                "DEST_BUCKET": dest_bucket.bucket_name,
                "DEST_PREFIX": "processed/",
            },
        )

        # Dozvole da čita i piše iz/na S3
        src_bucket.grant_read(fn)
        dest_bucket.grant_write(fn)

        # S3 -> Lambda trigger za .csv fajlove
        notification = s3n.LambdaDestination(fn)
        src_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            notification,
            s3.NotificationKeyFilter(suffix=".csv"),
        )

        from aws_cdk import CfnOutput
        CfnOutput(self, "SourceBucketName", value=src_bucket.bucket_name)
        CfnOutput(self, "DestBucketName", value=dest_bucket.bucket_name)

        # extra_layer = _lambda.LayerVersion(
        #     self,
        #     "ExtraLibLayer",
        #     code=_lambda.Code.from_asset("layer_src"),
        #     compatible_runtimes=[_lambda.Runtime.PYTHON_3_11],
        #     description="Extra library layer (e.g. python-dateutil)",
        #     removal_policy=RemovalPolicy.DESTROY,
        # )
        #
        # # Demo Lambda funkcija (ZIP), koja koristi layer
        # layer_demo_fn = _lambda.Function(
        #     self,
        #     "LayerDemoFunction",
        #     runtime=_lambda.Runtime.PYTHON_3_11,
        #     handler="handler.main",  # fajl handler.py, funkcija main
        #     code=_lambda.Code.from_asset("layer_demo_src"),
        #     layers=[extra_layer],
        #     timeout=Duration.seconds(10),
        #     memory_size=256,
        # )
