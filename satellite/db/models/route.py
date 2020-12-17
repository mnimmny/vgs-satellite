import enum
import uuid
from datetime import datetime
from typing import List

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import relationship

from satellite.transformers import TransformerType

from .base import Base


class RouteType(enum.Enum):
    INBOUND = 'INBOUND'
    OUTBOUND = 'OUTBOUND'


class Phase(enum.Enum):
    REQUEST = 'REQUEST'
    RESPONSE = 'RESPONSE'


class Operation(enum.Enum):
    REDACT = 'REDACT'
    ENRICH = 'ENRICH'


class Route(Base):
    __tablename__ = 'rule_chains'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=lambda: datetime.utcnow())
    protocol = Column(String)
    source_endpoint = Column(String)
    destination_override_endpoint = Column(String)
    host_endpoint = Column(String)
    port = Column(Integer)
    tags = Column(JSON)
    rule_entries_list = relationship(
        'RuleEntry',
        back_populates='rule_chain',
        cascade='all, delete, delete-orphan',
        passive_deletes=True,
    )

    @property
    def route_type(self) -> RouteType:
        return RouteType.OUTBOUND if self.is_outbound() else RouteType.INBOUND

    def is_outbound(self) -> bool:
        return self.destination_override_endpoint == '*'


class RuleEntry(Base):
    __tablename__ = 'rule_entries'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=lambda: datetime.utcnow())
    route_id = Column(String, ForeignKey('rule_chains.id', ondelete='CASCADE'))
    rule_chain = relationship('Route', back_populates='rule_entries_list')
    phase = Column(String)
    operation = Column(String)
    token_manager = Column(String)
    public_token_generator = Column(String)
    transformer = Column(Enum(TransformerType))
    transformer_config = Column(JSON)
    transformer_config_map = Column(JSON)
    targets = Column(JSON)
    classifiers = Column(JSON)
    expression_snapshot = Column(JSON)
    operations_v2 = Column(JSON)

    @property
    def has_operations(self) -> bool:
        return bool(self.operations_v2)

    @property
    def operations_config(self) -> List[dict]:
        return self.operations_v2
