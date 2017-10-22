# coding=utf-8
import sys, socket, select
import time
from xmlservice import XmlService

class Student:

    SUBMIT_STATUS_MESSAGES = ['sucesso', 'XML inválido',
        'XML mal-formado', 'Erro Interno']
    CONSULT_STATUS_MESSAGES = ['Candidato não encontrado', 'Em processamento',
        'Candidato Aprovado e Selecionado',
        'Candidato Aprovado e em Espera',
        'Candidato Não Aprovado']

    def _connect(self):
        host = sys.argv[1]
        port = int(sys.argv[2])
        print "Concetando-se ao servidor %s:%s" % (host, port)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))

    def __prepareMessage(self, method_name, parameter_name):
        message = '<?xml version="1.0" encoding="utf-8" ?>\n \
            <request xmlns="https://www.w3schools.com">\n \
                <nome_metodo>%s</nome_metodo>\n \
                <parametro><![CDATA[ %s ]></parametro>\n \
                <tipo_retorno> int </tipo_retorno>\n \
            </request>\n' % (method_name, parameter_name)

        return message

    def submit(self, xml):

        if XmlService.checkXmlStatus(xml, 'boletim.xsd'):
            xml = XmlService.convertInvalidXml('boletim.xml',
                'transform_boletim.xsl')

        submit_message =  self.__prepareMessage('submeter', xml)
        self.s.send(submit_message)
        xml = self.s.recv(4096)

        while not xml:
            xml = self.s.recv(4096)

        xsd_filename = 'status_submeter.xsd'

        return XmlService.checkXmlStatus(xml, xsd_filename)

    def consult_status(self, cpf):

        xml = '<?xml version="1.0" encoding="utf-8" ?>\n \
            <cpf xmlns="https://www.w3schools.com">00000000000</cpf>'
        submit_message =  self.__prepareMessage('consulta', xml)
        self.s.send(submit_message)
        xml = self.s.recv(4096)

        while not xml:
            xml = self.s.recv(4096)

        xsd_filename = 'consultar_status.xsd'

        return XmlService.retrieve_consulta_status_value(xml)


student = Student()
student._connect()

xml = XmlService.getXmlAsString('boletim.xml')
print "Submetendo arquivo para o servidor"
print student.SUBMIT_STATUS_MESSAGES[student.submit(xml)]

cpf = '00000000000'
print "Consultando status do estudante de cpf = %s " % cpf
print student.CONSULT_STATUS_MESSAGES[student.consult_status(cpf)]

student.s.close()
