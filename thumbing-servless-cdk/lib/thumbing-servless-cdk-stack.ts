import * as cdk from 'aws-cdk-lib/core';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as s3n from 'aws-cdk-lib/aws-s3-notifications';
import * as subscriptions from 'aws-cdk-lib/aws-sns-subscriptions';
import * as sns from 'aws-cdk-lib/aws-sns';
import { Construct } from 'constructs';
import * as dotenv from 'dotenv';
import { S3_KEEP_NOTIFICATION_IN_IMPORTED_BUCKET } from 'aws-cdk-lib/cx-api';
import { subscribe } from 'diagnostics_channel';


dotenv.config();

export class ThumbingServlessCdkStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const functionPath: string = process.env.THUMBING_FUNCTION_PATH as string;
    const folderInput: string = process.env.THUMBING_S3_FOLDER_INPUT as string;
    const folderOutput: string = process.env.THUMBING_S3_FOLDER_OUTPUT as string;
    const webhookUrl: string = process.env.THUMBING_WEBHOOK_URL as string;
    const topicName: string = process.env.THUMBING_TOPIC_NAME as string;

    const snsTopic = this.createSnsTopic(topicName)
    this.createSnsSubscription(snsTopic,webhookUrl)
    const snsPublishPolicy = this.createPolicySnSPublish(snsTopic.topicArn)


    //Per Bucket Build the Following ------------------------------->
    // const bucketName: string = process.env.TEMPLATE_BUCKET_NAME as string; 
    // const bucketTemplate = this.createBucket(bucketName);
    // const lambdaTemplate = this.createLambda(functionPath, bucketName, folderInput, folderOutput);
    // this.createAddPoliciesAndNotifications(lambdaTemplate, bucketTemplate, snsPublishPolicy, snsTopic, folderInput, folderOutput);
    //<-------------------------------------------

    
    // Avatars Assets' Bucket ------------------------------->
    const bucketNameAvatars: string = process.env.ASSETS_BUCKET_NAME as string; 
    const bucketAvatars = this.createBucket(bucketNameAvatars);
    //const bucketAvatars = this.importBucket(bucketNameAvatars);
    const lambdaAvatars = this.createLambda(functionPath,  'avatarAssetsLambda', bucketNameAvatars, folderInput, folderOutput);
    this.createAddPoliciesAndNotifications(lambdaAvatars, bucketAvatars, snsPublishPolicy, snsTopic, folderInput, folderOutput);
    //<-------------------------------------------


    // Ports Assets' Bucket ------------------------------->
    const bucketNamePosts: string = process.env.POSTS_BUCKET_NAME as string; 
    const bucketPosts = this. createBucket(bucketNamePosts);
    //const bucketPosts = this.importBucket(bucketNamePosts);
    const lambdaPosts = this.createLambda(functionPath, 'postsAssetsLambda', bucketNamePosts, folderInput, folderOutput);
    this.createAddPoliciesAndNotifications(lambdaPosts, bucketPosts, snsPublishPolicy, snsTopic, folderInput, folderOutput);
    //<-------------------------------------------


    // Personal Communications' Assets' Bucket ------------------------------->
    const bucketNamePerscomms: string = process.env.PERSCOMMS_BUCKET_NAME as string; 
    const bucketPerscomms = this.createBucket(bucketNamePerscomms);
    //const bucketPerscomms = this.importBucket(bucketNamePerscomms);
    const lambdaPerscomms = this.createLambda(functionPath,  'persCommsAssetsLambda', bucketNamePerscomms, folderInput, folderOutput);
    this.createAddPoliciesAndNotifications(lambdaPerscomms, bucketPerscomms, snsPublishPolicy, snsTopic, folderInput, folderOutput);
    //<-------------------------------------------

  }

  createBucket(bucketName: string): s3.IBucket {
    const bucket = new s3.Bucket(this, bucketName, {
      bucketName: bucketName,
      //removalPolicy: cdk.RemovalPolicy.DESTROY // I removed this because I want the Buckets to exsist even when I take down the Stack
    });
    return bucket;
  }

  importBucket(bucketName: string): s3.IBucket {
    const bucket = new s3.Bucket(this, bucketName, {bucketName: bucketName});
    return bucket;
  }

  createLambda(functionPath: string, id: string, bucketName: string, folderInput: string, folderOutput: string ): lambda.IFunction {
    const lambdaFunction = new lambda.Function(this, id, {
      runtime: lambda.Runtime.NODEJS_24_X,
      handler: 'index.handler',
      code: lambda.Code.fromAsset(functionPath),
      environment: {
        DEST_BUCKET_NAME: bucketName,
        FOLDER_INPUT: folderInput,
        FOLDER_OUTPUT: folderOutput,
        PROCESS_WIDTH: '512',
        PROCESS_HEIGHT: '512'
      }
    });
    return lambdaFunction;
  }

  createAddPoliciesAndNotifications(lambda: lambda.IFunction, bucket: s3.IBucket, snsPublishPolicy: iam.PolicyStatement, snsTopic: sns.ITopic, folderInput: string, folderOutput: string): void{
    const s3ReadWritePolicy = this.createPolicyBucketAccess(`${bucket.bucketArn}`,`${bucket.bucketArn}/*`)
    lambda.addToRolePolicy(s3ReadWritePolicy);
    lambda.addToRolePolicy(snsPublishPolicy);
    this.createS3NotifyToLambda(folderInput,lambda,bucket)
    this.createS3NotifyToSns(folderOutput,snsTopic,bucket)
  }

  createS3NotifyToLambda(prefix: string, lambda: lambda.IFunction, bucket: s3.IBucket): void {
    const destination = new s3n.LambdaDestination(lambda);
    bucket.addEventNotification(s3.EventType.OBJECT_CREATED_PUT,destination,{prefix: prefix})
  }

  createPolicyBucketAccess(bucketArn: string, bucketResouces: string){
    const s3ReadWritePolicy = new iam.PolicyStatement({
        actions: ['s3:GetObject', 's3:PutObject',],
        resources: [bucketArn, bucketResouces,],
    });
    return s3ReadWritePolicy;
  }

  createSnsTopic(topicName: string): sns.ITopic{
      const logicalName = "ThumbingTopic";
      const snsTopic = new sns.Topic(this, logicalName, {
          topicName: topicName
      });
      return snsTopic;
  }

  createSnsSubscription(snsTopic: sns.ITopic, webhookUrl: string): sns.Subscription {
    const snsSubscription = snsTopic.addSubscription(
      new subscriptions.UrlSubscription(webhookUrl)
    )
    return snsSubscription;

  }

  createS3NotifyToSns(prefix: string, snsTopic: sns.ITopic, bucket: s3.IBucket): void {
    const destination = new s3n.SnsDestination(snsTopic)
    bucket.addEventNotification(
      s3.EventType.OBJECT_CREATED_PUT,
      destination,
      {prefix: prefix}
    );
  }

  createPolicySnSPublish(topicArn: string){
    const snsPublishPolicy = new iam.PolicyStatement({
      actions: [
        'sns:Publish',
      ],
      resources: [
        topicArn
      ]
    });
    return snsPublishPolicy;
  }


}