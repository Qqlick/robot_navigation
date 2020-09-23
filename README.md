# Robot City Navigation System


## CICD is here: <https://github.com/Qqlick/robot_navigation/actions>


Stack:
   - Python 3.7
   - DynamoDB
   - AWS Lambda as backend server
   - Flask
   - Zappa for deployment to AWS
   - Pytest (just draft for CICD)
   - Flake8 for lint
   - Swagger for data validation and API docs and live demo
   - Localstack for local AWS development 
   - Docker, docker-compose for local dev env
   - Newman (Postman) for API testing in CICD

## Domain-specific language
   DSL is set of steps for robot to tet from starting point to destination.
   Each step consists of azimuth and distance to next step.
   Example: 
   
        {
            "path":[
                {
                    "azimuth":5,
                    "dist":17
                },
                {
                    "azimuth":23,
                    "dist":5
                },
                {
                    "azimuth":12,
                    "dist":7
                }
            ],
            "path_dest":"45:56=>76:90",
            "path_info":{
                "finish":[
                    76,
                    90
                ],
                "start":[
                    45,
                    56
                ]
            }
        }
