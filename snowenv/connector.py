import os
import snowflake.connector
from snowflake.connector import SnowflakeConnection
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def connect(
    account: str,
    user: str,
    password: str = None,
    private_key_path: str = None,
    private_key_passphrase: str = None,
    **kwargs,
) -> SnowflakeConnection:
    """Initiates Snowflake connection.

    Args:
        account (str): Account identifier.
        user (str): Username.
        password (str, optional): Password, if authenticating with password. Defaults to None.
        private_key_path (str, optional): Path to private key, if authenticating with a private key. Defaults to None.
        private_key_passphrase (str, optional): Passphrase to decrypt the private key, if authenticating with a private key. Defaults to None.
        kwargs: Any optional arguments for snowflake.connector.connect(), e.g. role, warehouse, database.

    Returns:
        SnowflakeConnection: Opened Snowflake connection.
    """

    connect_kwargs = {
        "account": account,
        "user": user,
        **kwargs,
    }

    if password:
        connect_kwargs["password"] = password
    elif private_key_path:
        private_key_path = os.path.expanduser(private_key_path)
        with open(private_key_path, "rb") as key:
            p_key = serialization.load_pem_private_key(
                key.read(),
                password=private_key_passphrase,
                backend=default_backend(),
            )
        connect_kwargs["private_key"] = p_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

    return snowflake.connector.connect(**connect_kwargs)
