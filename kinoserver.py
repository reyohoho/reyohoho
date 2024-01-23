from typing import Union

from fastapi import FastAPI, status, Response, Request, Form

from fastapi.middleware.cors import CORSMiddleware

import nkinopoiskpy

from nkinopoiskpy.movie import Movie

import json
import logging
import sys
import requests

from cached_kinopoisk_unofficial.kinopoisk_api_client import CachedKinopoiskApiClient
from cached_kinopoisk_unofficial.request.films.search_by_keyword_request import SearchByKeywordRequest
from cached_kinopoisk_unofficial.model.dictonary.film_type import FilmType
from cached_kinopoisk_unofficial.request.films.film_request import FilmRequest
import requests_cache
from datetime import timedelta

logging.basicConfig(
    filename=('kino_server_int.log'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

session = requests_cache.CachedSession('iframe_cache', expire_after=timedelta(days=1))

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/cache")
async def cache(kinopoisk: str = Form(...)):
    iframes = []
    try:
        iframe_video = session.get('https://iframe.video/api/v2/search?kp=' + str(kinopoisk), timeout=2)
        first_result = iframe_video.json()["results"][0]
        iframe_iframe = format_result('iframe', first_result['path'], first_result['title_ru'], '')
        iframes.append(iframe_iframe)
    except Exception as e:
        logger.error('iframe.video ' + str(e))

    try:
        iframe_video = session.get('https://apicollaps.cc/list?token=token&kinopoisk_id=' + str(kinopoisk), timeout=2)
        first_result = iframe_video.json()["results"][0]
        iframe_iframe = format_result('apicollaps', first_result['iframe_url'], first_result['name'], first_result['quality'])
        iframes.append(iframe_iframe)
    except Exception as e:
        logger.error('apicollaps ' + str(e))

    try:
        iframe_video = session.get('https://videocdn.tv/api/short?api_token=token&kinopoisk_id=' + str(kinopoisk), timeout=2)
        first_result = iframe_video.json()["data"][0]
        iframe_iframe = format_result('videocdn', first_result['iframe_src'], first_result['title'], '')
        iframes.append(iframe_iframe)
    except Exception as e:
        logger.error('videocdn ' + str(e))

    # try: #collapse analog
    #     iframe_video = requests.get('https://api.bhcesh.me/list?token=token&kinopoisk_id=' + str(kinopoisk), timeout=2)
    #     first_result = iframe_video.json()["results"][0]
    #     iframe_iframe = format_result('bhcesh', first_result['iframe_url'], first_result['name'], first_result['quality'])
    #     iframes.append(iframe_iframe)
    # except Exception as e:
    #     logger.error('bhcesh ' + str(e))

    try:
        iframe_video = session.get('https://apivb.info/api/videos.json?token=token&id_kp=' + str(kinopoisk), timeout=2)
        first_result = iframe_video.json()[0]
        iframe_iframe = format_result('hdvb', first_result['iframe_url'], first_result['title_ru'], first_result['quality'])
        iframes.append(iframe_iframe)
    except Exception as e:
        logger.error('hdvb ' + str(e))

    try:
        iframe_video = session.get('https://bazon.cc/api/search?token=token&kp=' + str(kinopoisk), timeout=2)
        first_result = iframe_video.json()['results']
        final_res = ''
        for res in first_result:
            final_res = final_res + format_result('bazon', res['link'], res['info']['rus'], res['quality']) + ','
        final_res = final_res.rstrip(',')
        iframes.append(final_res)
    except Exception as e:
        logger.error('bazon ' + str(e))

    try:
        iframe_video = session.get('https://api.alloha.tv/?token=token&kp=' + str(kinopoisk), timeout=2)
        first_result = iframe_video.json()['data']
        iframe_iframe = format_result('alloha', first_result['iframe'], 'alloha ' + first_result['name'], first_result['quality'])
        iframes.append(iframe_iframe)
    except Exception as e:
        logger.error('alloha ' + str(e))

    try:
        r = session.get('https://voidboost.tv/embed/' + str(kinopoisk), timeout=2)
        if r.status_code != 404:
            iframe_iframe = format_result('voidboost', 'https://voidboost.tv/embed/' + str(kinopoisk), 'voidboost', '')
            iframes.append(iframe_iframe)
    except Exception as e:
        logger.error('voidboost ' + str(e))

    result = "{"
    for iframe in iframes:
        result = result + iframe + ','
    result = result + '}'
    result = result.replace('},}', '}}')
    return Response(content=result, media_type="application/json")
    

def format_result(src_name, iframe_url, translate, quality):
    return '"' + src_name + '":{"iframe":"' + iframe_url + '","translate":"' + translate + '","quality":"' + quality + '"}'
    
    
@app.get("/search/{query}")
def search(query: str, request: Request):
    try:
        logger.info(query)
        api_client = CachedKinopoiskApiClient("token")
        api_request = SearchByKeywordRequest(query)
        response = api_client.films.send_search_by_keyword_request(api_request)
        movies = []
        if query.isdigit():
            try:
                request_by_id = FilmRequest(int(query))
                response_by_id = api_client.films.send_film_request(request_by_id)
                name = ''
                film_by_id = response_by_id.film
                if film_by_id.name_ru is None:
                    name=film_by_id.name_en
                else:
                    name=film_by_id.name_ru
                movies.append({"id":film_by_id.kinopoisk_id, "title":name + ' (' + str(film_by_id.year) + ') ' + film_by_id.type.name, "poster":film_by_id.poster_url_preview})
            except Exception as error:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error('Film by id error: ' + str(error) + ", line: " + str(exc_tb.tb_lineno))
                pass
        for film in response.films:
             if film.year is None or film.year == 'None' or film.year == 'null':
                 continue
             movie_type = ''
             name = ''
             if film.name_ru is None:
                 name=film.name_en
             else:
                 name=film.name_ru
             movies.append({"id":film.film_id, "title":name + ' (' + str(film.year) + ') ' + film.type.name, "poster":film.poster_url_preview})
        json_string = json.dumps(movies)
        logger.info(query + ', result_json: ' + json.dumps(movies, ensure_ascii=False))
        if len(movies) == 0:
            return []
        return Response(content=json_string, media_type="application/json")
    except Exception as error:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error('Error: ' + str(error) + ", line: " + str(exc_tb.tb_lineno))
        try:
            logger.info('Try official API')
            movie_list = Movie.objects.search(query)
            if len(movie_list) == 0:
                return []
            movies = []
            for movie in movie_list:
                 if movie.runtime is None:
                     continue
                 if movie.year is None or movie.year == 'None':
                     continue
                 movie_type = ''
                 if movie.series:
                     movie_type='Сериал'
                 else:
                     movie_type='Фильм'
                 movies.append({"id":movie.id, "title":movie.title + ' (' + str(movie.year) + ') ' + movie_type})
            json_string = json.dumps(movies)
            logger.info(query + ', result_json: ' + json.dumps(movies, ensure_ascii=False))
            return Response(content=json_string, media_type="application/json")
        except Exception as error:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error('Error: ' + str(error) + ", line: " + str(exc_tb.tb_lineno))
            return []
