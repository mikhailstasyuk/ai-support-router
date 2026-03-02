from collections.abc import Callable

from .file_backend import FileBackend


class DomainRepository:
    def __init__(self, backend: FileBackend, domain: str, id_field: str = "id") -> None:
        self.backend = backend
        self.domain = domain
        self.id_field = id_field

    def all(self) -> list[dict]:
        return self.backend.read(self.domain)

    def get(self, value: str) -> dict | None:
        for record in self.all():
            if record.get(self.id_field) == value:
                return record
        return None

    def find(self, matcher: Callable[[dict], bool]) -> list[dict]:
        return [record for record in self.all() if matcher(record)]

    def save(self, record_id: str, payload: dict) -> dict:
        return self.backend.upsert(self.domain, record_id, payload, self.id_field)

    def delete(self, record_id: str) -> bool:
        return self.backend.delete(self.domain, record_id, self.id_field)


class Repositories:
    def __init__(self, backend: FileBackend) -> None:
        self.callers = DomainRepository(backend, "callers", "caller_id")
        self.policies = DomainRepository(backend, "policies", "policy_id")
        self.appointments = DomainRepository(backend, "appointments", "appointment_id")
        self.renewals = DomainRepository(backend, "renewals", "renewal_id")
        self.callbacks = DomainRepository(backend, "callbacks", "callback_id")
        self.compensations = DomainRepository(backend, "compensations", "case_id")
        self.plans = DomainRepository(backend, "plans", "plan_id")
        self.feedback = DomainRepository(backend, "feedback", "feedback_id")
