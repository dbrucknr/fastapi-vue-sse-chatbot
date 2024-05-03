# FastAPI Dependencies
from fastapi import Request, Depends, HTTPException
from fastapi.responses import StreamingResponse

# OpenAI Dependencies
from openai import AsyncOpenAI

# Redis Dependencies
from redis.asyncio.client import Redis, RedisError

# Local Dependencies
from src.modules.events.types import Message
from src.shared import openai_client, redis_client

###############################################################################
# Subscription Handler
###############################################################################
async def subscribe(
    request: Request, 
    redis: Redis = Depends(redis_client),
    openai: AsyncOpenAI = Depends(openai_client)
) -> StreamingResponse:
    """
        Extract the desired channel from the Request context.
        Subscribes the client to the channel for real-time updates.
    """
    channel = 'example'  # topic - TODO: get from request context

    async def openai_response_generator():
        async with redis.pubsub() as listener:
            await listener.subscribe(channel)
            async for event in listener.listen():
                if event['type'] == 'message':
                    response_stream = await openai.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            { "role": "user", "content": event['data'] }
                        ], # I think this might be the event['data'] + some DB history
                        stream=True,
                    )
                    async for chunk in response_stream:
                        if chunk.choices[0].delta.content:
                            yield f"data: {chunk.choices[0].delta.content}\n\n"
                        if await request.is_disconnected():
                            break

    return StreamingResponse(
        content=openai_response_generator(), 
        media_type="text/event-stream"
    )

###############################################################################
# Publish Handler
###############################################################################
async def publish(
    message: Message, 
    redis: Redis = Depends(redis_client)
) -> dict[str, int]:
    """
        Extract the desired channel from the Request context.
        Publishes a message to the channel for real-time updates.
    """
    channel = 'example' 
    try:
        # TODO: Check if channel has subscribers?
        subcriber_count = await redis.publish(
            channel=channel, 
            message=message.content
        )
        return { "received_by": subcriber_count }
    except RedisError as error:
        raise HTTPException(status_code=500, detail=str(error))