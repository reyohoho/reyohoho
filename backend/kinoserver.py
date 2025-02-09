from sanic import Sanic, response
from sanic.response import json, text, raw
from sanic.log import logger
from sanic.exceptions import ServerError, SanicException
from sanic_cors import CORS
from db_client.db_client import DatabaseClient
from aiohttp_client_cache import CachedSession, RedisBackend, SQLiteBackend
from aiohttp import ClientSession
from enum import Enum
import ujson
import dataclasses
import requests
import os
import re
import asyncio
from urllib.parse import unquote
from aiocache import cached
from aiocache.serializers import PickleSerializer
from urllib.parse import urlparse

from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.request.films.search_by_keyword_request import (
    SearchByKeywordRequest,
)
from kinopoisk_unofficial.model.dictonary.film_type import FilmType
from kinopoisk_unofficial.request.films.film_request import FilmRequest
import geoip2.database
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()
app = Sanic("reyohoho")

KINOPOISK_TECH_API_TOKEN = os.getenv("KINOPOISK_TECH_API_TOKEN")
COLLAPS_TOKEN = os.getenv("COLLAPS_TOKEN")
LUMEX_TOKEN = os.getenv("LUMEX_TOKEN")
CDNMOVIES_TOKEN = os.getenv("CDNMOVIES_TOKEN")
ALLOHA_TOKEN = os.getenv("ALLOHA_TOKEN")
HDVB_TOKEN = os.getenv("HDVB_TOKEN")
VIBIX_TOKEN = os.getenv("VIBIX_TOKEN")
KODIK_TOKEN = os.getenv("KODIK_TOKEN")
REDIS_ADDRESS = os.getenv("REDIS_ADDRESS")
GEOIP_DB_PATH = os.getenv("GEOIP_DB_PATH")

origins = [
    "https://reyohoho.space",
    "https://reyohoho.space:4435",
    "https://reyohoho.space:4446",
    "https://reyohoho.github.io",
    "https://reyohoho.github.io/reyohoho",
    "https://reyohoho.serv00.net",
    "https://reyohoho.surge.sh",
    "https://reyohoho.vercel.app",
]

o1rigins = ["*"]


cors = CORS(app, resources={r"*": {"origins": origins}})

CACHE_TOP_TTL = 86400  # 24h
CACHE_PL_TTL = 600  # 10m

kinopoisk_api_client = KinopoiskApiClient(KINOPOISK_TECH_API_TOKEN)
session_hdr = requests.Session()
app.static("/", "yohoho", index="index.html")


async def get_video_from_collaps(kinopoisk):
    url = f"https://apicollaps.cc/list?token={COLLAPS_TOKEN}&kinopoisk_id={kinopoisk}"
    async with CachedSession(cache=app.ctx.backend) as session:
        try:
            async with session.get(url, timeout=5) as response:
                response.raise_for_status()
                response = await response.json()
                first_result = response["results"][0]
                iframe_iframe = format_result(
                    "collaps", first_result["iframe_url"], f"COLLAPS", ""
                )
                return iframe_iframe
        except Exception as e:
            logger.warning(f"Error processing collaps API: {e}")
            url = f"https://api.bhcesh.me/list?token={COLLAPS_TOKEN}&kinopoisk_id={kinopoisk}"
            try:
                async with session.get(url, timeout=5) as response:
                    response.raise_for_status()
                    response = await response.json()
                    first_result = response["results"][0]
                    iframe_iframe = format_result(
                        "collaps",
                        first_result["iframe_url"],
                        f"COLLAPS",
                        "",
                    )
                    return iframe_iframe
            except Exception as e:
                logger.warning(f"Error processing bhcesh(collaps) API: {e}")
                return None


async def get_video_from_lumex(kinopoisk):
    try:
        url = f"https://portal.lumex.host/api/short?api_token={LUMEX_TOKEN}&kinopoisk_id={kinopoisk}"
        async with CachedSession(cache=app.ctx.backend) as session:
            async with session.get(url, timeout=5) as response:
                response.raise_for_status()
                response = await response.json(content_type=None)
                first_result = response["data"][0]
                iframe_iframe = format_result(
                    "videocdn", first_result["iframe_src"], f"LUMEX", ""
                )
                return iframe_iframe
    except Exception as e:
        logger.warning(f"Failed lumex: {e}")
        return None


async def get_video_from_cdnmovies(kinopoisk, referer):
    try:
        if "github" in referer:
            return None
        url = f"https://api.cdnmovies.net/v1/contents?token={CDNMOVIES_TOKEN}&kinopoisk_id={kinopoisk}"
        async with CachedSession(cache=app.ctx.backend) as session:
            async with session.get(url, timeout=5) as response:
                response.raise_for_status()
                response = await response.text()
                if "iframe" in response:
                    iframe_iframe = format_result(
                        "cdnmovies",
                        f"https://ugly-turkey.cdnmovies-stream.online/kinopoisk/{kinopoisk}/iframe?domain=reyohoho.github.io",
                        "CDNMOVIES",
                        "",
                    )
                    return iframe_iframe
                return None
    except Exception as e:
        logger.warning(f"Failed cdnmovies: {e}")
        return None


async def get_video_from_alloha(kinopoisk):
    try:
        url = f"https://api.apbugall.org/?token={ALLOHA_TOKEN}&kp={kinopoisk}"
        async with CachedSession(cache=app.ctx.backend) as session:
            async with session.get(url, timeout=5) as response:
                response.raise_for_status()
                response = await response.json(content_type=None)
                first_result = response["data"]
                new_url = re.sub(
                    r"https://[^/]+",
                    "https://attractive-as.allarknow.online",
                    first_result["iframe"],
                )
                iframe_iframe = format_result(
                    "alloha",
                    new_url,
                    "ALLOHA",
                    "",
                )
                return iframe_iframe
    except Exception as e:
        logger.warning(f"Failed alloha: {e}")
        return None


async def get_video_from_hdvb(kinopoisk):
    try:
        # see new domain on https://github.com/hdvb-player/hdvb-player.github.io/blob/main/actualize.js
        url = f"https://kinolordfilm.com/api/videos.json?token={HDVB_TOKEN}&id_kp={kinopoisk}"
        async with CachedSession(cache=app.ctx.backend) as session:
            async with session.get(url, timeout=5) as response:
                response.raise_for_status()
                response = await response.json(content_type=None)
                first_result = response[0]
                iframe_iframe = format_result(
                    "hdvb",
                    first_result["iframe_url"],
                    "HDVB",
                    "",
                )
                return iframe_iframe
    except Exception as e:
        logger.warning(f"Failed hdvb: {e}")
        return None


async def get_video_from_vibix(kinopoisk):
    try:
        url = f"https://vibix.org/api/v1/publisher/videos/kp/{kinopoisk}"
        async with CachedSession(cache=app.ctx.backend) as session:
            async with session.get(
                url,
                timeout=5,
                headers={"Authorization": f"Bearer {VIBIX_TOKEN}"},
            ) as response:
                response.raise_for_status()
                response = await response.json(content_type=None)
                first_result = response
                iframe_iframe = format_result(
                    "vibix", first_result["iframe_url"], "VIBIX", ""
                )
                return iframe_iframe
    except Exception as e:
        logger.warning(f"Failed vibix: {e}")
        return None


async def get_video_from_militorys(kinopoisk):
    try:
        url = f"https://militorys.net/api/{kinopoisk}"
        async with CachedSession(cache=app.ctx.backend) as session:
            async with session.get(url, timeout=5) as response:
                response.raise_for_status()
                text_test = await response.text()
                if "playlist_id" in text_test:
                    iframe_iframe = format_result(
                        "militorys",
                        f"https://militorys.net/van/{kinopoisk}",
                        "MILITORYS",
                        "",
                    )
                    return iframe_iframe
    except Exception as e:
        logger.warning(f"Failed militorys: {e}")
        return None


async def get_video_from_videoseed(kinopoisk):
    try:
        url = f"https://tv-2-kinoserial.net/api.php?kp_id={kinopoisk}"
        async with CachedSession(cache=app.ctx.backend) as session:
            async with session.get(url, timeout=5, allow_redirects=True) as response:
                response.raise_for_status()
                if "embed" in str(response.url):
                    iframe_iframe = format_result(
                        "videoseed", str(response.url), "VIDEOSEED", ""
                    )
                    return iframe_iframe
    except Exception as e:
        logger.warning(f"Failed videoseed: {e}")
        return None


turbo_block_countries = {"AU", "CA", "FR", "DE", "NL", "ES", "TR", "GB", "US", "JP"}
async def get_video_from_turbo(request, kinopoisk):
    try:
        url = f"https://4f463c79.obrut.show/embed/IDN/kinopoisk/{kinopoisk}"
        with geoip2.database.Reader(GEOIP_DB_PATH) as reader:
            client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
            try:
                response = reader.country(client_ip)
            except Exception as e:
                logger.warning(f"Failed check geoip: {e}")
            if response.country.iso_code in turbo_block_countries:
                logger.warning(f"Turbo block by iso code: {response.country.iso_code}")
                return None
        async with CachedSession(cache=app.ctx.backend) as session:
            async with session.get(
                url,
                timeout=5,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
                },
            ) as response:
                response.raise_for_status()
                iframe_iframe = format_result(
                    "turbo",
                    "https://4f463c79.obrut.show/embed/IDN/kinopoisk/" + str(kinopoisk),
                    "TURBO",
                    "",
                )
                return iframe_iframe
    except Exception as e:
        logger.warning(f"Failed turbo: {e}")
        return None


async def get_video_from_kodik(kinopoisk):
    try:
        url = (
            f"https://kodikapi.com/search?token={KODIK_TOKEN}&kinopoisk_id={kinopoisk}"
        )
        async with CachedSession(cache=app.ctx.backend) as session:
            async with session.get(url, timeout=5) as response:
                response.raise_for_status()
                response = await response.json(content_type=None)
                k_iframes = []
                for result in response["results"]:
                    if result["title"] in str(k_iframes):
                        continue
                    iframe_iframe = format_result(
                        f"kodik{50 - len(k_iframes)}",
                        f"https:{result['link']}",
                        f"KODIK>{result['title']}",
                        "",
                    )
                    k_iframes.append(iframe_iframe)
                return k_iframes
    except Exception as e:
        logger.warning(f"Failed kodik: {e}")
        return None


async def cache_kodik(kinopoisk: str) -> tuple[str | None, str | None]:
    shiki_id = re.sub(r"[^0-9]", "", kinopoisk)
    url = f"https://kodikapi.com/search?token={KODIK_TOKEN}&shikimori_id={shiki_id}"
    async with CachedSession(cache=app.ctx.backend) as session:
        async with session.get(url, timeout=5) as response:
            response.raise_for_status()
            response = await response.json(content_type=None)
            results = response.get("results", [])

            k_iframes = []
            iframes = []
            seen_titles = set()

            for result in results:
                if "kinopoisk_id" in result:
                    return result["kinopoisk_id"], None
                title = result["title"]
                if title in seen_titles:
                    continue

                seen_titles.add(title)
                iframe_iframe = format_result(
                    f"kodik{len(k_iframes) + 1}",
                    f"https:{result['link']}",
                    f"KODIK>{title}",
                    "",
                )
                k_iframes.append(iframe_iframe)
                iframes.append(iframe_iframe)

            result = "{" + ",".join(iframes) + "}"
    return None, result


@app.get("/check_cache")
async def check_cache(request):
    r = requests.post(
        "http://localhost:5788/cache",
        {"kinopoisk": "301", "code": "31", "type": "check"},
    )
    return raw(r.content, status=r.status_code)


@app.post("/cache")
async def cache_request(request):
    kinopoisk = request.form.get("kinopoisk")
    video_type = request.form.get("type", None)
    if kinopoisk is None:
        return json({})
    if kinopoisk.startswith("shiki"):
        try:
            kinopoisk, text_kodik = await cache_kodik(kinopoisk.replace("shiki", ""))
            if text_kodik:
                return text(
                    text_kodik,
                    headers={"Content-Type": "application/json; charset=utf-8"},
                )
        except:
            return json({})
    try:
        kp_id = int(kinopoisk)
        if kp_id == 0:
            return json({})
        if DatabaseClient().check_id_is_blocked(kp_id) is not None:
            return text("Item blocked", status=403)
    except ValueError as e:
        logger.error(f"Kinopoisk ID to int error: {e}")
        return text("Not int", status=500)

    request_by_id = FilmRequest(int(kinopoisk))
    response_by_id = kinopoisk_api_client.films.send_film_request(request_by_id)
    film_by_id = response_by_id.film
    name = film_by_id.name_ru or film_by_id.name_en or film_by_id.name_original

    tasks = [
        get_video_from_collaps(kinopoisk),
        get_video_from_lumex(kinopoisk),
        get_video_from_cdnmovies(kinopoisk, str(request.headers.get("referer"))),
        get_video_from_alloha(kinopoisk),
        get_video_from_turbo(request, kinopoisk),
        get_video_from_kodik(kinopoisk),
        get_video_from_vibix(kinopoisk),
        get_video_from_videoseed(kinopoisk),
        get_video_from_hdvb(kinopoisk),
        get_video_from_militorys(kinopoisk),
    ]

    wrapped_tasks = [asyncio.wait_for(task, timeout=10) for task in tasks]

    try:
        iframe_results = await asyncio.gather(*wrapped_tasks, return_exceptions=True)
        for i, iframe_result in enumerate(iframe_results):
            # logger.error(f"Task {i} str, PID: {os.getpid()} {iframe_result}, kp_id: {kinopoisk}")
            if iframe_result is None:
                # logger.error(f"Task {i} result is None, kp_id: {kinopoisk}")
                continue
            if isinstance(iframe_result, asyncio.TimeoutError):
                logger.error(f"Task {i} exceeded timeout, PID: {os.getpid()}")
    except asyncio.TimeoutError as e:
        logger.error(f"One or more tasks exceeded timeout: {e}, PID: {os.getpid()}")

    iframes = []
    for result in iframe_results:
        if isinstance(result, asyncio.TimeoutError):
            continue
        if result is None:
            continue
        if result:
            if isinstance(result, list):
                iframes.extend(result)
            else:
                iframes.append(result)

    if len(iframes) > 0:
        try:
            client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
            logger.info(f"Pre add watch: kp_id: {kinopoisk}, IP:{client_ip}")
            DatabaseClient().insert_video_stats(
                kinopoisk,
                film_by_id.poster_url,
                name,
                film_by_id.year,
                film_by_id.rating_kinopoisk,
                film_by_id.rating_imdb,
                film_by_id.web_url,
                f"https://www.imdb.com/title/{film_by_id.imdb_id}/",
                film_by_id.type,
                client_ip,
            )
        except Exception as e:
            logger.error(f"Error insert to video stats DB: ${e}")

    result = "{" + ",".join(iframes) + "}"
    result = result.replace("},}", "}}")
    return text(result, headers={"Content-Type": "application/json; charset=utf-8"})


def format_result(src_name, iframe_url, translate, quality):
    return (
        f'"{src_name.strip()}":{{'
        f'"iframe":"{iframe_url.strip()}",'
        f'"translate":"{translate.strip()}",'
        f'"quality":"{quality.strip()}"'
        f"}}"
    )


@app.get("/search/<term>")
async def search_kinopoisk(request, term):
    if not term:
        return text("No term string provided")

    api_request = SearchByKeywordRequest(unquote(term))
    response = kinopoisk_api_client.films.send_search_by_keyword_request(api_request)
    movies = [
        {
            "id": film.film_id,
            "title": (film.name_ru or film.name_en or film.name_original)
            + f" ({film.year})",
            "poster": film.poster_url_preview,
        }
        for film in response.films
        if film.year not in [None, "None", "null"]
    ]

    if not movies:
        return json([])
    return json(movies)


@app.get("/shiki_info/<shiki>")
async def shiki_info(request, shiki):
    if not shiki or "shiki" not in shiki:
        return text("No shiki query provided")

    shiki_id = shiki.replace("shiki", "")
    shiki_id = re.sub(r"[^0-9]", "", shiki_id)

    if not shiki_id or not shiki_id.isnumeric():
        return text("No valid shiki_id provided")

    if shiki_id == 0:
        return json({})

    url = f"https://kodikapi.com/search?token={KODIK_TOKEN}&shikimori_id={shiki_id}"
    try:
        async with CachedSession(cache=app.ctx.backend) as session:
            async with session.get(url, timeout=5) as response:
                response.raise_for_status()
                response = await response.json()
                results = response.get("results", [])
                if not results:
                    return json([])

                first = results[0]
                res = {
                    "name_ru": first.get("title"),
                    "name_en": first.get("title_orig"),
                    "slogan": first.get("other_title"),
                    "year": first.get("year"),
                }

                return json(res)
    except Exception as e:
        raise SanicException("Failed to fetch data", status_code=500) from e


@app.get("/kp_info/<kp_id>")
async def kinopoisk_info(request, kp_id):
    if not kp_id or not kp_id.isnumeric():
        return text("No valid kp_id provided")
    if kp_id == 0:
        return json({})
    request_by_id = FilmRequest(int(kp_id))
    response_by_id = kinopoisk_api_client.films.send_film_request(request_by_id)
    film_by_id = response_by_id.film
    film_dict = dataclasses.asdict(film_by_id)
    for key, value in film_dict.items():
        if isinstance(value, Enum):
            film_dict[key] = value.name
    json_string = ujson.dumps(film_dict, ensure_ascii=False)
    return text(
        json_string, headers={"Content-Type": "application/json; charset=utf-8"}
    )


@app.get("/top/<type>")
async def top(request, type):
    if not type:
        return text("No valid type provided")
    db = DatabaseClient()
    type_filter = request.args.get("type")
    if type_filter == "movie":
        type_filter = "FilmType.FILM"
    if type_filter == "series":
        type_filter = "FilmType.TV_SERIES"
    if type_filter == "all":
        type_filter = None

    data = None

    if type == "all":
        data = db.get_top_video_stats(type=type_filter)
    if type == "30d":
        data = db.get_top_video_stats_30_days(type=type_filter)
    if type == "7d":
        data = db.get_top_video_stats_7_days(type=type_filter)
    if type == "24h":
        data = db.get_top_video_stats_1_days(type=type_filter)

    replacements = {
        "FilmType.FILM": "🎬Фильм",
        "FilmType.VIDEO": "🎬Видео",
        "FilmType.TV_SERIES": "🎬Сериал",
        "FilmType.MINI_SERIES": "🎬Мини-сериал",
        "FilmType.TV_SHOW": "🎬ТВ-шоу",
    }

    def replace_values(obj):
        if isinstance(obj, dict):
            return {k: replace_values(v) for k, v in obj.items()}
        elif isinstance(obj, tuple):
            return tuple(replace_values(item) for item in obj)
        elif isinstance(obj, list):
            return [replace_values(item) for item in obj]
        elif isinstance(obj, str):
            return replacements.get(obj, obj)
        return obj

    data = replace_values(data)

    return json(data)


@app.get("/get_pl_list_1")
@cached(ttl=CACHE_PL_TTL, serializer=PickleSerializer(), key="pl_key")
async def get_pl_list_1(request):
    return text(DatabaseClient().get_pl_1()["data"])


@app.get("/get_dons")
@cached(ttl=CACHE_PL_TTL, serializer=PickleSerializer(), key="dons_key")
async def get_dons(request):
    dons = "\n".join([item["name"] for item in DatabaseClient().get_dons()])
    return text(dons)


@app.exception(ServerError)
async def test(request, exception):
    return response.json(
        {"exception": str(exception), "status": exception.status_code},
        status=exception.status_code,
    )


@app.before_server_start
async def init_app(app, loop):
    app.ctx.backend = RedisBackend(
        cache_name="demo_cache_aio",
        address=REDIS_ADDRESS,
        expire_after=timedelta(hours=3),
    )


if __name__ == "__main__":
    app.run()