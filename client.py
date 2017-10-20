# coding=utf-8
import sys, socket, select
import time
from lxml import etree
from cStringIO import StringIO

class Student:

    STATIC_PATH = 'static/%s'

    def _connect(self):
        host = sys.argv[1]
        port = int(sys.argv[2])
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
        submit_message =  self.__prepareMessage('submeter', xml)
        self.s.send(submit_message)
        xml = self.s.recv(4096)

        while not xml:
            xml = self.s.recv(4096)

        xsd_filename = 'status_submeter.xsd'

        return self.__checkXmlStatus(xml, xsd_filename)

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
            print "Deu ruim"
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
print student.submit(xml)