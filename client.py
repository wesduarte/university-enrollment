# coding=utf-8
import sys, socket, select
import time
from lxml import etree
from cStringIO import StringIO

class Student:

    STATIC_PATH = 'static/%s'
    SUBMIT_STATUS_MESSAGES = ['sucesso', 'XML inválido', 'XML mal-formado', 'Erro Interno']
    CONSULT_STATUS_MESSAGES = ['Candidato não encontrado', 'Em processamento',
        'Candidato Aprovado e Selecionado',
        'Candidato Aprovado e em Espera',
        'Candidato Não Aprovado']

    def _connect(self):
        host = sys.argv[1]
        port = int(sys.argv[2])
        print "Conectando-se ao servidor %s:%s" % (host, port)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))

    def _getXml(self, xml_filename):
        parsed_xml = ''
        filepath = 'static/%s' % xml_filename
        with open(filepath) as xml:
            parsed_xml = xml.read()
        return parsed_xml

    def _convertInvalidXml(self, xml_filename):

        valid_xml = None
        xml_filepath = self.STATIC_PATH % xml_filename
        with open(xml_filepath):
            dom = etree.parse(xml_filepath)

        xsl_filename = 'transform_boletim.xsl'
        xsl_filepath = self.STATIC_PATH % xsl_filename
        with open(xsl_filepath):
            xslt = etree.parse(xsl_filepath)

        try:
            transform = etree.XSLT(xslt)
            newdom = transform(dom)
            result_xml = etree.tostring(newdom, pretty_print=True)
        except:
            print "deu ruim"
        return valid_xml

    def __prepareMessage(self, method_name, parameter_name):
        message = '<?xml version="1.0" encoding="utf-8" ?>\n \
            <request xmlns="https://www.w3schools.com">\n \
                <nome_metodo>%s</nome_metodo>\n \
                <parametro><![CDATA[ %s ]></parametro>\n \
                <tipo_retorno> int </tipo_retorno>\n \
            </request>\n' % (method_name, parameter_name)

        return message

    def submit(self, xml):

        if self.__checkXmlStatus(xml, 'boletim.xsd'):
            xml = self._convertInvalidXml('boletim.xml')
        #submit_message =  self.__prepareMessage('submeter', xml)
        submit_message = '<?xml version="1.0" encoding="utf-8" ?><request xmlns="https://www.w3schools.com"><nome_metodo>submeter</nome_metodo><parametro><![CDATA[<?xml version="1.0" encoding="utf-8" ?><boletim xmlns="https://www.w3schools.com"><informacao_pessoal><nome>flavio</nome><CPF>1234567890</CPF><matricula>1234567890</matricula><endereco>Rua Fulano da Silva</endereco><telefone>21123456789</telefone></informacao_pessoal><informacao_periodo><data>2017-02-16</data><cr_periodo>7</cr_periodo><materia><nome>comp I</nome><nota_final>9</nota_final><carga_horaria>40</carga_horaria><creditos>10</creditos><situacao_final>AP</situacao_final></materia><materia><nome>comp I</nome><nota_final>9</nota_final><carga_horaria>40</carga_horaria><creditos>10</creditos><situacao_final>AP</situacao_final></materia></informacao_periodo></boletim>]]></parametro><tipo_retorno>int</tipo_retorno></request>\n \0'
        self.s.send(submit_message)
        xml = self.s.recv(4096)

        while not xml:
            xml = self.s.recv(4096)

        xsd_filename = 'status_submeter.xsd'

        return self.__checkXmlStatus(xml, xsd_filename)

    def retrieve_consulta_status_value(self, xml):
        status_value = 0
        status_text = ''
        try:
            doc = etree.parse(StringIO(xml))
            request_elem = doc.getiterator().__next__()
            parameter_elem = request_elem.iterchildren().__next__().getnext()
            consultar_status_elem = parameter_elem.iterchildren().__next__()
            status_text = consultar_status_elem.text
        except:
            pass

        for i in status_text:
            if i.isdigit():
                status_value = int(i)
                break
        return status_value


    def consult_status(self, cpf):

        xml = '<?xml version="1.0" encoding="utf-8" ?>\n \
            <cpf xmlns="https://www.w3schools.com">00000000000</cpf>'
        #submit_message =  self.__prepareMessage('consulta', xml)
        submit_message = '<?xml version="1.0" encoding="utf-8" ?><request xmlns="https://www.w3schools.com"><nome_metodo>consulta</nome_metodo><parametro><![CDATA[<?xml version="1.0" encoding="utf-8" ?><cpf xmlns="https://www.w3schools.com">00000000000</cpf>]]></parametro><tipo_retorno>int</tipo_retorno></request> \n \0'
        self.s.send(submit_message)
        xml = self.s.recv(4096)

        while not xml:
            xml = self.s.recv(4096)

        xsd_filename = 'consultar_status.xsd'

        return self.retrieve_consulta_status_value(xml)

    def __checkXmlStatus(self, xml, xsd_filename):
        xsd = ''
        status = None
        filepath = self.STATIC_PATH % xsd_filename
        with open(filepath) as xsd_file:
            xsd = xsd_file.read()
        xmlschema_doc = etree.parse(StringIO(xsd))
        xmlschema = etree.XMLSchema(xmlschema_doc)

        # Parse XML
        try:
            doc = etree.parse(StringIO(xml))
        except IOError:
            status = 3
        except etree.XMLSyntaxError:
            status = 1

        if status:
            return status

        # Validate XML
        try:
            xmlschema.assertValid(doc)
            status = 0

        except etree.DocumentInvalid as err:
            status = 2

        except:
            status = 3

        return status

student = Student()
student._connect()

xml = student._getXml('boletim.xml')
print "Submetendo arquivo para o servidor"
print student.SUBMIT_STATUS_MESSAGES[student.submit(xml)]

cpf = '00000000000'
print "Consultando status do estudante de cpf = %s " % cpf
print student.CONSULT_STATUS_MESSAGES[student.consult_status(cpf)]

student.s.close()