import sgs
import pandas as pd
import requests

results = sgs.search_ts("economica", language="pt")

data = pd.DataFrame(results, columns=['name', 'unit'])
#print(data)


from bcb import sgs
import bcb
from bcb import TaxaJuros
em = TaxaJuros()

from bcb import Expectativas

expec = Expectativas()
#print(expec.describe())

#expec.describe("ExpectativasMercadoAnuais")

ep = expec.get_endpoint("ExpectativasMercadoAnuais")
print(ep.query().filter(ep.Indicador ==
                  'Selic').collect())






