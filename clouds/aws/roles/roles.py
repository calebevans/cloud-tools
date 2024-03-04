import boto3
from simple_logger.logger import get_logger

LOGGER = get_logger(name=__name__)
DEFAULT_AWS_REGION = "us-east-1"


def iam_client(region=DEFAULT_AWS_REGION):
    """Creates an IAM client.

    Args:
        region (str, default: "us-east-1"): Region to use for session, a client is associated with a single region.

    Returns:
        botocore.client.IAM: Service client instance.

    """
    LOGGER.info(f"Creating IAM client using region {region}.")
    return boto3.client(service_name="iam", region_name=region)


def get_roles(client=None):
    """
    Get all IAM roles.

    Args:
        client (botocore.client.IAM, optional): A boto3 client for IAM. Defaults to None.

    Returns:
        List[Dict[Any, Any]]: A list of IAM roles
    """
    LOGGER.info("Retrieving all roles from IAM.")

    client = client or iam_client()

    response = client.list_roles(MaxItems=1000)
    roles = response["Roles"]
    is_truncated = response["IsTruncated"]
    marker = response.get("Marker", None)

    if not is_truncated:
        return roles

    while is_truncated:
        response = client.list_roles(Marker=marker, MaxItems=1000)
        roles.extend(response["Roles"])
        is_truncated = response["IsTruncated"]
        marker = response["Marker"]

    return roles


def create_or_update_role_policy(role_name, policy_name, policy_document, region=DEFAULT_AWS_REGION):
    """
    Create a new policy role or update an existing one.

    Args:
        role_name (str): role policy name
        policy_name (str): policy name
        policy_document (str): policy documents as Json file content
        region (str): aws region
    """
    client = iam_client(region=region)
    LOGGER.info(f"Create/Update role {role_name} for policy {policy_name} by documented policy.")
    client.put_role_policy(
        RoleName=role_name,
        PolicyName=policy_name,
        PolicyDocument=policy_document,
    )
