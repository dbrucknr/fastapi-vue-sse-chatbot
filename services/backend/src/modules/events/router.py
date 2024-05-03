from fastapi import APIRouter
import src.modules.events.pubsub as pubsub

event_router = APIRouter()

event_router.add_api_route(
    path="/subscribe",
    methods=["GET"],
    endpoint=pubsub.subscribe,
    summary="Server Sent Event Subscription Endpoint",
    dependencies=[],
    description=""
)

event_router.add_api_route(
    path="/publish",
    methods=["POST"],
    endpoint=pubsub.publish,
    summary="Server Sent Event Publish Endpoint"
)