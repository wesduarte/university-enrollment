# coding=utf-8
import sys, socket, select
import time
from lxml import etree
from cStringIO import StringIO

class Student:
    def _connect(self):
        host = sys.argv[1]
        port = int(sys.argv[2])
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))


    def _getXml(self, xml_filename):
        parsed_xml = ''
        filepath = 'static/%s' % xml_filename
        with open(filepath) as xml:
            parsed_xml = xml.read().replace("\n", "")
        return parsed_xml

    def __prepareMessage(self, xml):
        message =  '<?xml version="1.0" >\n \
                <Request>\n \
                  <nome_metodo>submeter</nome_metodo>\n \
                  <parametro> <![CDATA[ %s ]]> </parametro>\n \
                  <tipo_retorno> int </tipo_retorno>\n \
                </Request>\n' % xml
        return message

    def submit(self, xml):
        submit_message =  self.__prepareMessage(xml)
        self.s.send(submit_message)
        xml = self.s.recv(4096)

        while not xml:
            xml = self.s.recv(4096)

        xsd_filename = 'status_submeter.xsd'

        return self.__checkXmlStatus(xml, xsd_filename)

    def __checkXmlStatus(self, xml, xsd_filename):
        xsd = ''
        status = None
        filepath = 'static/%s' % xsd_filename
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

    def convertInvalidXml(self, xml_filename, xslt_filename):
        newXml = None
        xml_filepath = 'static/%s' % xml_filename
        xslt_filepath = 'static/%s' % xslt_filename

        with open(xml_filepath) as xml_file:
            xml = etree.parse(xml_filename)

        with open(xslt_filepath) as xslt_file:
            xslt = etree.parse(xslt_filename)
            transform = etree.XSLT(xslt)
            newXml = transform(xml)

        return newXml


student = Student()
student._connect()
xml = student._getXml('boletim.xml')
print student.submit(xml)