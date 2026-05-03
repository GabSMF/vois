"""
Dependency injection container
"""
from typing import Dict, Any, Callable, TypeVar, Generic
from abc import ABC, abstractmethod

T = TypeVar('T')


class Container:
    """Simple dependency injection container"""

    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._factories: Dict[str, Callable[[], Any]] = {}
        self._singletons: Dict[str, Any] = {}

    def register(self, name: str, service: Any) -> None:
        """Register a service instance"""
        self._services[name] = service

    def register_factory(self, name: str, factory: Callable[[], Any]) -> None:
        """Register a factory function that creates service instances"""
        self._factories[name] = factory

    def register_singleton(self, name: str, service: Any) -> None:
        """Register a singleton service"""
        self._singletons[name] = service

    def get(self, name: str) -> Any:
        """Get a service by name"""
        if name in self._singletons:
            return self._singletons[name]
        elif name in self._services:
            return self._services[name]
        elif name in self._factories:
            return self._factories[name]()
        else:
            raise ValueError(f"Service '{name}' not registered")


# Global container instance
_container = Container()


def register_service(name: str, service: Any) -> None:
    """Register a service in the global container"""
    _container.register(name, service)


def register_factory(name: str, factory: Callable[[], Any]) -> None:
    """Register a factory in the global container"""
    _container.register_factory(name, factory)


def register_singleton(name: str, service: Any) -> None:
    """Register a singleton in the global container"""
    _container.register_singleton(name, service)


def get_service(name: str) -> Any:
    """Get a service from the global container"""
    return _container.get(name)