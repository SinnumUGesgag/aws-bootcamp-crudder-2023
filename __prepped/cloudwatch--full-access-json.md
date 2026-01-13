
{
	"Version":"2012-10-17",
	"Statement":[{
		{
			"Effect": "Allow",
			"Action": [
				"ssmessages:CreateControlChannel",
				"ssmessages:CreateDataChannel",
				"ssmessages:OpenControlChannel",
				"ssmessages:OpenDataChannel"
			],
			"Resource": ":\*"
		}
	}]
}
