import smtplib

class Email(object):

    def __init__(self, sender, password, recipient=None):
        '''
            Informações
            -----------
            sender:
                - email do usuário emissor
                - tipo string
            password:
                - senha do usuário emissor
                - tipo string
            recipient:
                - email do usuário receptor
                - tipo string
        '''
        self.sender = sender
        self.password = password
        self.recipient = recipient


    def send_mail(self, subject_matter, text_email):
        '''
            Informações
            -----------
            subject_matter:
                - assunto do email enviado
                - tipo string
            text_email:
                - texto que será enviado
                - tipo string
        '''
        msg = '\r\n'.join([
                'from: {}'.format(self.sender),
                'To: {}'.format(self.recipient),
                'Subject: {}'.format(subject_matter),
                '',
                '{}'.format(text_email)
            ]).encode(encoding='utf-8')

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(self.sender, self.password)
        server.sendmail(self.sender, self.recipient, msg)
        server.quit()