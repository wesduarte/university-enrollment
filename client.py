# coding=utf-8
import sys, socket, select
import time

class Student:
    def connect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(("localhost", 9008))


    def get_xml():
        return '<?xml version="1.0" encoding="UTF-8"?>'

    def check_status(self, cpf):
        pass

    def submit(self, xml):
        submit_message =  '<?xml version="1.0" >\n \
                <Request>\n \
                  <nome_metodo>submeter</nome_metodo>\n \
                  <parametro> <![CDATA[ %s ]]> </parametro>\n \
                  <tipo_retorno> int </tipo_retorno>\n \
                </Request>\n' % xml

        self.s.send(submit_message)
        data = self.s.recv(4096)
        while not data:
            data = self.s.recv(4096)

        return data


student = Student()
student.connect()
print student.submit('abcde')