'''
Created on 

@author: Mohammed Farmaan k, Surya pugal

source:
    https://youtu.be/k10ILjUyWuQ
'''
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask, Response, render_template, send_from_directory
from marshmallow import Schema, fields
import json
from werkzeug.utils import secure_filename



app = Flask(__name__, template_folder='./swagger/templates')

@app.route('/')
def hello_world():
    return 'Hello, World'

# Create an APISpec
spec = APISpec(
    openapi_version="3.0.0",
    title="",
    version="",
    # servers = [
    # {
    #     "url": "https://api.tikapi.io",
    #     "description": "Live Server"
    # },
    # {
    #     "url": "https://sandbox.tikapi.io",
    #     "description": "Sandbox Server"
    # }
# ],
    info={
        "description":"# Introduction\r\n\r\nTikAPI is an unofficial API platform on top of TikTok. Our API is RESTful. It has predictable resource URLs. It uses HTTP response codes to indicate errors. It also accepts and returns JSON in the HTTP body. You can use your favorite HTTP/REST library to work with TikAPI.\r\n\r\n\r\nTikAPI endpoints fall into two categories:\r\n\r\n- **Public Data**\r\n\t\r\n\tWhich are endpoints for getting any TikTok Public information, such as profile information, feed posts, videos, hashtags, etc.\r\n\tYou don't need any TikTok account authentication to use the Public Data endpoints.\r\n\r\n- **Authenticated Users**\r\n\t\r\n   These Endpoints are for getting information or performing interactions on authorized TikTok accounts that have been authenticated through our OAuth platform. \r\n\r\n# Getting Started\r\n\r\nTo make things easier for you we have already implemented TikAPI in Javascript (Typescript) and Python. \r\n\r\n## Installation\r\nInstall for Javascript\r\n```bash\r\nnpm i tikapi@latest\r\n```\r\n\r\nInstall for Python\r\n```bash\r\npip3 install tikapi\r\n```\r\n\r\nIf you are using another programming language you can just call the API directly with any HTTP client. The HTTP request formation is quite simple and well documented.\r\n\r\n\r\n## Authentication\r\n\r\n### API Key\r\nNow to start using TikAPI you will need an API Key. If you don't already have one, you can [sign up for a free trial subscription and get your API Key](https://tikapi.io/#pricing).\r\n\r\nIf you just want to do some testings first, then you can just use our Sandbox server.\r\n\r\n### Account Key\r\nFor using the authenticated user endpoints you will need to get an Account Key by asking users for authorization. Or you can authenticate your own account(s) from the [Developer Dashboard](https://tikapi.io/developer/users) with a click of a button.\r\n\r\n\r\n[Learn more about authenticating users](https://helpdesk.tikapi.io/portal/en/kb/articles/how-do-i-authorize-users)\r\n\r\n## Usage\r\n\r\nThe API is meant to be used on server-side only, because it would be a security issue to directly expose your API Key in the front-end. \r\n\r\n\r\n\r\n### Usage in Javascript\r\n\r\n```javascript\r\nimport TikAPI from 'tikapi';\r\n\r\nconst api = TikAPI('DemoAPIKeyTokenSeHYGXDfd4SFD320Sc39Asd0Sc39Asd4s');\r\n```\r\n*ES6 Import syntax is recommended*\r\n\r\nCommon JS\r\n```javascript\r\nconst TikAPI = require('tikapi').default;\r\n\r\nconst api = TikAPI('DemoAPIKeyTokenSeHYGXDfd4SFD320Sc39Asd0Sc39Asd4s');\r\n```\r\n\r\n\r\n### Usage in Python\r\n\r\n```python\r\nfrom tikapi import TikAPI\r\n\r\napi = TikAPI('DemoAPIKeyTokenSeHYGXDfd4SFD320Sc39Asd0Sc39Asd4s');\r\n```\r\n\r\n\r\n### Sandbox\r\n\r\nEnabling sandbox in Javascript:\r\n```javascript\r\napi.set({\r\n\t$sandbox: true\r\n});\r\n```\r\n\r\nEnabling sandbox server in Python:\r\n```python\r\napi.set(\r\n\t__sandbox__=True\r\n)\r\n```\r\n\r\nSandbox API Key:\r\n```\r\nDemoAPIKeyTokenSeHYGXDfd4SFD320Sc39Asd0Sc39Asd4s\r\n```\r\n\r\nSandbox Account Key:\r\n```\r\nDemoAccountKeyTokenSeHYGXDfd4SFD320Sc39Asd0Sc39A\r\n```\r\n\r\nScroll down the documentation for more specific usage examples on all endpoints 🙃\r\n\r\n\r\n\r\n## Postman\r\nYou can easily start testing our API with Postman. Make sure you set `apiKey` & `accountKey` as environment variables.\r\n\r\n[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/13698063-2f272f6e-e328-4777-b7b4-9e5d53f7bfd2?action=collection%2Ffork&collection-url=entityId%3D13698063-2f272f6e-e328-4777-b7b4-9e5d53f7bfd2%26entityType%3Dcollection%26workspaceId%3D9d466c87-79ba-4b04-aec2-6d8d57a67cb4#?env%5BProduction%5D=W3sia2V5IjoiYXBpS2V5IiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6IiIsInNlc3Npb25JbmRleCI6MH0seyJrZXkiOiJhY2NvdW50S2V5IiwidmFsdWUiOiIiLCJlbmFibGVkIjp0cnVlLCJ0eXBlIjoiZGVmYXVsdCIsInNlc3Npb25WYWx1ZSI6Iihvbmx5IGZvciBhdXRoZW50aWNhdGVkIGVuZHBvaW50cykiLCJzZXNzaW9uSW5kZXgiOjF9LHsia2V5IjoiYmFzZVVybCIsInZhbHVlIjoiaHR0cHM6Ly9hcGkudGlrYXBpLmlvIiwiZW5hYmxlZCI6dHJ1ZSwidHlwZSI6ImRlZmF1bHQiLCJzZXNzaW9uVmFsdWUiOiJodHRwczovL2FwaS50aWthcGkuaW8iLCJzZXNzaW9uSW5kZXgiOjJ9XQ==)\r\n\r\n\r\n\r\n\r\n# Errors\r\nYou can identify errors from the HTTP Status code or response body.\r\n\r\n\r\n## Bad Request (400)\r\n\r\nThe request could not be understood by the server due to malformed syntax or parameters. The client should not repeat the request without modifications.\r\n\r\n#### Example\r\n```json\r\n{\r\n\t\"status\": \"error\",\r\n\t\"message\": \"Missing fields.\", \r\n\t\"fields\": {\r\n\t\t\"secUid\": \"A valid TikTok secUid is required.\"\r\n\t}\r\n}\r\n```\r\n\r\n## Unauthorized (401)\r\n\r\nThe API Key is not valid, make sure you have typed it correctly and you haven't refreshed it recently.\r\n\r\n#### Example\r\n```json\r\n{\r\n    \"message\": \"A valid API Key is required.\",\r\n    \"status\": \"error\"\r\n}\r\n```\r\n\r\n## Forbidden (403)\r\n\r\nThis error can occur for different reasons. Usually the message includes more information about the error, and might also include a TikTok `statusCode` paramater.\r\n\r\n#### Example\r\n```json\r\n{\t\r\n\t\"status\": \"error\",\r\n\t\"message\":\"Something went wrong.\"\r\n}\r\n```\r\n\r\n[Scroll down below for more 403 error examples](#other-errors)\r\n\r\n## Account Key Session Expiry (428)\r\nThe Account Key is no longer valid and a re-authorization is required. \r\n\r\nWhen this error occurs you should notify the user and send a new authorization link.\r\n\r\n#### Example\r\n```json\r\n{\t\r\n\t\"status\": \"error\",\r\n\t\"message\": \"Account session expired, please ask user to re-login and re-authorize.\",\r\n\t\"statusCode\": 8\r\n}\r\n```\r\n[Learn more about session expiry](https://helpdesk.tikapi.io/portal/en/kb/articles/why-are-authorized-accounts-being-removed-automatically)\r\n\r\n## Rate-Limit (429)\r\n\r\nThis means that you have reached your subscription daily request limit or bandwidth limit. You should upgrade your subscription or just wait a few hours until the limit rests.\r\n\r\n[Learn more about the rate-limit reset](https://helpdesk.tikapi.io/portal/en/kb/articles/when-does-api-rate-limit-reset) \r\n\r\n#### Example\r\n```json\r\n{\t\r\n\t\"status\": \"error\",\r\n\t\"message\":\"API Key Rate-Limit reached.\"\r\n}\r\n```\r\n\r\n<h2 id=\"other-errors\">Other TikTok Errors (403)</h2>\r\nLike we mentioned above, the 403 Errors can occur for different reasons.\r\n\r\n#### For example this error happens when you are trying to get a profile information for a TikTok account that doesn't exist:\r\n```json\r\n{\r\n\t\"status\": \"error\",\r\n\t\"message\": \"User doesn't exist\",\r\n\t\"statusCode\": 10202\r\n}\r\n```\r\n\r\nHere is the description of some of the error codes:\r\n```json\r\n\t2054: \"Video is unavailable or deleted.\",\r\n\t2752: \"Ad video is unavailable.\",\r\n\t10000: \"TikTok Captcha Error\",\r\n\t10101: \"TikTok Server Error\",\r\n\t10102: \"User not logged-in\",\r\n\t10111: \"TikTok Network Error\",\r\n\t10113: \"TikTok blocked resource\",\r\n\t10114: \"TikTok blocked resource\",\r\n\t10119: \"User not logged-in for Live\",\r\n\t10202: \"User doesn't exist\",\r\n\t10203: \"Music doesn't exist\",\r\n\t10204: \"Video doesn't exist\",\r\n\t10205: \"Hashtag doesn't exist\",\r\n\t10208: \"Effect doesn't exist\",\r\n\t10209: \"Hashtag is blacklisted\",\r\n\t10210: \"Live doesn't exist\",\r\n\t10211: \"Hashtag is sensitive\",\r\n\t10212: \"Hashtag error\",\r\n\t10215: \"Video is currently unavailable\",\r\n\t10216: \"Video is private\",\r\n\t10217: \"Video is currently unavailable\",\r\n\t10218: \"Music error\",\r\n\t10219: \"Music copyright error\",\r\n\t10220: \"Video music error\",\r\n\t10221: \"User is banned\",\r\n\t10223: \"User error\",\r\n\t10224: \"Entity doesn't exist\",\r\n\t10225: \"User unique sensitivity\",\r\n\t10227: \"Video is under review\",\r\n\t10228: \"Video is under risk control\",\r\n\t10229: \"Video is hidden\",\r\n\t10230: \"Video is under risk control\",\r\n\t10231: \"Video is not visible on your country\",\r\n\t10241: \"Video is deleted.\",\r\n    10242: \"This video has restricted access\",\r\n\t10404: \"List limit reached\"\r\n```\r\n\r\n",
        "version":"3.0.0",
        "title":"TikAPI REST API",
        "license":{"name": "All rights reserved.", "url": "http://tikapi.io"},
        "contact":{"name": "Contact","email": "contact@tikapi.io"},
        "termsOfService": "https://www.tikapi.io/terms/",
        "x-logo": { "url": "/assets/img/ll.png", "backgroundColor": "transparent", "href": "https://tikapi.io/"},
        "x-sideInfoItems": [
      {
        "text": "Developer Dashboard",
        "url": "https://tikapi.io/developer"
      },
      {
        "text": "Frequently Asked Questions",
        "url": "https://helpdesk.tikapi.io"
      },
      {
        "text": "Popup Login Button",
        "url": "https://github.com/tikapi-io/login-popup"
      },
      {
        "text": "Python & Javascript API",
        "url": "https://github.com/tikapi-io/tiktok-api"
      },
      {
        "text": "OAuth Demo Video Tutorial",
        "url": "https://youtu.be/JDupJKZ0Yy8"
      },
    ],
      "tags": [
    {
      "name": "Public",
      "description": "Endpoints that do not require a logged in user."
    },
    {
      "name": "Profile",
      "description": "Authenticated user profile endpoints."
    },
    {
      "name": "Followers",
      "description": "View & interact with followers."
    },
    {
      "name": "Posts",
      "description": "View & react to videos and comments."
    },
    {
      "name": "Messages",
      "description": "User messages endpoints."
    },
    {
      "name": "Live",
      "description": "Live endpoints."
    },
    {
      "name": "Key",
      "description": "Information about your API Key."
    }
  ],
  "x-tagGroups": [
    {
      "name": "Public Data",
      "collapsible": True,
      "tags": [
        "Public"
      ]
    },
    {
      "name": "Authenticated User",
      "collapsible": True,
      "tags": [
        "Profile",
        "Followers",
        "Posts",
        "Messages",
        "Live"
      ]
    },
    {
      "name": "APIKey",
      "tags": [
        "Key"
      ]
    }
  ],
   "components": {
    "securitySchemes": {
      "apiKey": {
        "in": "header",
        "name": "X-API-KEY",
        "x-displayName": "API Key",
        "description": "This is your TikAPI API Key, it must be included in the headers of every request.\r\n \r\nYou can refresh it from your [Developer Dashboard](https://tikapi.io/developer).",
        "type": "apiKey"
      },
      "accountKey": {
        "description": "TikAPI is using a custom implementation of OAuth 2.0 specification.\r\n\r\nHere are the steps for getting an Account Key:\r\n\r\n### 1. Ask a User for Authorization \r\n\r\nTo get an Account Key, you need to ask the user to authorize your application. \r\nYou can do this by sharing your OAuth link to the user or using the [TikAPI Login Button Popup](https://github.com/tikapi-io/js-sdk).\r\n\r\nExample OAuth Link: `https://tikapi.io/account/authorize?client_id=c_1234567890&redirect_uri=https://tikapi.io/success&scope=view_profile+explore`\r\n\r\n- **client_id** <span style=\"color:red;font-size:smaller; font-family: Verdana;\">required</span>\r\n\t- This is your application id, you can find this on your [Developer Dashboard](https://tikapi.io/developer).\r\n- **redirect_uri** <span style=\"color:red;font-size:smaller; font-family: Verdana;\">required</span>\r\n\t- The user will be redirect here after successful authorization and the query parameters `access_token`,`scope` will be included. You must set your application redirect links from the [Developer Dashboard](https://tikapi.io/developer/settings).\r\n- **scope** <span style=\"color:orange;font-size:smaller; font-family: Verdana;\">optional</span>\r\n\t- A list of permissions seperated with space. User can choose to not allow some of these permission.\r\n\r\n- **state** <span style=\"color:orange;font-size:smaller; font-family: Verdana;\">optional</span>\r\n\t- A custom state data to pass on.\r\n\r\n- **country** <span style=\"color:orange;font-size:smaller; font-family: Verdana;\">optional</span>\r\n\t- The account country is automatically detected, but you can override it by providing a ISO country code (~50 countries supported).\r\n\r\n- **email** <span style=\"color:orange;font-size:smaller; font-family: Verdana;\">optional</span>\r\n\t- The account email for your own reference, might be used for future features.\r\n\r\n\r\n### 2. Saving Account Key\r\n\r\nAfter an user has authorized your application, a redirection will occur at your **specified redirection link** and the **query url parameters will include**:\r\n - `access_token` which is the Account Key. \r\n - `scope` which is the list of allowed permissions, in case the user might have chosen to disallow some permissions.\r\n\r\nAlso, you can see your current authorized users from your [Developer Dashboard](https://tikapi.io/developer)\r\n\r\nThe Account Key doesn't normally expire, but it will be invalidated if the account session expires, or when the user chooses to revoke access.\r\n\r\nThe Account Key must be included in the request headers with the header name being `X-ACCOUNT-KEY`.\r\n\r\n| **Security Scheme Type** | <span style=\"font-weight:normal\">User Authorization Key</span> |\r\n|-----------------------|------------------------|\r\n| **Header parameter name** | X-ACCOUNT-KEY          |\r\n\r\n",
        "type": "oauth2",
        "x-displayName": "Account Key",
        "flows": {
          "implicit": {
            "authorizationUrl": "https://tikapi.io/account/authorize",
            "scopes": {
              "view_profile": "To read a user's profile info and activity",
              "edit_profile": "Modify a user's profile",
              "explore": "Explore posts, view feeds and search for things",
              "view_messages": "View a user's messages",
              "media_actions": "To like or comment videos on a user behalf",
              "follow_actions": "To follow or unfollow other users",
              "send_messages": "Send DM messages and Live chat messages",
              "live": "Start, View & End Live videos"
            }
          }
        }
      }
    },
    "responses": {
      "403": {
        "description": "Something went wrong",
        "content": {
          "application/json": {
            "schema": {
              "type": "object",
              "properties": {
                "status": {
                  "type": "string",
                  "default": "error"
                },
                "statusCode": {
                  "type": "integer",
                  "description": "A TikTok status code associated with this error type. Might not always be present.",
                  "example": 10111
                },
                "message": {
                  "type": "string",
                  "description": "A short, human-readable summary of the error type.",
                  "example": "TikTok Network Error"
                }
              }
            }
          }
        }
      },
              "428": {
        "description": "Re-authorization required",
        "content": {
          "application/json": {
            "schema": {
              "type": "object",
              "properties": {
                "status": {
                  "type": "string",
                  "example": "error"
                },
                "message": {
                  "type": "string",
                  "example": "Account session expired please ask user to re-login and re-authorize."
                },
                "statusCode": {
                  "type": "integer",
                  "format": "int32",
                  "example": 8
                }
              }
            }
          }
        }
      },
            "public@check": {
        "description": "Success",
        "content": {
          "application/json": {
            "schema": {
              "type": "object",
              "properties": {
                "extra": {
                  "type": "object",
                  "properties": {
                    "fatal_item_ids": {
                      "type": "array",
                      "items": {
                        "type": "string",
                        "format": "nulleable"
                      }
                    },
                    "logid": {
                      "type": "string",
                      "example": "20230227160725AB294E94D1D34F357D83"
                    },
                    "now": {
                      "type": "number",
                      "example": 1677514046000
                    }
                  }
                },
              }
            }
          }
        }
      }
    }
   }
  },
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)


@app.route('/api/swagger.json')
def create_swagger_spec():
    json_data = json.dumps(spec.to_dict(), indent=2)
    return Response(json_data, mimetype='application/json')

json_data = json.dumps(spec.to_dict(), indent=2)

# Writing the JSON data to a file
with open('swagger.json', 'w') as file:
    file.write(json_data)

class TodoResponseSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    status = fields.Boolean()


class TodoListResponseSchema(Schema):
    todo_list = fields.List(fields.Nested(TodoResponseSchema))

@app.route('/todo')
def todo():
    """Get List of Todo
    ---
    get:
        description: Get List of Todos
        responses:
            200:
                description: Return a todo list
                content:
                    application/json:
                        schema: TodoListResponseSchema
    """

    dummy_data = [{
        'id': 1,
        'title': 'Finish this task',
        'status': False
    }, {
        'id': 2,
        'title': 'Finish that task',
        'status': True
    }]

    return TodoListResponseSchema().dump({'todo_list': dummy_data})


with app.test_request_context():
    spec.path(view=todo)

class TestResponseSchema(Schema):
    name = fields.Str()
    city = fields.Str()
    status = fields.Boolean()


class TestListResponseSchema(Schema):
    test_list = fields.List(fields.Nested(TestResponseSchema))


@app.route('/test')
def test():
    """Get List of test
    ---
    get:
        description: Get List of tests
        responses:
            200:
                description: Return a test list
                content:
                    application/json:
                        schema: TestListResponseSchema
    """

    dummy_data1 = [{
        'name': 'farmaan',
        'city': 'chennai',
        'status': False
    }, {
        'name': 'ali',
        'city': 'madurai',
        'status': True
    }]

    return TestListResponseSchema().dump({'test_list': dummy_data1})


with app.test_request_context():
    spec.path(view=test)

class CarResponseSchema(Schema):
    name = fields.Str()
    brand = fields.Str()


class CarListResponseSchema(Schema):
    car_list = fields.List(fields.Nested(CarResponseSchema))


@app.route('/car')
def car():
    """Get List of car
    ---
    get:
        description: Get List of car
        responses:
            200:
                description: Return a car list
                content:
                    application/json:
                        schema: CarListResponseSchema
    """

    dummy_data2 = [{
        'name': 'farmaan',
        'brand': 'vw',
    }, {
        'name': 'ali',
        'brand': 'bmw',
    }]

    return CarListResponseSchema().dump({'car_list': dummy_data2})


with app.test_request_context():
    spec.path(view=car)

@app.route('/docs')
@app.route('/docs/<path:path>')
def swagger_docs(path=None):
    if not path or path == 'index.html':
        return render_template('index.html', base_url='/docs')
    else:
        return send_from_directory('./swagger/static', secure_filename(path))


if __name__ == '__main__':
    app.run(debug=True)
