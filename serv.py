#Auth WP Asura dev team
#RESTserver for fetching data from Thai national id card
#19/11/2018

from flask import Flask, Response
from flask_cors import CORS
from smartcard.CardConnection import CardConnection
from smartcard.CardType import AnyCardType
from smartcard.CardRequest import CardRequest
from smartcard.util import toHexString, toBytes
import json
import base64

tis620encoding = {

    32:' ',    #  0x20 -> SPACE
    33:'!',        #  0x21 -> EXCLAMATION MARK
    34:'"',        #  0x22 -> QUOTATION MARK
    35:'#',        #  0x23 -> NUMBER SIGN
    36:'$',        #  0x24 -> DOLLAR SIGN
    37:'%',        #  0x25 -> PERCENT SIGN
    38:'&',        #  0x26 -> AMPERSAND
    39:"'",        #  0x27 -> APOSTROPHE
    40:'(',        #  0x28 -> LEFT PARENTHESIS
    41:')',        #  0x29 -> RIGHT PARENTHESIS
    42:'*',        #  0x2A -> ASTERISK
    43:'+',        #  0x2B -> PLUS SIGN
    44:',',        #  0x2C -> COMMA
    45:'-',        #  0x2D -> HYPHEN-MINUS
    46:'.',        #  0x2E -> FULL STOP
    47:'/',        #  0x2F -> SOLIDUS
    48:'0',        #  0x30 -> DIGIT ZERO
    49:'1',        #  0x31 -> DIGIT ONE
    50:'2',        #  0x32 -> DIGIT TWO
    51:'3',        #  0x33 -> DIGIT THREE
    52:'4',        #  0x34 -> DIGIT FOUR
    53:'5',        #  0x35 -> DIGIT FIVE
    54:'6',        #  0x36 -> DIGIT SIX
    55:'7',        #  0x37 -> DIGIT SEVEN
    56:'8',        #  0x38 -> DIGIT EIGHT
    57:'9',        #  0x39 -> DIGIT NINE
    58:':',        #  0x3A -> COLON
    59:';',        #  0x3B -> SEMICOLON
    60:'<',        #  0x3C -> LESS-THAN SIGN
    61:'=',        #  0x3D -> EQUALS SIGN
    62:'>',        #  0x3E -> GREATER-THAN SIGN
    63:'?',        #  0x3F -> QUESTION MARK
    64:'@',        #  0x40 -> COMMERCIAL AT
    65:'A',        #  0x41 -> LATIN CAPITAL LETTER A
    66:'B',        #  0x42 -> LATIN CAPITAL LETTER B
    67:'C',        #  0x43 -> LATIN CAPITAL LETTER C
    68:'D',        #  0x44 -> LATIN CAPITAL LETTER D
    69:'E',        #  0x45 -> LATIN CAPITAL LETTER E
    70:'F',        #  0x46 -> LATIN CAPITAL LETTER F
    71:'G',        #  0x47 -> LATIN CAPITAL LETTER G
    72:'H',        #  0x48 -> LATIN CAPITAL LETTER H
    73:'I',        #  0x49 -> LATIN CAPITAL LETTER I
    74:'J',        #  0x4A -> LATIN CAPITAL LETTER J
    75:'K',        #  0x4B -> LATIN CAPITAL LETTER K
    76:'L',        #  0x4C -> LATIN CAPITAL LETTER L
    77:'M',        #  0x4D -> LATIN CAPITAL LETTER M
    78:'N',        #  0x4E -> LATIN CAPITAL LETTER N
    79:'O',        #  0x4F -> LATIN CAPITAL LETTER O
    80:'P',        #  0x50 -> LATIN CAPITAL LETTER P
    81:'Q',        #  0x51 -> LATIN CAPITAL LETTER Q
    82:'R',        #  0x52 -> LATIN CAPITAL LETTER R
    83:'S',        #  0x53 -> LATIN CAPITAL LETTER S
    84:'T',        #  0x54 -> LATIN CAPITAL LETTER T
    85:'U',        #  0x55 -> LATIN CAPITAL LETTER U
    86:'V',        #  0x56 -> LATIN CAPITAL LETTER V
    87:'W',        #  0x57 -> LATIN CAPITAL LETTER W
    88:'X',        #  0x58 -> LATIN CAPITAL LETTER X
    89:'Y',        #  0x59 -> LATIN CAPITAL LETTER Y
    90:'Z',        #  0x5A -> LATIN CAPITAL LETTER Z
    91:'[',        #  0x5B -> LEFT SQUARE BRACKET
    92:'\\',       #  0x5C -> REVERSE SOLIDUS
    93:']',        #  0x5D -> RIGHT SQUARE BRACKET
    94:'^',        #  0x5E -> CIRCUMFLEX ACCENT
    95:'_',        #  0x5F -> LOW LINE
    96:'`',        #  0x60 -> GRAVE ACCENT
    97:'a',        #  0x61 -> LATIN SMALL LETTER A
    98:'b',        #  0x62 -> LATIN SMALL LETTER B
    99:'c',        #  0x63 -> LATIN SMALL LETTER C
    100:'d',        #  0x64 -> LATIN SMALL LETTER D
    101:'e',        #  0x65 -> LATIN SMALL LETTER E
    102:'f',        #  0x66 -> LATIN SMALL LETTER F
    103:'g',        #  0x67 -> LATIN SMALL LETTER G
    104:'h',        #  0x68 -> LATIN SMALL LETTER H
    105:'i',        #  0x69 -> LATIN SMALL LETTER I
    106:'j',        #  0x6A -> LATIN SMALL LETTER J
    107:'k',        #  0x6B -> LATIN SMALL LETTER K
    108:'l',        #  0x6C -> LATIN SMALL LETTER L
    109:'m',        #  0x6D -> LATIN SMALL LETTER M
    110:'n',        #  0x6E -> LATIN SMALL LETTER N
    111:'o',        #  0x6F -> LATIN SMALL LETTER O
    112:'p',        #  0x70 -> LATIN SMALL LETTER P
    113:'q',        #  0x71 -> LATIN SMALL LETTER Q
    114:'r',        #  0x72 -> LATIN SMALL LETTER R
    115:'s',        #  0x73 -> LATIN SMALL LETTER S
    116:'t',        #  0x74 -> LATIN SMALL LETTER T
    117:'u',        #  0x75 -> LATIN SMALL LETTER U
    118:'v',        #  0x76 -> LATIN SMALL LETTER V
    119:'w',        #  0x77 -> LATIN SMALL LETTER W
    120:'x',        #  0x78 -> LATIN SMALL LETTER X
    121:'y',        #  0x79 -> LATIN SMALL LETTER Y
    122:'z',        #  0x7A -> LATIN SMALL LETTER Z
    123:'{',        #  0x7B -> LEFT CURLY BRACKET
    124:'|',        #  0x7C -> VERTICAL LINE
    125:'}',        #  0x7D -> RIGHT CURLY BRACKET
    126:'~',        #  0x7E -> TILDE

    161:'\u0e01',   #  0xA1 -> THAI CHARACTER KO KAI
    162:'\u0e02',   #  0xA2 -> THAI CHARACTER KHO KHAI
    163:'\u0e03',   #  0xA3 -> THAI CHARACTER KHO KHUAT
    164:'\u0e04',   #  0xA4 -> THAI CHARACTER KHO KHWAI
    165:'\u0e05',   #  0xA5 -> THAI CHARACTER KHO KHON
    166:'\u0e06',   #  0xA6 -> THAI CHARACTER KHO RAKHANG
    167:'\u0e07',   #  0xA7 -> THAI CHARACTER NGO NGU
    168:'\u0e08',   #  0xA8 -> THAI CHARACTER CHO CHAN
    169:'\u0e09',   #  0xA9 -> THAI CHARACTER CHO CHING
    170:'\u0e0a',   #  0xAA -> THAI CHARACTER CHO CHANG
    171:'\u0e0b',   #  0xAB -> THAI CHARACTER SO SO
    172:'\u0e0c',   #  0xAC -> THAI CHARACTER CHO CHOE
    173:'\u0e0d',   #  0xAD -> THAI CHARACTER YO YING
    174:'\u0e0e',   #  0xAE -> THAI CHARACTER DO CHADA
    175:'\u0e0f',   #  0xAF -> THAI CHARACTER TO PATAK
    176:'\u0e10',   #  0xB0 -> THAI CHARACTER THO THAN
    177:'\u0e11',   #  0xB1 -> THAI CHARACTER THO NANGMONTHO
    178:'\u0e12',   #  0xB2 -> THAI CHARACTER THO PHUTHAO
    179:'\u0e13',   #  0xB3 -> THAI CHARACTER NO NEN
    180:'\u0e14',   #  0xB4 -> THAI CHARACTER DO DEK
    181:'\u0e15',   #  0xB5 -> THAI CHARACTER TO TAO
    182:'\u0e16',   #  0xB6 -> THAI CHARACTER THO THUNG
    183:'\u0e17',   #  0xB7 -> THAI CHARACTER THO THAHAN
    184:'\u0e18',   #  0xB8 -> THAI CHARACTER THO THONG
    185:'\u0e19',   #  0xB9 -> THAI CHARACTER NO NU
    186:'\u0e1a',   #  0xBA -> THAI CHARACTER BO BAIMAI
    187:'\u0e1b',   #  0xBB -> THAI CHARACTER PO PLA
    188:'\u0e1c',   #  0xBC -> THAI CHARACTER PHO PHUNG
    189:'\u0e1d',   #  0xBD -> THAI CHARACTER FO FA
    190:'\u0e1e',   #  0xBE -> THAI CHARACTER PHO PHAN
    191:'\u0e1f',   #  0xBF -> THAI CHARACTER FO FAN
    192:'\u0e20',   #  0xC0 -> THAI CHARACTER PHO SAMPHAO
    193:'\u0e21',   #  0xC1 -> THAI CHARACTER MO MA
    194:'\u0e22',   #  0xC2 -> THAI CHARACTER YO YAK
    195:'\u0e23',   #  0xC3 -> THAI CHARACTER RO RUA
    196:'\u0e24',   #  0xC4 -> THAI CHARACTER RU
    197:'\u0e25',   #  0xC5 -> THAI CHARACTER LO LING
    198:'\u0e26',   #  0xC6 -> THAI CHARACTER LU
    199:'\u0e27',   #  0xC7 -> THAI CHARACTER WO WAEN
    200:'\u0e28',   #  0xC8 -> THAI CHARACTER SO SALA
    201:'\u0e29',   #  0xC9 -> THAI CHARACTER SO RUSI
    202:'\u0e2a',   #  0xCA -> THAI CHARACTER SO SUA
    203:'\u0e2b',   #  0xCB -> THAI CHARACTER HO HIP
    204:'\u0e2c',   #  0xCC -> THAI CHARACTER LO CHULA
    205:'\u0e2d',   #  0xCD -> THAI CHARACTER O ANG
    206:'\u0e2e',   #  0xCE -> THAI CHARACTER HO NOKHUK
    207:'\u0e2f',   #  0xCF -> THAI CHARACTER PAIYANNOI
    208:'\u0e30',   #  0xD0 -> THAI CHARACTER SARA A
    209:'\u0e31',   #  0xD1 -> THAI CHARACTER MAI HAN-AKAT
    210:'\u0e32',   #  0xD2 -> THAI CHARACTER SARA AA
    211:'\u0e33',   #  0xD3 -> THAI CHARACTER SARA AM
    212:'\u0e34',   #  0xD4 -> THAI CHARACTER SARA I
    213:'\u0e35',   #  0xD5 -> THAI CHARACTER SARA II
    214:'\u0e36',   #  0xD6 -> THAI CHARACTER SARA UE
    215:'\u0e37',   #  0xD7 -> THAI CHARACTER SARA UEE
    216:'\u0e38',   #  0xD8 -> THAI CHARACTER SARA U
    217:'\u0e39',   #  0xD9 -> THAI CHARACTER SARA UU
    218:'\u0e3a',   #  0xDA -> THAI CHARACTER PHINTHU

    223:'\u0e3f',   #  0xDF -> THAI CURRENCY SYMBOL BAHT
    224:'\u0e40',   #  0xE0 -> THAI CHARACTER SARA E
    225:'\u0e41',   #  0xE1 -> THAI CHARACTER SARA AE
    226:'\u0e42',   #  0xE2 -> THAI CHARACTER SARA O
    227:'\u0e43',   #  0xE3 -> THAI CHARACTER SARA AI MAIMUAN
    228:'\u0e44',   #  0xE4 -> THAI CHARACTER SARA AI MAIMALAI
    229:'\u0e45',   #  0xE5 -> THAI CHARACTER LAKKHANGYAO
    230:'\u0e46',   #  0xE6 -> THAI CHARACTER MAIYAMOK
    231:'\u0e47',   #  0xE7 -> THAI CHARACTER MAITAIKHU
    232:'\u0e48',   #  0xE8 -> THAI CHARACTER MAI EK
    233:'\u0e49',   #  0xE9 -> THAI CHARACTER MAI THO
    234:'\u0e4a',   #  0xEA -> THAI CHARACTER MAI TRI
    235:'\u0e4b',   #  0xEB -> THAI CHARACTER MAI CHATTAWA
    236:'\u0e4c',   #  0xEC -> THAI CHARACTER THANTHAKHAT
    237:'\u0e4d',   #  0xED -> THAI CHARACTER NIKHAHIT
    238:'\u0e4e',   #  0xEE -> THAI CHARACTER YAMAKKAN
    239:'\u0e4f',   #  0xEF -> THAI CHARACTER FONGMAN
    240:'\u0e50',   #  0xF0 -> THAI DIGIT ZERO
    241:'\u0e51',   #  0xF1 -> THAI DIGIT ONE
    242:'\u0e52',   #  0xF2 -> THAI DIGIT TWO
    243:'\u0e53',   #  0xF3 -> THAI DIGIT THREE
    244:'\u0e54',   #  0xF4 -> THAI DIGIT FOUR
    245:'\u0e55',   #  0xF5 -> THAI DIGIT FIVE
    246:'\u0e56',   #  0xF6 -> THAI DIGIT SIX
    247:'\u0e57',   #  0xF7 -> THAI DIGIT SEVEN
    248:'\u0e58',   #  0xF8 -> THAI DIGIT EIGHT
    249:'\u0e59',   #  0xF9 -> THAI DIGIT NINE
    250:'\u0e5a',   #  0xFA -> THAI CHARACTER ANGKHANKHU
    251:'\u0e5b'   #  0xFB -> THAI CHARACTER KHOMUT

}

SELECT = [0x00, 0xA4, 0x04, 0x00, 0x08]
THAI_ID_CARD = [0xA0, 0x00, 0x00, 0x00, 0x54, 0x48, 0x00, 0x01]

app = Flask(__name__)
CORS(app)

#Getting status
@app.route('/get_status')
def get_status():
    ##header("Content-type: application/json")
    cardtype = AnyCardType()
    cardrequest = CardRequest( timeout=1, cardType=cardtype )
    try:
        cardservice = cardrequest.waitforcard()
    except:
        resultdict = {
            'status':'inactive'
        }
        return json.dumps(resultdict)

    resultdict = {
        'status':'active'
    }
    return Response(json.dumps(resultdict), mimetype='application/json')



#Start get_data
@app.route('/get_data')
def get_data():
    cardtype = AnyCardType()
    cardrequest = CardRequest( timeout=1, cardType=cardtype )

    try:
        cardservice = cardrequest.waitforcard()
    except:
        resultdict = {
            'status':'inactive'
        }
        return json.dumps(resultdict)

    stat = cardservice.connection.connect()

    REQ_CID = [0x80, 0xb0, 0x00, 0x04, 0x02, 0x00, 0x0d]
    REQ_THAI_NAME = [0x80, 0xb0, 0x00, 0x11, 0x02, 0x00, 0x64]
    REQ_ENG_NAME = [0x80, 0xb0, 0x00, 0x75, 0x02, 0x00, 0x64]
    REQ_GENDER = [0x80, 0xb0, 0x00, 0xE1, 0x02, 0x00, 0x01]
    REQ_DOB = [0x80, 0xb0, 0x00, 0xD9, 0x02, 0x00, 0x08]
    REQ_ADDRESS = [0x80, 0xb0, 0x15, 0x79, 0x02, 0x00, 0x64]
    REQ_ISSUE_EXPIRE = [0x80, 0xb0, 0x01, 0x67, 0x02, 0x00, 0x0C]

    DATA = [REQ_CID,REQ_THAI_NAME,REQ_ENG_NAME,REQ_GENDER,REQ_DOB,
    REQ_ADDRESS,REQ_ISSUE_EXPIRE]

    apdu = SELECT+THAI_ID_CARD
    response, sw1, sw2 = cardservice.connection.transmit( apdu )

    resultlist = list();

    for d in DATA:
        response, sw1, sw2 = cardservice.connection.transmit( d )
        if sw1 == 0x61:
            GET_RESPONSE = [0X00, 0XC0, 0x00, 0x00 ]
            apdu = GET_RESPONSE + [sw2]
            response, sw1, sw2 = cardservice.connection.transmit( apdu )
            result = ''
            for i in response:
                result = result + tis620encoding[i]
            resultlist.append(result)

    resultdict = {
        'status':'active',
        'idnumber':resultlist[0],
        'thainame':resultlist[1],
        'englishname':resultlist[2],
        'gender':resultlist[3],
        'dob':resultlist[4],
        'address':resultlist[5],
        'issueexpire':resultlist[6]
    }
    return Response(json.dumps(resultdict), mimetype='application/json')
#End get_data

#Start get_photo
@app.route('/get_photo_byte')
def get_photo_byte():
    cardtype = AnyCardType()
    cardrequest = CardRequest( timeout=1, cardType=cardtype )

    try:
        cardservice = cardrequest.waitforcard()
    except:
        resultdict = {
            'status':'inactive'
        }
        return json.dumps(resultdict)

    cardservice.connection.connect()

    REQ_PHOTO_P1 = [0x80,0xB0,0x01,0x7B,0x02,0x00,0xFF]
    REQ_PHOTO_P2 = [0x80,0xB0,0x02,0x7A,0x02,0x00,0xFF]
    REQ_PHOTO_P3 = [0x80,0xB0,0x03,0x79,0x02,0x00,0xFF]
    REQ_PHOTO_P4 = [0x80,0xB0,0x04,0x78,0x02,0x00,0xFF]
    REQ_PHOTO_P5 = [0x80,0xB0,0x05,0x77,0x02,0x00,0xFF]
    REQ_PHOTO_P6 = [0x80,0xB0,0x06,0x76,0x02,0x00,0xFF]
    REQ_PHOTO_P7 = [0x80,0xB0,0x07,0x75,0x02,0x00,0xFF]
    REQ_PHOTO_P8 = [0x80,0xB0,0x08,0x74,0x02,0x00,0xFF]
    REQ_PHOTO_P9 = [0x80,0xB0,0x09,0x73,0x02,0x00,0xFF]
    REQ_PHOTO_P10 = [0x80,0xB0,0x0A,0x72,0x02,0x00,0xFF]
    REQ_PHOTO_P11 = [0x80,0xB0,0x0B,0x71,0x02,0x00,0xFF]
    REQ_PHOTO_P12 = [0x80,0xB0,0x0C,0x70,0x02,0x00,0xFF]
    REQ_PHOTO_P13 = [0x80,0xB0,0x0D,0x6F,0x02,0x00,0xFF]
    REQ_PHOTO_P14 = [0x80,0xB0,0x0E,0x6E,0x02,0x00,0xFF]
    REQ_PHOTO_P15 = [0x80,0xB0,0x0F,0x6D,0x02,0x00,0xFF]
    REQ_PHOTO_P16 = [0x80,0xB0,0x10,0x6C,0x02,0x00,0xFF]
    REQ_PHOTO_P17 = [0x80,0xB0,0x11,0x6B,0x02,0x00,0xFF]
    REQ_PHOTO_P18 = [0x80,0xB0,0x12,0x6A,0x02,0x00,0xFF]
    REQ_PHOTO_P19 = [0x80,0xB0,0x13,0x69,0x02,0x00,0xFF]
    REQ_PHOTO_P20 = [0x80,0xB0,0x14,0x68,0x02,0x00,0xFF]

    PHOTO = [REQ_PHOTO_P1,REQ_PHOTO_P2,REQ_PHOTO_P3,REQ_PHOTO_P4,REQ_PHOTO_P5,
    REQ_PHOTO_P6,REQ_PHOTO_P7,REQ_PHOTO_P8,REQ_PHOTO_P9,REQ_PHOTO_P10,REQ_PHOTO_P11
    ,REQ_PHOTO_P12,REQ_PHOTO_P13,REQ_PHOTO_P14,REQ_PHOTO_P15,REQ_PHOTO_P16,REQ_PHOTO_P17,
    REQ_PHOTO_P18,REQ_PHOTO_P19,REQ_PHOTO_P20]

    photobytearray = bytearray();

    apdu = SELECT+THAI_ID_CARD
    response, sw1, sw2 = cardservice.connection.transmit( apdu )

    for d in PHOTO:
        response, sw1, sw2 = cardservice.connection.transmit( d )
        if sw1 == 0x61:
            GET_RESPONSE = [0X00, 0XC0, 0x00, 0x00 ]
            apdu = GET_RESPONSE + [sw2]
            response, sw1, sw2 = cardservice.connection.transmit( apdu )
            photobytearray.extend(bytearray(response))

    return photobytearray

#End get_photo

#Start get_photo
@app.route('/get_photo_json')
def get_photo_json():
    cardtype = AnyCardType()
    cardrequest = CardRequest( timeout=1, cardType=cardtype )
    cardservice = cardrequest.waitforcard()
    cardservice.connection.connect()

    REQ_PHOTO_P1 = [0x80,0xB0,0x01,0x7B,0x02,0x00,0xFF]
    REQ_PHOTO_P2 = [0x80,0xB0,0x02,0x7A,0x02,0x00,0xFF]
    REQ_PHOTO_P3 = [0x80,0xB0,0x03,0x79,0x02,0x00,0xFF]
    REQ_PHOTO_P4 = [0x80,0xB0,0x04,0x78,0x02,0x00,0xFF]
    REQ_PHOTO_P5 = [0x80,0xB0,0x05,0x77,0x02,0x00,0xFF]
    REQ_PHOTO_P6 = [0x80,0xB0,0x06,0x76,0x02,0x00,0xFF]
    REQ_PHOTO_P7 = [0x80,0xB0,0x07,0x75,0x02,0x00,0xFF]
    REQ_PHOTO_P8 = [0x80,0xB0,0x08,0x74,0x02,0x00,0xFF]
    REQ_PHOTO_P9 = [0x80,0xB0,0x09,0x73,0x02,0x00,0xFF]
    REQ_PHOTO_P10 = [0x80,0xB0,0x0A,0x72,0x02,0x00,0xFF]
    REQ_PHOTO_P11 = [0x80,0xB0,0x0B,0x71,0x02,0x00,0xFF]
    REQ_PHOTO_P12 = [0x80,0xB0,0x0C,0x70,0x02,0x00,0xFF]
    REQ_PHOTO_P13 = [0x80,0xB0,0x0D,0x6F,0x02,0x00,0xFF]
    REQ_PHOTO_P14 = [0x80,0xB0,0x0E,0x6E,0x02,0x00,0xFF]
    REQ_PHOTO_P15 = [0x80,0xB0,0x0F,0x6D,0x02,0x00,0xFF]
    REQ_PHOTO_P16 = [0x80,0xB0,0x10,0x6C,0x02,0x00,0xFF]
    REQ_PHOTO_P17 = [0x80,0xB0,0x11,0x6B,0x02,0x00,0xFF]
    REQ_PHOTO_P18 = [0x80,0xB0,0x12,0x6A,0x02,0x00,0xFF]
    REQ_PHOTO_P19 = [0x80,0xB0,0x13,0x69,0x02,0x00,0xFF]
    REQ_PHOTO_P20 = [0x80,0xB0,0x14,0x68,0x02,0x00,0xFF]

    PHOTO = [REQ_PHOTO_P1,REQ_PHOTO_P2,REQ_PHOTO_P3,REQ_PHOTO_P4,REQ_PHOTO_P5,
    REQ_PHOTO_P6,REQ_PHOTO_P7,REQ_PHOTO_P8,REQ_PHOTO_P9,REQ_PHOTO_P10,REQ_PHOTO_P11
    ,REQ_PHOTO_P12,REQ_PHOTO_P13,REQ_PHOTO_P14,REQ_PHOTO_P15,REQ_PHOTO_P16,REQ_PHOTO_P17,
    REQ_PHOTO_P18,REQ_PHOTO_P19,REQ_PHOTO_P20]

    resultdict = dict()
    photobytearray = list()

    apdu = SELECT+THAI_ID_CARD
    response, sw1, sw2 = cardservice.connection.transmit( apdu )

    for d in PHOTO:
        response, sw1, sw2 = cardservice.connection.transmit( d )
        if sw1 == 0x61:
            GET_RESPONSE = [0X00, 0XC0, 0x00, 0x00 ]
            apdu = GET_RESPONSE + [sw2]
            response, sw1, sw2 = cardservice.connection.transmit( apdu )

            for i in response:
                photobytearray.append(i)

    resultdict = {
        'status':'active',
        'photo':photobytearray
    }

    return Response(json.dumps(resultdict), mimetype='application/json')
#End get_photo
