import aws_cdk as core
import aws_cdk.assertions as assertions

from lambda_csv_copy.lambda_csv_copy_stack import LambdaCsvCopyStack

# example tests. To run these tests, uncomment this file along with the example
# resource in lambda_csv_copy/lambda_csv_copy_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = LambdaCsvCopyStack(app, "lambda-csv-copy")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
