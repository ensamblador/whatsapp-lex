#!/usr/bin/env python3

from aws_cdk import core

from whatsapp_lex.whatsapp_lex_stack import WhatsappLexStack


app = core.App()
WhatsappLexStack(app, "whatsapp-lex")

app.synth()
