# -*- coding: utf-8 -*-
"""
Created on Tue May 10 17:24:23 2016

@author: jenniferstark
"""

import logging
import logging.handlers


smtp_handler = logging.handlers.SMTPHandler(mailhost=("aspmx.l.google.com", 25),
                                            fromaddr="cjl.at.umd@gmail.com",
                                            toaddrs="jastark1@gmail.com",
                                            subject="GoogleScraper XPATH error!")



logger = logging.getLogger()
logger.addHandler(smtp_handler)

try: break
except Exception as e:
    logger.exception('Unhandled Exception')