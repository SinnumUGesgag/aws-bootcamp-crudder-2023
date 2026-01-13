
#task-defintion

"family": "backend-flask",
"executionRoleArn": "arn:aws:iam::{ acct# }:role/CruddurServiceExecutionRole",
"taskRoleArn": "arn:aws:iam::{ acct# }:role/CruddurTaskRole",
"networkMode": "awsvpc",
"cpu": "256",
"memory": "512",
"requiresCompatibilities": [
	"FARGATE"
],
"containerDefinitions": [
	{
		"name": "backend-flask",
		"image": "{ acct# }.dkr.ecr.{region}.amazonaws.com/backend-flask",
		"essential": true,
		"healthcheck": {
			"command": [
				"CMD-SHELL",
				"python /backend-flask/bin/flask/health-check"
			],
			"interval": 30,
			"timeout": 5,
			"retries": 3,
			"startPeriod": 60
		},
		"portMappings": [
			{
				"name": "backend-flask",
				"containerPort": 4567,
				"protocol": "tcp",
				"appProtocol": "http"
			}
		],
		"logConfiguration": {
			"logDriver": "awslogs",
			"options": {
				"awslogs-group": "cruddur",
				"awslogs-region": "{region}",
				"awslogs-stream-prefix": "backend-flask"
			}
		},
		"environment": [
			{"name": "OTEL_SERVICE_NAME", "value": "aaaaa"},
			{"name": "OTEL_EXPORTER_OTLP_ENDPOINT", "value": "aaaaa"},
			{"name": "AWS_COGNITO_USER_POOL_ID", "value": "aaaaa"},
			{"name": "AWS_COGNITO_USER_POOL_CLIENT_ID ", "value": "aaaaa"},
			{"name": "FRONTEND_URL", "value": "aaaaa"},
			{"name": "BACKEND_URL", "value": "aaaaa"},
			{"name": "AWS_DEFAULT_REGION", "value": "aaaaa"}
		],
		"secrets": [
			{"name": "AWS_ACCESS_KEY_ID", "valueFrom": "arn:aws:ssm:{region}:{acct#}:parameter/cruddur/backend-flask/AWS_ACCESS_KEY_ID"},
			{"name": "AWS_SECRET_ACCESS_KEY", "valueFrom": "arn:aws:ssm:{region}:{acct#}:parameter/cruddur/backend-flask/AWS_SECRET_ACCESS_KEY"},
			{"name": "CONNECTION_URL", "valueFrom": "arn:aws:ssm:{region}:{acct#}:parameter/cruddur/backend-flask/CONNECTION_URL"},
			{"name": "ROLLBAR_ACCESS_TOKEN", "valueFrom": "arn:aws:ssm:{region}:{acct#}:parameter/cruddur/backend-flask/ROLLBAR_ACCESS_TOKEN"},
			{"name": "OTEL_EXPORTER_OTLP_HEADERS", "valueFrom": "arn:aws:ssm:{region}:{acct#}:parameter/cruddur/backend-flask/OTEL_EXPORTER_OTLP_HEADERS"}	
		]
	}
]

