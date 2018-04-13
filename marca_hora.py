import smtplib
import urllib3
import requests
import schedule
import time
import sys
import logging
import datetime
from bs4 import BeautifulSoup
from smtplib import SMTPException


user = 'Coloque seu user aqui'
senha = 'Coloque sua senha aqui'
user_email = 'Coloque seu gmail aqui'
password_email = 'Coloque seu password gmail aqui'

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) '
              '-30s: %(message)s')
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, stream=sys.stdout)
LOGGER = logging.getLogger(__name__)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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


class SMTPProvider:

    LOGGER = logging.getLogger(__name__)

    server = None

    def __init__(self, user, password):
        try:
            self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            self.server.ehlo()
            self.server.login(user, password)
        except SMTPException as e:
            self.LOGGER.error("Erro ao se conectar no SMTP", e)

    def send_email(self, from_address, to_address, message):
        try:
            self.server.sendmail(from_address, to_address, message)
        except SMTPException as e:
            self.LOGGER.error("Erro ao enviar email", e)


def is_holyday(dt):
    r = requests.get('http://dadosbr.github.io/feriados/nacionais.json')
    dt1 = ('{:02d}'.format(dt.day) + '/' + '{:02d}'.format(dt.month))
    for elem in r.json():
        if dt1 == elem['date']:
            return True
    return False


def marca_hora(retry=4):
    LOGGER.info('Iniciando marcacao de hora')

    smtp_provider = None

    try:
        smtp_provider = SMTPProvider(user_email, password_email)
        if not is_holyday(datetime.datetime.now()):
            provider = MytimesProvider(user, senha)
            provider.marca_hora()

            logging.info('Hora Marcada com Sucesso!')
            smtp_provider.send_email(user_email, password_email,
                                     'Hora Marcada com Sucesso!')
        else:
            LOGGER.info('Feriado')
    except Exception as e:
        logging.error("Erro ao marcar hora", e)
        if retry > 0:
            logging.info("Tentando novamente em 10 segundos")
            time.sleep(10)
            retry = retry - 1
            marca_hora(retry)
        else:
            logging.info("Atingida a última tentativa")
            if smtp_provider is not None:
                smtp_provider.send_email(user_email, user_email,
                                         'Erro ao marcar hora')


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
