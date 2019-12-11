from urllib import parse

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from twilio.twiml.messaging_response import MessagingResponse
from string import punctuation

GREETINGS = [
    'bom dia',
    'boa tarde',
    'boa noite',
    'olá',
    'oi',
]


@require_http_methods(['POST', ])
@csrf_exempt
def bot_view(request):
    if request.method == 'POST':
        incoming_msg = request.body.decode('utf-8').split('&')[4]
        incoming_msg_parsed = parse.unquote(incoming_msg)[5:]
        incoming_msg_parsed = incoming_msg_parsed if incoming_msg_parsed[
                                                         -1] not in punctuation else incoming_msg_parsed[0:-1]
        if '+' in incoming_msg_parsed:
            incoming_msg_parsed = ' '.join(incoming_msg_parsed.split('+'))
        resp = MessagingResponse()
        msg = resp.message()
        responded = False
        if incoming_msg_parsed.lower() in GREETINGS:
            msg.body('Olá! Sou Fulano, o atendente virtual da clínica XXX. Tudo bem contigo? Em que posso ajudar?')
            responded = True
        else:
            msg.body('Desculpe, não entendi! Pode repetir?')
            responded = True
    return HttpResponse(f"{resp}")
