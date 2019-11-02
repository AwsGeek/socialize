#!/usr/bin/env python3

from aws_cdk import core

from skamokawa.skamokawa_stack import SkamokawaStack


app = core.App()
SkamokawaStack(app, "skamokawa")

app.synth()
