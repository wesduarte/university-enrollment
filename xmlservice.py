# coding=utf-8
from lxml import etree
from cStringIO import StringIO

class XmlService:

    STATIC_PATH = 'static/%s'

    @staticmethod
    def getXmlAsString(xml_filename):
        xml_str = ''
        filepath = XmlService.STATIC_PATH % xml_filename
        with open(filepath) as xml:
            xml_str = xml.read()
        return xml_str

    @staticmethod
    def convertInvalidXml(xml_filename, xsl_filename):

        valid_xml = None
        xml_filepath = XmlService.STATIC_PATH % xml_filename
        with open(xml_filepath):
             dom = etree.parse(xml_filepath)

        xsl_filepath = XmlService.STATIC_PATH % xsl_filename
        with open(xsl_filepath):
            xslt = etree.parse(xsl_filepath)

        try:
            transform = etree.XSLT(xslt)
            newdom = transform(dom)
            valid_xml = etree.tostring(newdom, pretty_print=True)
        except:
            print "Erro ao converter XML"
        return valid_xml

    @staticmethod
    def checkXmlStatus(xml, xsd_filename):
        xsd = ''
        status = None
        filepath = XmlService.STATIC_PATH % xsd_filename
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

    @staticmethod
    def retrieve_consulta_status_value(xml):
        status_value = 0
        try:
            doc = etree.parse(StringIO(xml))
            request_elem = doc.getiterator().__next__()
            parameter_elem = request_elem.iterchildren().__next__().getnext()
            consultar_status_elem = parameter_elem.iterchildren().__next__()
            status_text = consultar_status_elem.text
        except:
            status_text = ''

        for i in status_text:
            if i.isdigit():
                status_value = int(i)
                break
        return status_value