import aiohttp
import asyncio
import aiomysql
import pyquery
import re

start_url=''
waitting_urls = []
seen_urls = set()
stopping = False

sem = asyncio.Semaphore(3)


async def fetch(url, session):
    '''异步访问URL获取html内容'''
    # 限制并发请求数量
    async with sem:
        await asyncio.sleep(1)  # 1秒3个请求
        try:
            async with session.get(url) as resp:
                if resp.status in [200, 201]:
                    data = await resp.text()
                    return data
        except Exception as e:
            print(e)


def extract_urls(html):
    '''解析html页面，提取URL'''
    urls=[]
    pq = pyquery.PyQuery(html)
    for link in pq.items('a'):
        url=link.attr('href')
        if url and url.startswith('http') and url not in seen_urls:
            urls.append(url)
            waitting_urls.append(url)
    return urls


async def init_urls(url, session):
    '''如果页面不是详情页，则继续提取URL'''
    html = await fetch(url, session)
    seen_urls.add(url)
    extract_urls(html)


async def article_handler(url, session, pool):
    '''获取文章详情并解析入库'''
    html = await fetch(url, session)
    seen_urls.add(url)
    extract_urls(html)
    pq = pyquery.PyQuery(html)
    title = pq('title').text()
    # 数据库操作
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            insert_sql = "insert into article(title)VALUES('{}')".format(title)
            await cur.execute(insert_sql)


async def consumer(pool):
    '''不停从waitting_urls中取URL，创建协程，去解析URL'''
    async with aiohttp.ClientSession() as session:
        while not stopping:
            # 用queue就无需处理列表为空的情况
            if len(waitting_urls) == 0:
                await asyncio.sleep(1)
                continue
            url = waitting_urls.pop()
            print('start get url:{}'.format(url))
            if re.match('http://.*?jobbole.com/\d+/', url):
                if url not in seen_urls:
                    asyncio.ensure_future(article_handler(url, session, pool))
                    # 加点延迟，别被ban了
                    await asyncio.sleep(10)
            else:
                if url not in seen_urls:
                    asyncio.ensure_future(init_urls(url, session))


async def main(loop):
    # 等待mysql连接建立好
    pool = await aiomysql.create_pool(host='localhost', port=3306,
                                      user='root', password='pass',
                                      db='mysql', loop=loop,
                                      charset='utf8', autocommit=True)

    async with aiohttp.ClientSession() as session:
        html = await fetch(start_url, session)
        seen_urls.add(start_url)
        extract_urls(html)

    asyncio.ensure_future(consumer(pool))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(main(loop))
    loop.run_forever()
