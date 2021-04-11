import json, os
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from .models import *
from .methods import requests
import datetime
from django.core.serializers.json import DjangoJSONEncoder
import random
import string


def unique_z_code(z_code):
    for registration in Registrations.objects.all():
        if registration.z_code == z_code:
            return False
    return True


def generate_z_code():
    z_code = False
    while True:
        z_code = "Z21-" + str(
            "".join(random.choices(string.digits, k=4))
            + str("".join(random.choices(["A", "B", "C", "D", "E", "F"], k=2)))
        )
        if unique_z_code(z_code):
            break
    return z_code


def z_code_handle(email, name):
    z_code = False

    for registration in Registrations.objects.all():
        if registration.email == email:
            z_code = registration.z_code

    if z_code == False:
        z_code = generate_z_code()
        Registrations.objects.create(name=name, email=email, z_code=z_code)

    return z_code


def fetch_reg_data():
    url = "https://www.townscript.com/api/registration/getRegisteredUsers"
    params = {"eventCode": os.environ["eventCode"]}
    headers = {"Authorization": os.environ["Authorization"]}
    r = requests.get(url, headers=headers, params=params)
    data = json.loads(str(r.json()["data"]))
    return data

def fetch_cashless_reg_data():
    cashless_data = []
    for i in CashlessReg.objects.all():
        new_data = {}
        new_data['userEmailId'] = i.email
        new_data['userName'] = i.name
        new_data['registrationTimestamp'] = i.dt.astimezone(datetime.timezone(datetime.timedelta(minutes=30, hours=5))).strftime("%d-%m-%Y %H:%M")
        answerList = []
        answerList.append({'question':'Organization','answer':'IIT Ropar'})
        answerList.append({'question':'City','answer':i.city})
        answerList.append({'question':'Contact Number','answer':i.mobile})
        new_data['answerList']=answerList
        new_data['uniqueOrderId'] = '-'
        new_data['ticketPrice'] = 0
        new_data['allTicketName'] = convert_event_name_to_actual_event_name(i.event)
        cashless_data.append(new_data)
    return cashless_data


def reg_details(details, events, total, reg):
    details = {}
    dt = datetime.datetime.strptime(reg["registrationTimestamp"], "%d-%m-%Y %H:%M")
    for i in reg['answerList']:
        if i['question']=='Organization':
            details["organization"] = i['answer']
        if i['question']=='City':
            details["city"] = i["answer"]
        if i['question']=='Contact Number':
            details["mobile"] = i["answer"]
    event = {}
    event["uniqueOrderId"] = reg["uniqueOrderId"]
    event["price"] = reg["ticketPrice"]
    event["name"] = reg["allTicketName"]
    event["dt"] = dt
    event["date"] = dt.strftime("%#d %b, %Y")
    event["time"] = dt.strftime("%I:%M %p")
    events.append(event)

    total["total"] += reg["ticketPrice"]

    details["events"] = events
    details["total"] = total["total"]
    return details


def update_reg_database(details, email):
    details["events"].sort(key=lambda x: x["dt"])

    for registration in Registrations.objects.all():
        if registration.email == email:
            registration.mobile = details["mobile"]
            registration.organization = details["organization"]
            registration.city = details["city"]
            registration.events = json.dumps(details["events"], cls=DjangoJSONEncoder)
            registration.total = details["total"]
            registration.save()
            break

def update_reg_profile_page(request):
    z_code=z_code_handle(request.user.email, request.user.first_name+' '+request.user.last_name)

    data = fetch_reg_data()
    cashless_data = fetch_cashless_reg_data()
    details=False
    events=[]
    total={'total':0}
    
    for reg in data:
        if reg['userEmailId']==request.user.email:
            details=reg_details(details,events,total,reg)
    
    for reg in cashless_data:
        if reg['userEmailId']==request.user.email:
            details=reg_details(details,events,total,reg)
    
    if (details!=False):
        update_reg_database(details,request.user.email)

    return details,z_code


def registrationsGoogleSheetsUpdateFun():
    SPREADSHEET_ID = "1_7EvZe4K_W2X3_p46inOaxsLgFKlUFKNHJVL1TFq9NY"

    creds = None

    token_key = json.loads(os.environ["token_key_json_3"])
    token_key["private_key"] = token_key["private_key"].replace("/*/", " ")

    creds = Credentials.from_service_account_info(token_key)
    # creds = Credentials.from_service_account_file("main_page/token_key.json")

    service = build("sheets", "v4", credentials=creds)

    sheets = (
        service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()["sheets"]
    )
    sheet_names = []
    for sheet in sheets:
        sheet_names.append(sheet["properties"]["title"])

    clearAll = {"ranges": []}

    for sheet in sheet_names:
        clearAll["ranges"].append(sheet + "!A1:O999")
    service.spreadsheets().values().batchClear(
        spreadsheetId=SPREADSHEET_ID, body=clearAll
    ).execute()

    addSheetRequest = {"requests": []}
    writeRequest = {
        "value_input_option": "USER_ENTERED",
        "data": [
            {
                "range": "Summary",
                "values": [["Summary"], ["Event Name", "Number of Registrations"]],
            }
        ],
    }

    for reg in Registrations.objects.all():
        if reg.events != "":
            for event in json.loads(reg.events):
                if event["name"] not in sheet_names:
                    add_sheet = {
                        "requests": [
                            {
                                "addSheet": {
                                    "properties": {
                                        "title": event["name"],
                                        "gridProperties": {
                                            "rowCount": 20,
                                            "columnCount": 9,
                                        },
                                    }
                                }
                            }
                        ]
                    }
                    service.spreadsheets().batchUpdate(
                        spreadsheetId=SPREADSHEET_ID, body=add_sheet
                    ).execute()
                    sheet_names.append(event["name"])

                if not any(
                    writeSheet["range"] == event["name"]
                    for writeSheet in writeRequest["data"]
                ):
                    writeRequest["data"].append(
                        {
                            "range": event["name"],
                            "values": [
                                [event["name"]],
                                [
                                    "Name",
                                    "Zeitgeist Code",
                                    "Email",
                                    "Mobile",
                                    "College",
                                    "City",
                                    "Date",
                                    "Time",
                                    "Paid",
                                ],
                            ],
                        }
                    )

                for sheet in writeRequest["data"]:
                    if sheet["range"] == event["name"]:
                        sheet["values"].append(
                            [
                                reg.name,
                                reg.z_code,
                                reg.email,
                                reg.mobile,
                                reg.organization,
                                reg.city,
                                event["date"],
                                event["time"],
                                event["price"],
                            ]
                        )

    sheets = (
        service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()["sheets"]
    )

    formatBodyRequest = {"requests": []}

    for sheet in sheets:
        sheet_name = sheet["properties"]["title"]
        sheet_id = sheet["properties"]["sheetId"]

        for sheet in writeRequest["data"]:
            if sheet["range"] != "Summary" and sheet["range"] == sheet_name:
                writeRequest["data"][0]["values"].append(
                    [sheet_name, len(sheet["values"]) - 2]
                )

                formatBodyRequest["requests"].append(
                    {
                        "mergeCells": {
                            "mergeType": "MERGE_ALL",
                            "range": {
                                "startColumnIndex": 0,
                                "startRowIndex": 0,
                                "endColumnIndex": 9,
                                "endRowIndex": 1,
                                "sheetId": sheet_id,
                            },
                        }
                    }
                )

        formatBodyRequest["requests"].append(
            {
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 0,
                        "endRowIndex": 1,
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "horizontalAlignment": "CENTER",
                            "textFormat": {
                                "fontSize": 14,
                                "bold": True,
                            },
                        }
                    },
                    "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)",
                }
            }
        )
        formatBodyRequest["requests"].append(
            {
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 1,
                        "endRowIndex": 2,
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "horizontalAlignment": "CENTER",
                            "textFormat": {
                                "fontSize": 11,
                                "bold": True,
                            },
                        }
                    },
                    "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)",
                }
            }
        )
        formatBodyRequest["requests"].append(
            {
                "repeatCell": {
                    "range": {"sheetId": sheet_id, "startRowIndex": 2},
                    "cell": {
                        "userEnteredFormat": {
                            "horizontalAlignment": "LEFT",
                            "textFormat": {"fontSize": 10},
                        }
                    },
                    "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)",
                }
            }
        )
        formatBodyRequest["requests"].append(
            {
                "autoResizeDimensions": {
                    "dimensions": {
                        "sheetId": sheet_id,
                        "dimension": "COLUMNS",
                        "startIndex": 0,
                    }
                }
            }
        )
        formatBodyRequest["requests"].append(
            {
                "sortRange": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 2,
                    },
                    "sortSpecs": [
                        {"dimensionIndex": 6, "sortOrder": "ASCENDING"},
                        {"dimensionIndex": 7, "sortOrder": "ASCENDING"},
                    ],
                }
            }
        )

    formatBodyRequest["requests"].append(
        {
            "repeatCell": {
                "range": {
                    "sheetId": sheets[0]["properties"]["sheetId"],
                    "startRowIndex": 2,
                    "startColumnIndex": 1,
                    "endColumnIndex": 2,
                },
                "cell": {"userEnteredFormat": {"horizontalAlignment": "CENTER"}},
                "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)",
            }
        }
    )
    formatBodyRequest["requests"].append(
        {
            "mergeCells": {
                "mergeType": "MERGE_ALL",
                "range": {
                    "startColumnIndex": 0,
                    "startRowIndex": 0,
                    "endColumnIndex": 2,
                    "endRowIndex": 1,
                    "sheetId": sheets[0]["properties"]["sheetId"],
                },
            }
        }
    )

    if len(addSheetRequest["requests"]) != 0:
        service.spreadsheets().batchUpdate(
            spreadsheetId=SPREADSHEET_ID, body=addSheetRequest
        ).execute()
    service.spreadsheets().values().batchUpdate(
        spreadsheetId=SPREADSHEET_ID, body=writeRequest
    ).execute()
    service.spreadsheets().batchUpdate(
        spreadsheetId=SPREADSHEET_ID, body=formatBodyRequest
    ).execute()

def CashlessEligible(request):
    try:
        email = request.user.email.lower()
        if email=="2019eeb1210@iitrpr.ac.in" or email=="2018eeb1174@iitrpr.ac.in":
            return True
        elif email[0:7]=="2020ceb" and email[12:]=="iitrpr.ac.in":
            return True
        elif email[0:7]=="2020chb" and email[12:]=="iitrpr.ac.in":
            return True
        elif email[0:7]=="2020csb" and email[12:]=="iitrpr.ac.in":
            return True
        elif email[0:7]=="2020eeb" and email[12:]=="iitrpr.ac.in":
            return True
        elif email[0:7]=="2020mcb" and email[12:]=="iitrpr.ac.in":
            return True
        elif email[0:7]=="2020meb" and email[12:]=="iitrpr.ac.in":
            return True
        elif email[0:7]=="2020mmb" and email[12:]=="iitrpr.ac.in":
            return True
        else:
            return False
    except:
        return False

def convert_event_name_to_actual_event_name(event):
    switcher={
        "Adagio":"Adagio",
        "AdMad":"AdMad",
        "Aero Deli":"Aero Deli",
        "Aero Quiz":"AeroQuiz",
        "Age Limit Exceeded":"Age limit exceeded",
        "Art of Photoshop":"Art of photoshop",
        "Article Writing and Press Release":"Article Writing and Press Release",
        "Astrophotography":"Astrophotography",
        "Astroquiz":"Astroquiz",
        "AUTOMOTIVE DYC":"Design (Automotive)",
        "Banging beats":"Banging Beats - Street Battle",
        "Biz-Tech Quiz":"Biz-Tech Quiz",
        "Brush War":"Brush War",
        "Business Quiz":"Business Quiz",
        "Call of duty mobile":"CODM",
        "Calypso":"Calypso : Group dance event",
        "Case Study (Zenith)":"Case Study (Zenith)",
        "Case Study Competition (Fincom)":"Case Study Competition (Fincom)",
        "Chem-e-quiz":"Chem Quiz",
        "Chemiscribble":"Chemiscribble",
        "Corte Paper":"Courte Paper",
        "Crisis Solving":"Crisis Solving-Action plan",
        "CSGO":"CSGO",
        "DebugIt":"Debugit",
        "Design Marathon":"Design Marathon",
        "Doodle Maestro":"Doodle Maestro",
        "News Up (Ecell)":"News Up (Ecell)",
        "Energy efficient building":"Energy Efficient Building",
        "Euphony":"Euphony",
        "Extempore":"Extempore",
        "Face Wizards":"Face Wizards",
        "FilmX":"FilmX",
        "Foodomark":"Foodomark",
        "FOTOPEDIA":"Photopedia",
        "General Quiz":"General Quiz",
        "Hackathon":"Hackathon",
        "Improvisation Theatre(Improv)":"Improv",
        "INVENTO":"Invento",
        "JUNOON":"Junoon : Solo Dance Event",
        "JUST A MINUTE":"Just a Minute",
        "LASHKARA":"Lashkara",
        "Mechanical Madness":"Mechanical Madness",
        "MELA Quiz":"Movie Quiz",
        "Micromouse":"Micromouse",
        "MISHTANNO":"Mishtanno",
        "Mono Acting(Abhivyakti)":"Mono Acting",
        "Mr & Mrs Zeitgeist":"Mr & Mrs Zeitgeist",
        "P=NP":"P=NP",
        "Polyphony":"Polyphony",
        "Quick Type":"Quick Type",
        "Rapsody":"Rapsody",
        "RoboCAD":"Robocad",
        "Rocket League":"Rockect-league",
        "Saaz":"Saaz",
        "SCRIBBLE":"Scribble",
        "Sketching Geeks":"Sketching Geeks",
        "SpeeDAC":"Speedac",
        "Spoken Poetry(Ruhaniyat)":"Spoken Poetry",
        "Stock stalkers":"Stock Stalkers",
        "STREET VAGANZA":"Street Vaganza",
        "Turncoat":"Turncoat",
        "VLSI Analog design":"VLSI Analog Design",
        "WALTZ":"Waltz : Duet Dance Event",
        "Valorant":"Valorant",
        "Weapon Star":"Weapon Star (Mechanical Department)",
        "Yatharth(Group Video)":"Group Acting",
    }
    return switcher.get(event,event)