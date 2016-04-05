#!/bin/sh
ENV=ENV
virtualenv $ENV
. $ENV/Scripts/activate
pip install -r requirements.txt
