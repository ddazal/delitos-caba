from io import StringIO
from urllib import request
from urllib.error import URLError

import pandas as pd

BASE_URL = "https://mapa.seguridadciudad.gob.ar/descargas/delitos_{}_{}_{}.csv"

years = range(2016, 2020)

months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
          "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

tvalues = range(1, 8)

# Para tenerlo como referencia
tkeys = ["hurto_automotor", "robo_total", "hurto_total", "homicidio_doloso",
      "robo_automotor", "homicidio_siniestro_vial", "lesiones_segvial"]
types = dict(zip(tkeys, tvalues))


def main():
    try:
        print("Descargando...")
        frames = []
        for year in years:
            for month in months:
                for tv in tvalues:
                    response = request.urlopen(
                        BASE_URL.format(year, month, tv))
                    body = str(response.read(), "utf-8")
                    df = pd.read_csv(StringIO(body))
                    frames.append(df)
        df = pd.concat(frames)
        compression_opts = dict(method="zip", archive_name="delitos-caba.csv")
        df.to_csv("delitos-caba.zip", compression=compression_opts)
    except URLError as e:
        print(e.reason)


if __name__ == "__main__":
    main()
