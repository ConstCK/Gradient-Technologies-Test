import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.parametrize('url', [
    'https://example.com/long-page',
    'https://example.com/target',
    'https://example.org/path?q=1',
])
async def test_shorten_returns_short_id_and_original_url(
    client: AsyncClient,
    url: str,
) -> None:
    response = await client.post(
        '/api/v1/shorten',
        json={'url': url},
    )
    assert response.status_code == 201
    data = response.json()
    assert 'short_id' in data
    assert isinstance(data['short_id'], str)
    assert len(data['short_id']) > 0
    assert data['short_id'].startswith('gradient-technologies/')
    assert data['original_url'] == url


@pytest.mark.asyncio
async def test_redirect_increments_clicks(client: AsyncClient) -> None:
    create_resp = await client.post(
        '/api/v1/shorten',
        json={'url': 'https://example.com/target'},
    )
    assert create_resp.status_code == 201
    short_id_full = create_resp.json()['short_id']
    short_id_suffix = short_id_full.removeprefix('gradient-technologies/')

    stats_before = await client.get(f'/api/v1/stats/{short_id_suffix}')
    assert stats_before.status_code == 200
    assert stats_before.json()['clicks'] == 0

    redirect_resp = await client.get(f'/api/v1/{short_id_suffix}', follow_redirects=False)
    assert redirect_resp.status_code == 302
    assert redirect_resp.headers.get('location') == 'https://example.com/target'

    stats_after = await client.get(f'/api/v1/stats/{short_id_suffix}')
    assert stats_after.status_code == 200
    assert stats_after.json()['clicks'] == 1


@pytest.mark.asyncio
@pytest.mark.parametrize('stats_path', [
    '/api/v1/stats/{suffix}',
    '/api/v1/stats/gradient-technologies/{suffix}',
])
async def test_get_stats_returns_clicks(
    client: AsyncClient,
    stats_path: str,
) -> None:
    create_resp = await client.post(
        '/api/v1/shorten',
        json={'url': 'https://example.com/stats-test'},
    )
    assert create_resp.status_code == 201
    short_id_full = create_resp.json()['short_id']
    suffix = short_id_full.removeprefix('gradient-technologies/')

    path = stats_path.format(suffix=suffix)
    response = await client.get(path)
    assert response.status_code == 200
    data = response.json()
    assert data['short_id'] == short_id_full
    assert data['clicks'] == 0


@pytest.mark.asyncio
async def test_get_stats_not_found(client: AsyncClient) -> None:
    response = await client.get('/api/v1/stats/nonexistent-id-99')
    assert response.status_code == 404
