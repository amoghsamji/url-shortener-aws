# 🔗 AWS Serverless URL Shortener

A simple serverless URL shortener built using **React, Python, and AWS**.

The application converts long URLs into short links and redirects users to the original URL. Short URLs are stored in **Amazon DynamoDB** and automatically expire after **7 days** using DynamoDB TTL.

---

## 🚀 Live Demo

[**Open the URL Shortener**](http://a-url-shortener.s3-website.eu-north-1.amazonaws.com/)

---

## ☁️ AWS Services Used

- **Amazon S3** – Frontend hosting
- **Amazon API Gateway** – REST API
- **AWS Lambda** – Backend logic
- **Amazon DynamoDB** – URL storage
- **DynamoDB TTL** – Automatic URL expiration
- **AWS IAM** – Access control
- **Amazon CloudWatch** – Monitoring and logs

---

## 🏗️ Architecture

```text
React
  ↓
Amazon S3
  ↓
API Gateway
  ↓
AWS Lambda
  ↓
DynamoDB

## ✨ Features
Generate short URLs
HTTP 302 redirects
7-day automatic URL expiration
Serverless architecture
React frontend
REST API
Persistent DynamoDB storage
🛠️ Tech Stack

Frontend: React, Vite, JavaScript, CSS

Backend: Python, Boto3

Cloud: AWS Lambda, API Gateway, DynamoDB, S3, IAM, CloudWatch

## 📚 What I Learned

Built this project to gain practical experience with AWS serverless architecture, including:

AWS Lambda
API Gateway
DynamoDB
Amazon S3
IAM
CORS
DynamoDB TTL

GitHub: https://github.com/amoghsamji

