import requests
import schedule
import time
import sys
import logging
from bs4 import BeautifulSoup


user = 'Coloque seu user aqui'
senha = 'Coloque sua senha aqui'

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) '
              '-30s: %(message)s')
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, stream=sys.stdout)
LOGGER = logging.getLogger(__name__)


class MytimesProvider:

    LOGGER = logging.getLogger(__name__)

    HOME_URL = 'https://mytimes.embratel.com.br:20443/MyTimes/'

    session = None

    def __init__(self, username=None, password=None):
        self.LOGGER.info('Logando')

        self.session = requests.session()
        self.session.verify = False

        response_home = self.session.get(self.HOME_URL)
        self.LOGGER.debug('Home Response: {}'.format(response_home.text))
        parsed_html = BeautifulSoup(response_home.text, 'lxml')

        view_state = parsed_html.find('input', attrs={'name': 'javax.faces.ViewState'}).attrs['value']
        self.LOGGER.debug('View State: {}'.format(view_state))

        payload = {'frmCadastro': 'frmCadastro', 'frmCadastro:email': username, 'frmCadastro:senha': password, 'frmCadastro:botaoLogin': '', 'javax.faces.ViewState': view_state}

        response_login = self.session.post(self.HOME_URL + '/Login2.xhtml', data=payload)
        self.LOGGER.debug("Login Response: {}".format(response_login.text))

    def marca_hora(self):
        self.LOGGER.info('Marcando')

        response_home = self.session.get(self.HOME_URL + 'RegistrarHorario.xhtml')
        self.LOGGER.debug('Marca HOME Response: {}'.format(response_home.text + 'RegistrarHorario.xhtml'))
        parsed_html = BeautifulSoup(response_home.text, 'lxml')

        view_state = parsed_html.find('input', attrs={'name': 'javax.faces.ViewState'}).attrs['value']
        self.LOGGER.debug('View State: {}'.format(view_state))

        payload = {'frmRegistro': 'frmRegistro', 'frmRegistro:inputJustificativa': '', 'frmRegistro:j_idt33': 'frmRegistro:j_idt33', 'javax.faces.ViewState': view_state}
        response = self.session.post(self.HOME_URL + 'RegistrarHorario.xhtml', data=payload)
        self.LOGGER.debug("Marca Response: {}".format(response.text))


def marca_hora():
    LOGGER.info('Iniciando marcacao de hora')
    provider = MytimesProvider(user, senha)
    provider.marca_hora()


if __name__ == '__main__':

    LOGGER.info('Ligando preenche horas')
    schedule.every().monday.at("10:00").do(marca_hora)
    schedule.every().monday.at("13:00").do(marca_hora)
    schedule.every().monday.at("14:00").do(marca_hora)
    schedule.every().monday.at("19:00").do(marca_hora)

    schedule.every().tuesday.at("10:00").do(marca_hora)
    schedule.every().tuesday.at("13:00").do(marca_hora)
    schedule.every().tuesday.at("14:00").do(marca_hora)
    schedule.every().tuesday.at("19:00").do(marca_hora)

    schedule.every().wednesday.at("10:00").do(marca_hora)
    schedule.every().wednesday.at("13:00").do(marca_hora)
    schedule.every().wednesday.at("14:00").do(marca_hora)
    schedule.every().wednesday.at("19:00").do(marca_hora)

    schedule.every().thursday.at("10:00").do(marca_hora)
    schedule.every().thursday.at("13:00").do(marca_hora)
    schedule.every().thursday.at("14:00").do(marca_hora)
    schedule.every().thursday.at("19:00").do(marca_hora)

    schedule.every().friday.at("10:00").do(marca_hora)
    schedule.every().friday.at("13:00").do(marca_hora)
    schedule.every().friday.at("14:00").do(marca_hora)
    schedule.every().friday.at("19:00").do(marca_hora)

    while True:
        schedule.run_pending()
        time.sleep(1)
