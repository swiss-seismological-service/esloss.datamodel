import enum

from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import BigInteger, String, Enum
from sqlalchemy.ext.mutable import MutableDict

from esloss.datamodel.mixins import CreationInfoMixin, JSONEncodedDict
from esloss.datamodel.base import ORMBase


class EStatus(enum.Enum):
    PENDING = 0
    RUNNING = 1
    ERROR = 2
    COMPLETE = 3
    DISPATCHED = 4
    PREPARED = 5
    ONHOLD = 6


class LossCalculation(ORMBase, CreationInfoMixin):
    """Calculation Parameters model"""

    aggregateby = Column(String())
    config = Column(MutableDict.as_mutable(JSONEncodedDict))
    status = Column(Enum(EStatus), default=EStatus.PENDING)
    description = Column(String())

    _assetcollection_oid = Column(BigInteger,
                                  ForeignKey('loss_assetcollection._oid',
                                             ondelete="RESTRICT"),
                                  nullable=False)
    assetcollection = relationship('AssetCollection',
                                   back_populates='losscalculation')

    _type = Column(String(25))

    __mapper_args__ = {
        'polymorphic_identity': 'losscalculation',
        'polymorphic_on': _type,
    }


class RiskCalculation(LossCalculation):
    __tablename__ = 'loss_riskcalculation'

    _oid = Column(BigInteger, ForeignKey('loss_losscalculation._oid'),
                  primary_key=True)

    losses = relationship('LossValue', back_populates='riskcalculation')

    _occupantsvulnerabilitymodel_oid = Column(
        BigInteger,
        ForeignKey('loss_vulnerabilitymodel._oid',
                   ondelete="RESTRICT"))
    _contentsvulnerabilitymodel_oid = Column(
        BigInteger,
        ForeignKey('loss_vulnerabilitymodel._oid',
                   ondelete="RESTRICT"))
    _structuralvulnerabilitymodel_oid = Column(
        BigInteger,
        ForeignKey('loss_vulnerabilitymodel._oid',
                   ondelete="RESTRICT"))
    _nonstructuralvulnerabilitymodel_oid = Column(
        BigInteger,
        ForeignKey('loss_vulnerabilitymodel._oid',
                   ondelete="RESTRICT"))
    _businessinterruptionvulnerabilitymodel_oid = Column(
        BigInteger,
        ForeignKey('loss_vulnerabilitymodel._oid',
                   ondelete="RESTRICT"))

    occupantsvulnerabilitymodel = relationship(
        'OccupantsVulnerabilityModel',
        backref='riskcalculation',
        foreign_keys=[_occupantsvulnerabilitymodel_oid])

    contentsvulnerabilitymodel = relationship(
        'ContentsVulnerabilityModel',
        backref='riskcalculation',
        foreign_keys=[_contentsvulnerabilitymodel_oid])

    structuralvulnerabilitymodel = relationship(
        'StructuralVulnerabilityModel',
        backref='riskcalculation',
        foreign_keys=[_structuralvulnerabilitymodel_oid])

    nonstructuralvulnerabilitymodel = relationship(
        'NonstructuralVulnerabilityModel',
        backref='riskcalculation',
        foreign_keys=[_nonstructuralvulnerabilitymodel_oid])

    businessinterruptionvulnerabilitymodel = relationship(
        'BusinessInterruptionVulnerabilityModel',
        backref='riskcalculation',
        foreign_keys=[_businessinterruptionvulnerabilitymodel_oid])

    __mapper_args__ = {
        'polymorphic_identity': 'riskcalculation'
    }


class DamageCalculation(LossCalculation):
    __tablename__ = 'loss_damagecalculation'

    _oid = Column(BigInteger, ForeignKey('loss_losscalculation._oid'),
                  primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'damagecalculation'
    }
