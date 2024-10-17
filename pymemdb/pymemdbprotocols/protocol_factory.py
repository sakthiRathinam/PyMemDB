from typing import Callable, Dict

from pymemdb.pymemdbprotocols.protocol_parsers import (
    array_parser,
    bulk_string_parser,
    number_parser,
    simple_error_parser,
    simple_string_parser,
)

PROTOCOL_FACTORY: Dict[str, Callable] = {
    "+": simple_string_parser,
    ":": number_parser,
    "$": bulk_string_parser,
    "*": array_parser,
    "-": simple_error_parser,
}


def check_write_permission(connection_string: str, container_name: str, test_blob_name: str = "test-blob.txt"):
    try:
    # Create the BlobServiceClient object using the connection string
            blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    
            # Create a container client
            container_client = blob_service_client.get_container_client(container_name)
    
            # Check if the container exists (you might want to skip this step if you're sure it exists)try:
                container_client.create_container()
            print(f"Container '{container_name}' created (it didn't exist).")
    except ResourceExistsError:
        print(f"Container '{container_name}' already exists.")

        # Upload a test blob to check write permission
        blob_client = container_client.get_blob_client(test_blob_name)

        # Upload some dummy data
        data = "This is a test to check write permissions."
        blob_client.upload_blob(data, overwrite=True)
        print(f"Write permission confirmed: '{test_blob_name}' was successfully uploaded.")

        # Optionally, delete the test blob afterward
        blob_client.delete_blob()
        print(f"Test blob '{test_blob_name}' deleted.")
    
        except ClientAuthenticationError:
            print("Authentication failed. Please check your connection string and permissions.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")