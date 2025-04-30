#!/usr/bin/env python3

import aws_cdk as cdk
from root_env_stack import RootEnvStack

# anl = AI Alliance Analytics Stack
application_ci = "anl"

app = cdk.App()

RootEnvStack(
    app,
    id=f"""{application_ci}-dev""",
    application_ci=application_ci,
    runtime_environment="dev",
)

# TODO: when we get additional AWS accounts for qa, prod...
'''
RootEnvStack(
    app,
    id=f"""{app_ci}-qa""",
    application_ci=app_ci,
    runtime_environment="qa",
)

RootEnvStack(
    app,
    id=f"""{app_ci}-prd""",
    application_ci=app_ci,
    runtime_environment="prd",
)
'''
app.synth()
