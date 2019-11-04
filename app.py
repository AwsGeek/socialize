#!/usr/bin/env python3

from aws_cdk import core

from socialize.socialize_stack import SocializeStack


app = core.App()
SocializeStack(app, "socialize")

app.synth()
