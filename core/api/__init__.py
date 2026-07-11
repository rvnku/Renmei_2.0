from aiohttp import ClientResponseError, ClientSession
from core.config import Conf
from datetime import datetime, timezone
from typing import Optional
import asyncio, logging


logger = logging.getLogger('api')


async def fetch_token(session: ClientSession, user_id: str) -> Optional[str]:
    try:
        async with session.get(f'{Conf.base_url}/auth/token', params={'user_id': user_id}) as response:
            match response.status:
                case 200:
                    data = await response.json()
                    return data.get('access_token')
                case 404:
                    return
                case code:
                    data = await response.text()
                    logger.error(f'Auth server error {code}: {data}')
    except ClientResponseError as exc:
        logger.error(f'Network error: {exc}')


async def poll_token(session: ClientSession, user_id: str, interval: float, timeout: float) -> Optional[str]:
    start = datetime.now(timezone.utc)
    while (datetime.now(timezone.utc) - start).total_seconds() < timeout:
        if token := await fetch_token(session, user_id):
            return token
        else:
            await asyncio.sleep(interval)
