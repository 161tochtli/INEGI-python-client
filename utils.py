import os
import time
import json
import datetime as dt
from requests import Response
import requests.exceptions
from urllib.parse import urlencode, quote
from pathlib import Path
from tempfile import TemporaryDirectory
from itertools import chain
from functools import wraps
import pandas as pd


def download_all_to_csv(first_call, outfile=None, folder=None, per=250):

    with TemporaryDirectory() as td:
        page=1
        try:
            print(f"Descargando, por favor espere..")
            result = first_call

            if result.is_empty():
                print("No se encontraron resultados para esta consulta.")
            else:
                result.to_csv(folder=td,echo=False)
                file_path = result.file_path
                page += 1
                print("[■", end="")
            while page > 1:
                time.sleep(1)

                print("■",end="")
                result = result.next_page(per)
                if result.is_empty():
                    print("]\nDescarga exitosa!")
                    break
                result.to_csv(folder=td, echo=False)
                file_path = result.file_path
                page += 1
        except requests.exceptions.RequestException as e:
            print(f"An error occurred on page {page}:\n{e}")

        except Exception as e:
            print(f"Broad exception on page {page}:\n{e}")


        files = [Path(td)/f for f in os.listdir(td)]
        files.sort(key=lambda f:int(f.stem.split("-")[-2]))

        dfs = [pd.read_csv(f) for f in files]

        df = pd.concat(dfs,axis="rows")
        if not outfile:
            file_name_split = [f.rstrip(".csv").split("-") for f in os.listdir(td)]
            get_page_intervals = [f[-2:] for f in file_name_split]

            page_intervals = list(chain.from_iterable(get_page_intervals))

            min_index = min(page_intervals,key=lambda x: int(x))
            max_index = max(page_intervals,key=lambda x: int(x))

            full_df_filename = list(filter(lambda x: x[-1]==max_index,file_name_split))[0]
            full_df_filename[-2] = min_index
            full_df_filename = "-".join(full_df_filename)+".csv"
            folder = folder if folder else ''
            outfile = Path(full_df_filename)
            if folder:
                outfile = Path(folder)/outfile
        print(f"Total: {len(df)} registros")
        df.to_csv(outfile,index=False)

    outfile = Path(outfile).resolve()
    print(f"Archivo guardado en {outfile}")
    return outfile



def inspect_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        print(f'URL: {response.url}')
        print(f'Status Code: {response.status_code}')
        print(f'Headers: {response.headers}')
        print(f'Content: {response.content[:1000]}')  # Print the first 1000 bytes of the content
        return response
    return wrapper

def url_encode_param(param):
    return quote(param, safe='')

#@inspect_response
def make_request(base_url,endpoint,params,token, **kwargs):
    encoded_params = [url_encode_param(param) for param in params]
    #encoded_params = params
    parametros_url = "/".join(encoded_params)
    # Construyendo la URL
    url = f"{base_url}{endpoint}/{parametros_url}/{token}"

    # Handle optional query string parameters (if any)
    query_string_params = kwargs.pop('query', None)
    if query_string_params:
        url += f'?{urlencode(query_string_params)}'

    # Realizando la solicitud a la API
    response = None
    try:
        #print(f"Requesting {url}")
        response = requests.get(url, **kwargs)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
    except requests.exceptions.Timeout as e:
        timeout = kwargs.get('timeout', 'not specified')  # Get timeout value from kwargs or default to 'not specified'
        print(f'The request timed out after {timeout} seconds: {e}')
        raise requests.exceptions.Timeout
    except requests.exceptions.RequestException as e:
        non_standard_no_data_exception = "('Connection aborted.', BadStatusLine('HTTP/1.1 000 \\r\\n'))"
        if non_standard_no_data_exception == str(e):
            return NoDataResponse(url)
        else:
            print(f'An error other than non_standard_no_data_exception {non_standard_no_data_exception} occurred: {e}')
            raise requests.exceptions.RequestException
    return response


class NoDataResponse(Response):
    def __init__(self, url=None):
        super().__init__()
        self.status_code = 204  # HTTP status code for 'No Content'
        self.url = url
        self.headers['Content-Type'] = 'application/json; charset=utf-8'
        self._content = b'[]'  # Empty content

class Result:
    def __init__(self, response:Response|NoDataResponse, encoding='utf-8'):
        self.timestamp = dt.datetime.now()
        self.raw_response = response
        self.data = json.loads(response.content.decode(encoding))
        self.file_path = None
        self.params = {} #TODO params from url

    def make_file_path(self):
        timestamp = self.timestamp.strftime("%Y%m%d-%H%M%S")
        url = self.raw_response.url
        # remove token
        url = "/".join(url.split("/")[:-1])
        # make filepath
        query = url.split("consulta/")[1].split("/")
        numpag_query = "-".join(query[:-2])
        file_path = '-'.join([timestamp, numpag_query]) + '.csv'
        return file_path

    def to_csv(self, outfile=None, folder=None, echo=True, **kwargs):
        df = self.to_pandas()
        if not outfile:
            outfile = self.make_file_path()
            if folder:
                outfile = Path(folder)/outfile
        self.file_path = outfile
        df.to_csv(outfile, index=False, **kwargs)
        outfile = Path(outfile).resolve()
        if echo:
            print(f"Archivo guardado en {outfile}")
        return outfile


    def to_pandas(self, **kwargs):
        df = pd.DataFrame(self.data, **kwargs)
        return df

    def is_empty(self):
        return not bool(self.data)

class PaginatedResult(Result):
    def __init__(self, method, params, response):
        super().__init__(response, encoding='utf-8')
        self.method = method
        self.params = params

    def make_file_path(self):
        file_path = super().make_file_path()
        path_parts = [file_path.split(".")[0], str(self.params['registro_inicial']), str(self.params['registro_final'])]
        file_path = '-'.join(path_parts) + '.csv'
        return file_path

    def next_page(self, per='default'):
        # Update the parameters for the next page
        # Assume page is controlled by registro_inicial and registro_final
        if per == 'default':
            per = self.params['registro_final'] - self.params['registro_inicial']
        self.params['registro_inicial'] = self.params['registro_final'] + 1
        self.params['registro_final'] = self.params['registro_inicial'] + per
        # Call the method to fetch the next page
        next_result = self.method(**self.params)
        return next_result

    def to_csv(self, outfile=None, folder=None, download_all=False, **kwargs):
        if download_all:
            outfile = download_all_to_csv(self, outfile, **kwargs)
        else:
            outfile = super().to_csv(outfile, folder, **kwargs)

        return outfile


    def __next__(self):
        self.next_page()


