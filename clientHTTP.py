#!/usr/bin/env python
#by Karla Garcia

# Modulos de python
import argparse
import socket
import sys
from argparse import RawTextHelpFormatter
from platform import system as sysBase

user_agent_option = {1: "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36", 
                     2: "Mozilla/5.0 (X11; Linux i686; rv:45.0) Gecko/20100101 Firefox/45.0",
                     3: "Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16"}


def proccessArguments():
        """
        Procesa los argumentos recibidos en la linea de comandos
        """
        if(sysBase() == 'Linux'):
                uadef = 2
        else:
                uadef = 1
        args = argparse.ArgumentParser(description='clientHTTP', formatter_class=RawTextHelpFormatter)
        args.add_argument('-m', action = 'store', dest = 'method', 
                          choices = ('GET', 'HEAD'),
                          default = 'GET', 
                          help = 'Metodo de HTTP que se usara para la solicitud')
        args.add_argument('-u', action = 'store', dest = 'url', 
                          default = '/', 
                          help = 'Recurso a solicitar al servidor web')
        args.add_argument('-a', action = 'store', dest = 'user_agent',
                          choices = user_agent_option, type = int, 
                          default = uadef,
                          help = 'User Agent\n\t1: ' + user_agent_option.get(1) + 
                          '\n\t2: ' + user_agent_option.get(2) + 
                          '\n\t3: ' + user_agent_option.get(3))
        args.add_argument('-e', action = 'store', dest = 'encoding', 
                          default = 'identity', 
                          choices = ('gzip', 'deflate', 'identity'), 
                          help = 'Parametro de la solicitud de la codificacion de la respuesta')
        args.add_argument('-c', action = 'store', dest = 'connection',
                          default = 'close',
                          choices = ('keep-alive', 'close'), 
                          help = 'Forma de establecimiento de la conexion')
        
        reqArgs = args.add_argument_group('required arguments')
        reqArgs.add_argument('-H', action = 'store', dest = 'host', 
                             required = True, 
                             help = 'IP del servidor HTTP o nombre de dominio')
        if(len(sys.argv) == 1):
                args.parse_args(['-h'])               
        return args.parse_args()


def constructHTTPRequest(args):
        """
        Cosntruccion de HTTP request 
        """
        #Valores fijos
        version = "HTTP/1.1"
        accept = "Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8"
        accept_charset = "Accept-Charset: utf-8, iso-8859-1;q=0.5"
        accept_language = "Accept-Language: en-US"
        blank_line = "\r\n"

        #Request line
        request_line = args.method + " " + args.url + " " + version + blank_line

        #Construccion de HTTP header lines

        # cada parametro debe terminar con un retorno de carro y un salto de linea
        header_lines = 'Host: ' + args.host + blank_line + \
                       'User-Agent: ' + user_agent_option.get(args.user_agent) + blank_line + \
                       accept + blank_line + \
                       accept_language + blank_line + \
                       'Accept-Encoding: ' + args.encoding + blank_line + \
                       accept_charset + blank_line + \
                       'Connection: ' + args.connection + blank_line
        #La peticion de HTTP debe terminar con un retorno de carro y un salto de linea

        #concatenacion de cada parametro para construir la peticion de HTTP
        HTTP_request = request_line + \
                       header_lines + \
                       blank_line
        #print HTTP_request
        return HTTP_request

def TCPconnection(host_server, HTTP_request):	
        # Crea un socket de TCP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	
        # Conexion del cliente al servidor dado,
        # en el puerto 80 para HTTP
        s.connect((host_server, 80))
        # Envia la peticion HTTP al servidor
        s.send(HTTP_request)
        #Mientras reciba informacion del servidor, la guardara en HTTP_response, e imprimira en pantalla
        while True:
                HTTP_response = s.recv(1024)
                if HTTP_response == "" :break
                #os.system('chrome ' + HTTP_response)
                print HTTP_response,
                # Una vez que la recepcion de informacion ha terminado
                # Se cierra la conexcion con el servidor
                print "\n\nConexion con el servidor finalizada\n"
                

       

def main():        
        arguments = proccessArguments()
        HTTP_request = constructHTTPRequest(arguments)
        try:
                TCPconnection(arguments.host, HTTP_request)
        except:
                print 'Imposible alcanzar:', arguments.host, "por favor verique la url."
                
        
        
        
	
if __name__ == "__main__":
        main()

