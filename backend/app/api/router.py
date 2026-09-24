from fastapi import APIRouter

from app.api.routes import audit, auth, changes, cluster, deployments, hosts, logs, subnets

api_router = APIRouter(prefix="/api")
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(hosts.router, prefix="/hosts", tags=["hosts"])
api_router.include_router(subnets.router, prefix="/subnets", tags=["subnets"])
api_router.include_router(changes.router, prefix="/changes", tags=["changes"])
api_router.include_router(deployments.router, prefix="/deployments", tags=["deployments"])
api_router.include_router(cluster.router, prefix="/cluster", tags=["cluster"])
api_router.include_router(logs.router, prefix="/logs", tags=["logs"])
api_router.include_router(audit.router, prefix="/audit", tags=["audit"])
