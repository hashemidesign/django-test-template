import os
import time

import docker


def start_database_container():
    client = docker.from_env(timeout=5)
    container_name = "project"
    script_dir = os.path.abspath("postgres/scripts")

    try:
        existing_container = client.containers.get(container_name)
        print(f"Container '{container_name}' exists")
        existing_container.stop()
        existing_container.remove()
        print(f"Container '{container_name}' removed")
    except docker.errors.NotFound:
        print(f"Container '{container_name}' does not exists")

    healthcheck_config = {
        "test": [
            "CMD-SHELL",
            "pg_isready -U postgres",
        ],
        "interval": 1000000000,
        "timeout": 5000000000,
        "retries": 5,
        "start_period": 2000000000,
    }

    container_config = {
        "image": "postgres:16.3-alpine3.20",
        "name": container_name,
        "detach": True,
        "ports": {"5432": "5434"},
        "environment": {
            "POSTGRES_USER": "postgres",
            "POSTGRES_PASSWORD": "postgres",
        },
        "volumes": [f"{script_dir}:/docker-entrypoint-initdb.d"],
        "network": "dev-network",
        "healthcheck": healthcheck_config,
    }

    try:
        container = client.containers.run(**container_config)

        print(f"Container '{container_name}' has started")
        wait_for_postgres_healthcheck(container)
        print("Postgres is ready")
    except docker.errors.APIError as e:
        print(f"Failed to start container. '{e}'")
        raise

    return container


def check_postgres_health(container):
    health = container.attrs.get("State", {}).get("Health", {})
    return health.get("Status").lower() == "healthy"


def wait_for_postgres_healthcheck(container, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            container.reload()
            if container.status == "running":
                if check_postgres_health(container):
                    print("Health check passed")
                    return True
            time.sleep(2)
        except Exception as e:
            print(f"Error checking container status: {e}")


def ensure_network_exists(network_name):
    client = docker.from_env()
    try:
        client.networks.get(network_name)
        print(f"Network '{network_name}' already exists.")
    except docker.errors.NotFound:
        print(f"Creating network '{network_name}'.")
        client.networks.create(
            network_name,
            driver="bridge",
            ipam={"Config": [{"Subnet": "192.168.0.0/24"}]},
        )
