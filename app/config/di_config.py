"""
Configuration for dependency injection container
"""
from app.domain.container import Container, register_service
from app.infrastructure.implementations import create_in_memory_repositories


def configure_container() -> Container:
    """
    Configure the dependency injection container with concrete implementations.

    This function sets up the container with in-memory implementations for development/testing.
    For production, you would replace these with actual database and service implementations.
    """
    # Get in-memory implementations
    implementations = create_in_memory_repositories()

    # Register all implementations
    for interface_name, implementation in implementations.items():
        register_service(interface_name, implementation)

    return Container()  # Return a new container instance (though we use global registration)


# Initialize the container with implementations
configure_container()


# Convenience functions for getting services
def get_capture_repository():
    from app.domain.container import get_service
    return get_service("capture_repository")

def get_image_repository():
    from app.domain.container import get_service
    return get_service("image_repository")

def get_timeline_repository():
    from app.domain.container import get_service
    return get_service("timeline_repository")

def get_transcription_repository():
    from app.domain.container import get_service
    return get_service("transcription_repository")

def get_processing_job_repository():
    from app.domain.container import get_service
    return get_service("processing_job_repository")

def get_search_service():
    from app.domain.container import get_service
    return get_service("search_service")

def get_file_service():
    from app.domain.container import get_service
    return get_service("file_service")

def get_processing_service():
    from app.domain.container import get_service
    return get_service("processing_service")
