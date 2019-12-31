## AWS Lambda Deployment

This deployment guide is derived from the following resources:

- https://edgarroman.github.io/zappa-django-guide/walk_core/
- https://jinwright.net/how-deploy-serverless-wsgi-app-using-zappa/
- https://blog.zappa.io/posts/simplified-aws-lambda-deployments-with-docker-and-zappa
- https://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_NAT_Instance.html#NATInstance
- https://gist.github.com/reggi/dc5f2620b7b4f515e68e46255ac042a7
- https://www.youtube.com/watch?v=zRMMbzw7SsA
- https://www.youtube.com/watch?v=V3pbUzAjdxo

## Setup Custom VPC

Follow this guide to create a public and two private subnets:

- https://miketabor.com/create-a-custom-vpc-with-private-and-public-subnets-on-aws/

Furthermore, create an S3 endpoint that attaches to the two private subnets.

## S3 Buckets

1. Create two S3 buckets:

   - `notepark-lambda`
   - `notepark-assets`

2. Click permissions for `notepark-assets` and enter the following settings for bucket policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::notepark-assets/*"
    }
  ]
}
```

3. Under CORS configuration, enter the following settings to enable CORS:

```xml
<CORSConfiguration>
	<CORSRule>
		<AllowedOrigin>*</AllowedOrigin>
		<AllowedMethod>GET</AllowedMethod>
		<MaxAgeSeconds>3000</MaxAgeSeconds>
		<AllowedHeader>Authorization</AllowedHeader>
	</CORSRule>
</CORSConfiguration>
```

4. Create a new group called `notepark-s3-buckets` in IAM

5. Skip through setup wizard and save new group.

6. Click `Policies` > `Create Policy` > `Import Managed Policy`

7. Search for S3 and select `AmazonS3FullAccess`

8. Enter the following settings into the JSON tab:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::notepark-assets",
        "arn:aws:s3:::notepark-assets/*"
      ]
    }
  ]
}
```

9. Name policy to `notepark-s3-buckets-policy`

10. Attach policy `notepark-s3-buckets-policy` to group `notepark-s3-buckets`

11. Create a new user with the following username: `notepark-s3-bucket`

12. Ensure new user is associated with the `notepark-s3-buckets` group

13. Create a new user with the following username: `notepark-lambda`

14. Attach policy `AdministratorAccess` to `notepark-lambda` user

## RDS

1. Create a new `postgresql 9.6.6-r1` instance

2. Name instance to `notepark-db`

3. Name master username to `notepark`

4. Ensure `notepark vpc` VPC is selected

5. Ensure public accessibility is `no`

6. Ensure selected VPC security group is `default`

7. Name database to `notepark`

## Custom NAT Instance

Follow this guide to setup an EC2 NAT instance:

- https://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_NAT_Instance.html#NATInstance
- https://www.youtube.com/watch?v=V3pbUzAjdxo

## Upload Django Static Files

1. `python manage.py collectstatic --noinput`

2. Create `static` and `media` folders for `notepark-assets` S3 bucket

3. Upload contents from `staticfiles` to `notepark-assets` S3 bucket

## Docker/Zappa (initial setup)

1. Create docker-machine (Windows): `docker-machine create -d virtualbox dev`

2. Make `dev` the current default docker for running commands (Windows):

`FOR /f "tokens=*" %i IN ('docker-machine env --shell cmd dev') DO %i`

3. `python manage.py makemigrations`

4. Setup SSL certificate on ACM

Copy ARN certificate to `zappa_settings.json`

5. Ensure all other credentials in `zappa_settings.json` are correct

6. `docker build -t notepark-deployment .`

7. Run docker container:

`docker run -ti -e AWS_ACCESS_KEY_ID=<YOUR KEY> -e AWS_SECRET_ACCESS_KEY=<YOUR KEY> --rm notepark-deployment bash`

8. Install dependencies:

`virtualenv env && source env/bin/activate && pip install -r requirements/production.txt && cd ..`

9. `zappa deploy production` or `zappa update production`

10. `zappa manage production migrate`

11. Create new superuser:

```
zappa invoke --raw production "from django.contrib.auth import get_user_model; User = get_user_model();
User.objects.create_superuser('admin', 'admin@notepark.net', '<PASSWORD>')"
```

12. `zappa certify production`
