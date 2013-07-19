#!/usr/bin/env python3
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

# WeCase -- This file defined constants and runtime constants.
# Copyright (C) 2013 Tom Li
# License: GPL v3 or later.


import sys
import os


APP_KEY = "1011524190"
APP_SECRET = "1898b3f668368b9f4a6f7ac8ed4a918f"
CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'
OAUTH2_PARAMETER = {'client_id': APP_KEY,
                    'response_type': 'code',
                    'redirect_uri': CALLBACK_URL,
                    'action': 'submit',
                    'userId': '',  # username
                    'passwd': '',  # password
                    'isLoginSina': 0,
                    'from': '',
                    'regCallback': '',
                    'state': '',
                    'ticket': '',
                    'withOfficalFlag': 0}

# TODO: Move it to the right place, rewrite Smiley.py
SMILES = {'good': 'ui/img/smiley/L6/good_thumb.gif',
          'ok': 'ui/img/smiley/L6/ok_thumb.gif',
          '不要': 'ui/img/smiley/L6/no_thumb.gif',
          '互粉': 'ui/img/smiley/L1/hufen_thumb.gif',
          '亲亲': 'ui/img/smiley/L3/qq_thumb.gif',
          '伤心': 'ui/img/smiley/L5/unheart.gif',
          '偷笑': 'ui/img/smiley/L3/heia_thumb.gif',
          '可怜': 'ui/img/smiley/L2/kl_thumb.gif',
          '可爱': 'ui/img/smiley/L2/tza_thumb.gif',
          '右哼哼': 'ui/img/smiley/L3/yhh_thumb.gif',
          '吃惊': 'ui/img/smiley/L2/cj_thumb.gif',
          '吐': 'ui/img/smiley/L3/t_thumb.gif',
          '呵呵': 'ui/img/smiley/L2/smilea_thumb.gif',
          '哈哈': 'ui/img/smiley/L2/laugh.gif',
          '哼': 'ui/img/smiley/L5/hatea_thumb.gif',
          '嘘': 'ui/img/smiley/L3/x_thumb.gif',
          '嘻嘻': 'ui/img/smiley/L2/tootha_thumb.gif',
          '囧': 'ui/img/smiley/L1/j_thumb.gif',
          '困': 'ui/img/smiley/L4/sleepya_thumb.gif',
          '围观': 'ui/img/smiley/L1/wg_thumb.gif',
          '太开心': 'ui/img/smiley/L3/mb_thumb.gif',
          '失望': 'ui/img/smiley/L4/sw_thumb.gif',
          '委屈': 'ui/img/smiley/L3/wq_thumb.gif',
          '害羞': 'ui/img/smiley/L2/shamea_thumb.gif',
          '左哼哼': 'ui/img/smiley/L3/zhh_thumb.gif',
          '弱': 'ui/img/smiley/L6/sad_thumb.gif',
          '心': 'ui/img/smiley/L5/hearta_thumb.gif',
          '怒': 'ui/img/smiley/L4/angrya_thumb.gif',
          '怒骂': 'ui/img/smiley/L5/nm_thumb.gif',
          '思考': 'ui/img/smiley/L4/sk_thumb.gif',
          '悲伤': 'ui/img/smiley/L5/bs_thumb.gif',
          '懒得理你': 'ui/img/smiley/L3/ldln_thumb.gif',
          '打哈欠': 'ui/img/smiley/L4/k_thumb.gif',
          '抓狂': 'ui/img/smiley/L5/crazya_thumb.gif',
          '抱抱': 'ui/img/smiley/L4/bba_thumb.gif',
          '拜拜': 'ui/img/smiley/L4/88_thumb.gif',
          '挖鼻屎': 'ui/img/smiley/L2/kbsa_thumb.gif',
          '挤眼': 'ui/img/smiley/L2/zy_thumb.gif',
          '晕': 'ui/img/smiley/L5/dizzya_thumb.gif',
          '来': 'ui/img/smiley/L6/come_thumb.gif',
          '汗': 'ui/img/smiley/L4/sweata_thumb.gif',
          '泪': 'ui/img/smiley/L3/sada_thumb.gif',
          '爱你': 'ui/img/smiley/L2/lovea_thumb.gif',
          '猪头': 'ui/img/smiley/L6/pig.gif',
          '生病': 'ui/img/smiley/L3/sb_thumb.gif',
          '疑问': 'ui/img/smiley/L4/yw_thumb.gif',
          '睡觉': 'ui/img/smiley/L4/sleepa_thumb.gif',
          '神马': 'ui/img/smiley/L1/horse2_thumb.gif',
          '耶': 'ui/img/smiley/L6/ye_thumb.gif',
          '花心': 'ui/img/smiley/L5/hsa_thumb.gif',
          '草泥马': 'ui/img/smiley/L1/shenshou_thumb.gif',
          '蛋糕': 'ui/img/smiley/L6/cake.gif',
          '蜡烛': 'ui/img/smiley/L6/lazu_thumb.gif',
          '衰': 'ui/img/smiley/L3/cry.gif',
          '话筒': 'ui/img/smiley/L6/m_thumb.gif',
          '赞': 'ui/img/smiley/L6/z2_thumb.gif',
          '鄙视': 'ui/img/smiley/L2/bs2_thumb.gif',
          '酷': 'ui/img/smiley/L5/cool_thumb.gif',
          '钟': 'ui/img/smiley/L6/clock_thumb.gif',
          '钱': 'ui/img/smiley/L4/money_thumb.gif',
          '闭嘴': 'ui/img/smiley/L2/bz_thumb.gif',
          '阴险': 'ui/img/smiley/L5/yx_thumb.gif',
          '馋嘴': 'ui/img/smiley/L4/cza_thumb.gif',
          '黑线': 'ui/img/smiley/L5/h_thumb.gif',
          '鼓掌': 'ui/img/smiley/L5/gza_thumb.gif'
}


try:
    # Users can define different $HOME.
    home_path = os.environ['HOME']
except KeyError:
    home_path = os.path.expanduser("~/")

config_path = home_path + '/.config/wecase/config_db'
cache_path = home_path + '/.cache/wecase/'
myself_name = sys.argv[0].split('/')[-1]
myself_path = os.path.dirname(os.path.realpath(__file__)) + '/'


def icon(name):
    return myself_path + "/icon/" + name
