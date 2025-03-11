from typing import Dict, Optional, Union

from snowflake.connector import connect
from snowflake.connector.connection import SnowflakeConnection

from semantic_model_generator.data_processing.data_types import FQNParts

def confirmFQNQuoting(fqn_part: str) -> str:
    if fqn_part[0] != '"':
        fqn_part = '"' + fqn_part
    end_idx = len(fqn_part)-1
    if fqn_part[end_idx] != '"':
        fqn_part = fqn_part + '"'
    return fqn_part

def create_fqn_table(fqn_str: str) -> FQNParts:
    # '.' characters in the table name throw off this check
    if fqn_str.count('"."') != 2:
        raise ValueError(
            "Expected to have a table fully qualified name following the {database}.{schema}.{table} format."
            + f"Instead found {fqn_str}"
        )
    database, schema, table = fqn_str.split('"."')
    database = confirmFQNQuoting(database)
    schema = confirmFQNQuoting(schema)
    table = confirmFQNQuoting(table)
    return FQNParts(
        database=database, schema_name=schema, table=table
    )


def create_connection_parameters(
    user: str,
    account: str,
    password: Optional[str] = None,
    host: Optional[str] = None,
    role: Optional[str] = None,
    warehouse: Optional[str] = None,
    database: Optional[str] = None,
    schema: Optional[str] = None,
    authenticator: Optional[str] = None,
    passcode: Optional[str] = None,
    passcode_in_password: Optional[bool] = None,
) -> Dict[str, Union[str, bool]]:
    connection_parameters: Dict[str, Union[str, bool]] = dict(
        user=user, account=account
    )
    if password:
        connection_parameters["password"] = password
    if role:
        connection_parameters["role"] = role
    if warehouse:
        connection_parameters["warehouse"] = warehouse
    if database:
        connection_parameters["database"] = database
    if schema:
        connection_parameters["schema"] = schema
    if authenticator:
        connection_parameters["authenticator"] = authenticator
    if host:
        connection_parameters["host"] = host
    if passcode:
        connection_parameters["passcode"] = passcode
    if passcode_in_password:
        connection_parameters["passcode_in_password"] = passcode_in_password
    return connection_parameters


def _connection(
    connection_parameters: Dict[str, Union[str, bool]]
) -> SnowflakeConnection:
    # https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-connect
    return connect(**connection_parameters)


def snowflake_connection(
    user: str,
    account: str,
    role: str,
    warehouse: str,
    password: Optional[str] = None,
    host: Optional[str] = None,
    authenticator: Optional[str] = None,
    passcode: Optional[str] = None,
    passcode_in_password: Optional[bool] = None,
) -> SnowflakeConnection:
    """
    Returns a Snowflake Connection to the specified account.
    """
    return _connection(
        create_connection_parameters(
            user=user,
            password=password,
            host=host,
            account=account,
            role=role,
            warehouse=warehouse,
            authenticator=authenticator,
            passcode=passcode,
            passcode_in_password=passcode_in_password,
        )
    )
