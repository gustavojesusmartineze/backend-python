from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, Any

InputType = TypeVar("InputType")
OutputType = TypeVar("OutputType")


class Result(Generic[OutputType]):
    """
    Simple success/error wrapper for use case execution.
    """

    def __init__(self, value: Optional[OutputType] = None, error: Optional[Exception] = None):
        self.value = value
        self.error = error

    @property
    def is_ok(self) -> bool:
        return self.error is None

    @property
    def is_err(self) -> bool:
        return self.error is not None

    @staticmethod
    def ok(value: OutputType) -> "Result[OutputType]":
        return Result(value=value)

    @staticmethod
    def fail(error: Exception) -> "Result[Any]":
        return Result(error=error)


class BaseUseCase(ABC, Generic[InputType, OutputType]):
    """
    Base class for application-level use cases.

    Override:
      - validate(input)
      - perform(input)
    """

    async def execute(self, input_data: InputType) -> Result[OutputType]:
        try:
            await self.validate(input_data)
            output = await self.perform(input_data)
            return Result.ok(output)
        except Exception as exc:
            return Result.fail(exc)

    async def validate(self, input_data: InputType) -> None:
        """
        Optional input validation hook.
        Override if needed.
        """
        return None

    @abstractmethod
    async def perform(self, input_data: InputType) -> OutputType:
        """
        Main business logic implementation.
        Must be async.
        """
        raise NotImplementedError
