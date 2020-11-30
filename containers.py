from dependency_injector import containers, providers
from services import LimitService, TransferSerivce


class Container(containers.DeclarativeContainer):
    limit_service = providers.Factory(LimitService)
    transfer_service = providers.Factory(TransferSerivce)
